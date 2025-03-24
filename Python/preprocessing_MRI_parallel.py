
# -*- coding: utf-8 -*-

# nohup env PYTHONDONTWRITEBYTECODE=1 python3 preprocessing_MRI_parallel.py > output_preprocessing_MRI_parallel.log 2>&1 < /dev/null &

import os
import glob
import multiprocessing
import nibabel as nib
from nipype.interfaces.fsl import BET, FAST
from nipype.interfaces.ants import N4BiasFieldCorrection
from nilearn.image import smooth_img

import ants

from logging_utils import setup_logging, log_print

setup_logging("output_preprocessing_MRI_parallel.log")

def mri_preprocess_subject(subject_id, base_dir, measurement_type, ref_template, total_subjects, subject_index):
    """Preprocess all NIfTI files for a given subject."""
    subject_path = os.path.join(base_dir, subject_id)
    measurement_path = os.path.join(subject_path, measurement_type)

    if not os.path.exists(measurement_path):
        log_print(f"Skipping {subject_id} ({subject_index}/{total_subjects}): No {measurement_type} folder")
        return

    nifti_files = sorted(glob.glob(os.path.join(measurement_path, "*.nii.gz")))

    if len(nifti_files) == 0:
        log_print(f"Skipping {subject_id} ({subject_index}/{total_subjects}): No NIfTI file found")
        return

    for file_index, input_nifti in enumerate(nifti_files, start=1):
        file_id = os.path.basename(input_nifti).replace(".nii.gz", "")
        output_dir = os.path.join(measurement_path, "preprocessed", file_id)
        os.makedirs(output_dir, exist_ok=True)

        log_print(f"Processing {subject_id} ({subject_index}/{total_subjects}) - File {file_index}/{len(nifti_files)}: {file_id}")

        # Step 1: Bias Field Correction (N4ITK - ANTs)
        log_print(f"Step 1/5: Bias Field Correction (N4ITK) - {file_id}")
        n4 = N4BiasFieldCorrection(
            input_image=input_nifti,
            output_image=os.path.join(output_dir, f"n4_{file_id}.nii.gz")
        )
        n4.run()

        # Step 2: Skull Stripping (BET - Brain Extraction)
        log_print(f"Step 2/5: Skull Stripping (BET) - {file_id}")
        bet = BET(in_file=os.path.join(output_dir, f"n4_{file_id}.nii.gz"), out_file=os.path.join(output_dir, f"brain_n4_{file_id}.nii.gz"), mask=True)
        bet.run()

        # Step 3: Tissue Segmentation (FAST - FSL)
        log_print(f"Step 3/5: Tissue Segmentation (FAST) - {file_id}")
        fast = FAST(in_files=os.path.join(output_dir, f"brain_n4_{file_id}.nii.gz"), number_classes=3)
        fast.run()

        # Step 4: Spatial Normalization (ANTs)
        log_print(f"Step 4/5: Spatial Normalization (ANTs - Affine) - {file_id}")

        fixed_ref_template = ants.image_read(ref_template)

        reg = ants.registration(
            fixed=fixed_ref_template,
            moving=ants.image_read(os.path.join(output_dir, f"brain_n4_{file_id}.nii.gz")),
            type_of_transform="Affine"
        )

        brain_mni_path = os.path.join(output_dir, f"brain_mni_{file_id}.nii.gz")
        reg["warpedmovout"].to_filename(brain_mni_path)

        pve_types = {
            "CSF": f"{output_dir}/brain_n4_{file_id}_pve_0.nii.gz",
            "GM":  f"{output_dir}/brain_n4_{file_id}_pve_1.nii.gz",
            "WM":  f"{output_dir}/brain_n4_{file_id}_pve_2.nii.gz"
        }

        for tissue, pve_path in pve_types.items():
            warped_pve = ants.apply_transforms(
                fixed=fixed_ref_template,
                moving=ants.image_read(pve_path),
                transformlist=reg["fwdtransforms"],
                interpolator="linear",
                imagetype=0
            )

            output_pve_mni = os.path.join(output_dir, f"brain_n4_{file_id}_pve_{tissue}_mni.nii.gz")
            warped_pve.to_filename(output_pve_mni)

        mask_img = ants.image_read(os.path.join(output_dir, f"brain_n4_{file_id}_mask.nii.gz"))
        warped_mask = ants.apply_transforms(
            fixed=fixed_ref_template,
            moving=mask_img,
            transformlist=reg["fwdtransforms"],
            interpolator="nearestNeighbor",
            imagetype=0
        )

        output_mask_mni = os.path.join(output_dir, f"brain_n4_{file_id}_mask_mni.nii.gz")
        warped_mask.to_filename(output_mask_mni)

        # Step 5: Smoothing (Gaussian Smoothing)
        log_print(f"Step 5/5: Applying Gaussian Smoothing - {file_id}")
        smoothed_img = smooth_img(os.path.join(output_dir, f"brain_mni_{file_id}.nii.gz"), fwhm=2)
        nib.save(smoothed_img, os.path.join(output_dir, f"brain_smoothed_{file_id}.nii.gz"))

        log_print(f"Completed processing: {file_id}\n")

def mri_preprocess_all_subjects_parallel(base_dir, measurement_type, ref_template, num_workers):
    """Preprocess all subjects in parallel using multiprocessing."""
    subject_list = sorted([s for s in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, s))])
    total_subjects = len(subject_list)

    log_print(f"Starting parallel MRI Preprocessing for {total_subjects} subjects using {num_workers} workers...\n")

    with multiprocessing.Pool(processes=num_workers) as pool:
        pool.starmap(mri_preprocess_subject, [(subject, base_dir, measurement_type, ref_template, total_subjects, i+1) for i, subject in enumerate(subject_list)])

    log_print("All MRI Preprocessing Completed!")

if __name__ == "__main__":

    NUM_CORES = 10

    mri_preprocess_all_subjects_parallel(
        base_dir="/root/data/ADNI/example/MRI/nifti/",
        measurement_type="Accelerated_Sagittal_MPRAGE__MSV22_",
        ref_template="/usr/lib/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz",
        num_workers=NUM_CORES
    )
