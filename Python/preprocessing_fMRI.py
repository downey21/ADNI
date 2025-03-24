
# -*- coding: utf-8 -*-

# nohup env PYTHONDONTWRITEBYTECODE=1 python3 preprocessing_fMRI.py > output_preprocessing_fMRI.log 2>&1 < /dev/null &

import os
import glob
import pandas as pd
import numpy as np
import nibabel as nib
from nipype.interfaces.fsl import BET, MCFLIRT, SliceTimer
from nilearn.image import smooth_img, mean_img, clean_img

import ants

from logging_utils import setup_logging, log_print

setup_logging("output_preprocessing_fMRI.log")

def preprocess_all_subjects(base_dir, measurement_type, ref_template):
    """
    Preprocess all subjects' fMRI data from the given base directory.

    Args:
    - base_dir (str): Root directory containing all subject folders.
    - measurement_type (str): The measurement folder to process.
    - ref_template (str): The reference template for spatial normalization.
    """

    # List and sort subject folders
    subject_list = sorted([s for s in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, s))])
    total_subjects = len(subject_list)

    log_print(f"Starting fMRI Preprocessing for {total_subjects} subjects...\n")

    for subject_index, subject_id in enumerate(subject_list, start=1):
        subject_path = os.path.join(base_dir, subject_id)
        preprocess_subject(subject_path, measurement_type, ref_template, total_subjects, subject_index)

    log_print("All fMRI Preprocessing Completed!")

def preprocess_subject(subject_path, measurement_type, ref_template, total_subjects, subject_index):
    """Preprocess all NIfTI files for a given subject."""
    measurement_path = os.path.join(subject_path, measurement_type)

    # Check if the specific measurement folder exists
    if not os.path.exists(measurement_path):
        log_print(f"Skipping {os.path.basename(subject_path)} ({subject_index}/{total_subjects}): No {measurement_type} folder")
        return

    # List and sort all NIfTI files in the measurement folder
    nifti_files = sorted(glob.glob(os.path.join(measurement_path, "*.nii.gz")))

    if len(nifti_files) == 0:
        log_print(f"Skipping {os.path.basename(subject_path)} ({subject_index}/{total_subjects}): No NIfTI file found")
        return

    # Process each NIfTI file separately
    for file_index, input_nifti in enumerate(nifti_files, start=1):
        file_id = os.path.basename(input_nifti).replace(".nii.gz", "")
        output_dir = os.path.join(measurement_path, "preprocessed", file_id)
        os.makedirs(output_dir, exist_ok=True)

        log_print(f"Processing subject {os.path.basename(subject_path)} ({subject_index}/{total_subjects}) - File {file_index}/{len(nifti_files)}: {file_id}")

        # Step 1: Slice Timing Correction
        log_print(f"Step 1/6: Slice Timing Correction - {file_id}")
        slicetimer = SliceTimer(
            in_file=input_nifti,
            out_file=os.path.join(output_dir, f"slice_time_corrected_{file_id}.nii.gz"),
            interleaved=True
        )
        slicetimer.run()

        # Step 2: Motion Correction
        log_print(f"Step 2/6: Motion Correction (MCFLIRT) - {file_id}")
        motion_out = os.path.join(output_dir, f"motion_corrected_{file_id}.nii.gz")
        mcflirt = MCFLIRT(
            in_file=os.path.join(output_dir, f"slice_time_corrected_{file_id}.nii.gz"),
            out_file=motion_out,
            mean_vol=True,
            save_plots=True
        )
        mcflirt.run()

        motion = np.loadtxt(os.path.join(output_dir, f"motion_corrected_{file_id}.nii.gz.par"))

        motion_deriv = np.vstack([np.zeros((1, 6)), np.diff(motion, axis=0)]) # diff (1st row = 0)
        confounds = np.hstack([motion, motion_deriv])
        columns = ["X", "Y", "Z", "RotX", "RotY", "RotZ", "dX", "dY", "dZ", "dRotX", "dRotY", "dRotZ"]

        confounds_df = pd.DataFrame(confounds, columns=columns)
        confounds_df.to_csv(os.path.join(output_dir, f"motion_corrected_{file_id}_confounds.tsv"), sep="\t", index=False)

        # Step 3: Skull Stripping (BET with 4D support)
        log_print(f"Step 3/6: Skull Stripping (BET with 4D support) - {file_id}")

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
        log_print(f"Step 4/6: Spatial Normalization (ANTs - Affine) - {file_id}")

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

        warped_mask = ants.apply_transforms(
            fixed=fixed_ref_template,
            moving=ants.image_read(mask_path),
            transformlist=reg["fwdtransforms"],
            interpolator="nearestNeighbor",
            imagetype=0
        )

        mni_mask_path = os.path.join(output_dir, f"brain_mean_{file_id}_mask_mni.nii.gz")
        warped_mask.to_filename(mni_mask_path)

        # Step 5: Smoothing
        log_print(f"Step 5/6: Applying Gaussian Smoothing - {file_id}")
        smoothed_img = smooth_img(os.path.join(output_dir, f"brain_mni_{file_id}.nii.gz"), fwhm=4)
        nib.save(smoothed_img, os.path.join(output_dir, f"brain_smoothed_{file_id}.nii.gz"))

        # Step 6: Band-pass Filtering
        log_print(f"Step 6/6: Applying Band-pass Filtering - {file_id}")

        smoothed_fmri_img = nib.load(os.path.join(output_dir, f"brain_smoothed_{file_id}.nii.gz"))
        tr = smoothed_fmri_img.header.get_zooms()[3]

        filtered_img = clean_img(
            smoothed_fmri_img, 
            detrend=True,
            standardize=True,
            low_pass=0.1, high_pass=0.01,
            t_r=tr,
            mask_img=mni_mask_path,
            # confounds=os.path.join(output_dir, f"motion_corrected_{file_id}.nii.gz.par")
            confounds=os.path.join(output_dir, f"motion_corrected_{file_id}_confounds.tsv")
        )

        filtered_img.set_qform(smoothed_fmri_img.affine)
        filtered_img.header.set_zooms(smoothed_fmri_img.header.get_zooms())

        nib.save(filtered_img, os.path.join(output_dir, f"bandpass_filtered_{file_id}.nii.gz"))

        log_print(f"Completed processing: {file_id}\n")

if __name__ == "__main__":

    preprocess_all_subjects(
        base_dir = "/root/data/ADNI/example/fMRI/nifti/",
        measurement_type = "Axial_HB_rsfMRI__Eyes_Open___MSV22_",
        ref_template = "/usr/lib/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz"
    )
