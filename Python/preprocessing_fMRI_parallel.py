
# -*- coding: utf-8 -*-

# nohup env PYTHONDONTWRITEBYTECODE=1 python3 preprocessing_fMRI_parallel.py > output_preprocessing_fMRI_parallel.log 2>&1 < /dev/null &

import os
import glob
import multiprocessing
import numpy as np
import nibabel as nib
from nipype.interfaces.fsl import BET, MCFLIRT, SliceTimer
from nilearn.image import smooth_img, mean_img

import ants

from logging_utils import setup_logging, log_print

setup_logging("output_preprocessing_fMRI_parallel.log")

def fmri_preprocess_subject(subject_id, base_dir, measurement_type, ref_template, total_subjects, subject_index):
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

        # Step 1: Slice Timing Correction
        log_print(f"Step 1/5: Slice Timing Correction - {file_id}")
        slicetimer = SliceTimer(
            in_file=input_nifti,
            out_file=os.path.join(output_dir, f"slice_time_corrected_{file_id}.nii.gz"),
            interleaved=True
        )
        slicetimer.run()

        # Step 2: Motion Correction
        log_print(f"Step 2/5: Motion Correction (MCFLIRT) - {file_id}")
        motion_out = os.path.join(output_dir, f"motion_corrected_{file_id}.nii.gz")
        mcflirt = MCFLIRT(
            in_file=os.path.join(output_dir, f"slice_time_corrected_{file_id}.nii.gz"),
            out_file=motion_out,
            mean_vol=True,
            save_plots=True
        )
        mcflirt.run()

        # Step 3: Skull Stripping (BET with 4D support)
        log_print(f"Step 3/5: Skull Stripping (BET with 4D support) - {file_id}")
        
        mean_img_3d = mean_img(motion_out, copy_header=True)
        mean_img_path = os.path.join(output_dir, f"mean_{file_id}.nii.gz")
        mean_img_3d.to_filename(mean_img_path)

        bet = BET(
            in_file=mean_img_path,
            out_file=os.path.join(output_dir, f"brain_mean_{file_id}.nii.gz"),
            mask=True
        )
        bet.run()

        mask_path = os.path.join(output_dir, f"brain_mean_{file_id}_mask.nii.gz")
        mask_data = nib.load(mask_path).get_fdata()

        fmri_img = nib.load(motion_out)
        fmri_data = fmri_img.get_fdata()
        masked_data = fmri_data * mask_data[..., np.newaxis]

        masked_img = nib.Nifti1Image(masked_data, affine=fmri_img.affine, header=fmri_img.header)
        brain_4d_path = os.path.join(output_dir, f"brain_{file_id}.nii.gz")
        nib.save(masked_img, brain_4d_path)

        # Step 4: Spatial Normalization (ANTs)
        log_print(f"Step 4/5: Spatial Normalization (ANTs - Affine) - {file_id}")

        fixed_ref_template = ants.image_read(ref_template)

        reg = ants.registration(
            fixed=fixed_ref_template,
            moving=ants.image_read(mean_img_path),
            type_of_transform="Affine"
        )

        mean_mni_path = os.path.join(output_dir, f"mean_mni_{file_id}.nii.gz")
        reg["warpedmovout"].to_filename(mean_mni_path)

        warped_fmri = ants.apply_transforms(
            fixed=fixed_ref_template,
            moving=ants.image_read(brain_4d_path),
            transformlist=reg["fwdtransforms"],
            interpolator="linear",
            imagetype=3
        )

        brain_mni_path = os.path.join(output_dir, f"brain_mni_{file_id}.nii.gz")
        warped_fmri.to_filename(brain_mni_path)

        # Step 5: Smoothing
        log_print(f"Step 5/5: Applying Gaussian Smoothing - {file_id}")
        smoothed_img = smooth_img(os.path.join(output_dir, f"brain_mni_{file_id}.nii.gz"), fwhm=5)
        nib.save(smoothed_img, os.path.join(output_dir, f"brain_smoothed_{file_id}.nii.gz"))

        log_print(f"Completed processing: {file_id}\n")

def fmri_preprocess_all_subjects_parallel(base_dir, measurement_type, ref_template, num_workers):
    """Preprocess all subjects in parallel using multiprocessing."""
    subject_list = sorted([s for s in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, s))])
    total_subjects = len(subject_list)

    log_print(f"Starting parallel fMRI Preprocessing for {total_subjects} subjects using {num_workers} workers...\n")

    with multiprocessing.Pool(processes=num_workers) as pool:
        pool.starmap(fmri_preprocess_subject, [(subject, base_dir, measurement_type, ref_template, total_subjects, i+1) for i, subject in enumerate(subject_list)])

    log_print("All fMRI Preprocessing Completed!")

if __name__ == "__main__":
    
    NUM_CORES = 10

    fmri_preprocess_all_subjects_parallel(
        base_dir="/root/Project/ADNI/data/example/fMRI/nifti",
        measurement_type="Axial_HB_rsfMRI__Eyes_Open___MSV22_",
        ref_template="/usr/lib/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz",
        num_workers=NUM_CORES
    )
