
# -*- coding: utf-8 -*-

# nohup env PYTHONDONTWRITEBYTECODE=1 python3 preprocessing_fMRI.py > output_preprocessing_fMRI.log 2>&1 < /dev/null &

import os
import glob
import nibabel as nib
from nipype.interfaces.fsl import BET, FAST, FNIRT, MCFLIRT, SliceTimer
from nipype.interfaces.ants import N4BiasFieldCorrection
from nilearn.image import smooth_img

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

        # Step 1: Motion Correction (MCFLIRT - FSL)
        log_print(f"Step 1/6: Motion Correction (MCFLIRT) - {file_id}")
        mcflirt = MCFLIRT(
            in_file=input_nifti,
            out_file=os.path.join(output_dir, f"motion_corrected_{file_id}.nii.gz"),
            mean_vol=True,
            save_plots=True
        )
        mcflirt.run()

        # Step 2: Slice Timing Correction (Slicetimer - FSL)
        log_print(f"Step 2/6: Slice Timing Correction - {file_id}")
        slicetimer = SliceTimer(
            in_file=os.path.join(output_dir, f"motion_corrected_{file_id}.nii.gz"),
            out_file=os.path.join(output_dir, f"slice_time_corrected_{file_id}.nii.gz"),
            interleaved=True  # Assumes interleaved slice acquisition
        )
        slicetimer.run()

        # Step 3: Skull Stripping (BET - Brain Extraction)
        log_print(f"Step 3/6: Skull Stripping (BET) - {file_id}")
        bet = BET(
            in_file=os.path.join(output_dir, f"slice_time_corrected_{file_id}.nii.gz"),
            out_file=os.path.join(output_dir, f"brain_{file_id}.nii.gz"),
            mask=True
        )
        bet.run()

        # Step 4: Bias Field Correction (N4ITK - ANTs)
        log_print(f"Step 4/6: Bias Field Correction (N4ITK) - {file_id}")
        n4 = N4BiasFieldCorrection(
            input_image=os.path.join(output_dir, f"brain_{file_id}.nii.gz"),
            output_image=os.path.join(output_dir, f"brain_n4_{file_id}.nii.gz")
        )
        n4.run()

        # Optional Step: Tissue Segmentation (FAST - FSL)
        log_print(f"Optional Step: Tissue Segmentation (FAST) - {file_id}")
        fast = FAST(in_files=os.path.join(output_dir, f"brain_n4_{file_id}.nii.gz"), number_classes=3)
        fast.run()

        # Step 5: Spatial Normalization (FNIRT - FSL)
        log_print(f"Step 5/6: Spatial Normalization (FNIRT) - {file_id}")
        fnirt = FNIRT(
            in_file=os.path.join(output_dir, f"brain_n4_{file_id}.nii.gz"),
            ref_file=ref_template,
            warped_file=os.path.join(output_dir, f"brain_mni_{file_id}.nii.gz")
        )
        fnirt.inputs.log_file = os.path.join(output_dir, f"FNIRT_log_{file_id}.txt")
        fnirt.run()

        # Step 6: Smoothing (Gaussian Smoothing)
        log_print(f"Step 6/6: Applying Gaussian Smoothing - {file_id}")
        smoothed_img = smooth_img(os.path.join(output_dir, f"brain_mni_{file_id}.nii.gz"), fwhm=5)  # fMRI에서는 보통 fwhm=5 사용
        nib.save(smoothed_img, os.path.join(output_dir, f"brain_smoothed_{file_id}.nii.gz"))

        log_print(f"Completed processing: {file_id}\n")

if __name__ == "__main__":

    preprocess_all_subjects(
        base_dir = "/root/data/ADNI/example/fMRI/nifti/",
        measurement_type = "Axial_HB_rsfMRI__Eyes_Open___MSV22_",
        ref_template = "/usr/lib/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz"
    )
