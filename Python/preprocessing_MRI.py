
# -*- coding: utf-8 -*-

# nohup env PYTHONDONTWRITEBYTECODE=1 python3 preprocessing_MRI.py > output_preprocessing_MRI.log 2>&1 < /dev/null &

import os
import glob
import nibabel as nib
from nipype.interfaces.fsl import BET, FAST, FNIRT
from nipype.interfaces.ants import N4BiasFieldCorrection
from nilearn.image import smooth_img

from logging_utils import setup_logging, log_print

setup_logging("output_preprocessing_MRI.log")

# ==========================================
# MRI Data Preprocessing Pipeline
# ==========================================
# This script preprocesses MRI data using FSL and ANTs.
# Skull Stripping - BET (FSL): Removes the skull, leaving only the brain tissue.
# Bias Field Correction - N4ITK (ANTs): Corrects intensity inhomogeneity caused by magnetic field bias.
# Tissue Segmentation - FAST (FSL): Segments the brain into gray matter (GM), white matter (WM), and cerebrospinal fluid (CSF).
# Spatial Normalization - FNIRT (FSL): Aligns individual brains to a standard template (MNI space).
# Smoothing - Gaussian Smoothing (nilearn): Reduces noise by applying a Gaussian filter.
# ==========================================

# Define input and output paths
# input_nifti = "/root/data/ADNI/example/MRI/nifti/135_S_6509/Accelerated_Sagittal_MPRAGE__MSV22_/2024-08-08_11_16_51.0_I10914001.nii.gz"
# output_dir = "/root/data/ADNI/example/MRI/nifti/135_S_6509/preprocessed"
# os.makedirs(output_dir, exist_ok=True)

# Skull Stripping - Removing non-brain structures
# MRI images include skull and other tissues. BET (Brain Extraction Tool) extracts only brain regions.

# Explanation of output files from BET:
# - brain.nii.gz: Skull-stripped brain MRI image.
# - brain_mask.nii.gz: Binary mask representing the brain region (0 for background, 1 for brain tissue).
# - The mask is used to select only the brain region, essential for segmentation and fMRI analysis.

# print("Running Skull Stripping...")
# bet = BET(in_file=input_nifti, out_file=os.path.join(output_dir, "brain.nii.gz"), mask=True)
# bet.run()

# Bias Field Correction - Correcting intensity inhomogeneity
# Magnetic field inhomogeneity can cause bias field effects, making certain areas appear brighter/darker.
# ANTs' N4BiasFieldCorrection normalizes the intensity distribution.

# Output from N4BiasFieldCorrection:
# brain_n4.nii.gz: Bias Field Correction (N4) applied image

# print("Applying Bias Field Correction...")
# n4 = N4BiasFieldCorrection(input_image=os.path.join(output_dir, "brain.nii.gz"),
#                            output_image=os.path.join(output_dir, "brain_n4.nii.gz"))
# n4.run()

# Tissue Segmentation - Segmenting GM, WM, and CSF
# FAST (FSL) segments the brain into three tissue classes: gray matter (GM), white matter (WM), and cerebrospinal fluid (CSF).

# Tissue Segmentation Output from FAST:
# - brain_n4_seg.nii.gz: Segmentation mask (0=CSF, 1=GM, 2=WM)
# - brain_n4_pve_0.nii.gz: CSF Probability Map (0~1)
# - brain_n4_pve_1.nii.gz: GM Probability Map (0~1)
# - brain_n4_pve_2.nii.gz: WM Probability Map (0~1)
# - brain_n4_pveseg.nii.gz: PVE-based refined segmentation
# - brain_n4_mixeltype.nii.gz: Partial Volume Info (internal use)

# print("Performing Tissue Segmentation...")
# fast = FAST(in_files=os.path.join(output_dir, "brain_n4.nii.gz"), number_classes=3)
# fast.run()

# Spatial Normalization - Aligning to MNI template
# To compare different subjects, MRI images must be aligned to a standard brain template (MNI152).

# https://git.fmrib.ox.ac.uk/fsl/data_standard
# https://github.com/muschellij2/RGL_Export

# Explanation of MNI152 Templates:
# - MNI152_T1_2mm.nii.gz: 2mm resolution full-brain MNI152 template
# - MNI152_T1_1mm.nii.gz: 1mm resolution full-brain MNI152 template
# - MNI152_T1_2mm_brain.nii.gz: 2mm resolution skull-stripped MNI152 template
# - MNI152_T1_1mm_brain.nii.gz: 1mm resolution skull-stripped MNI152 template
#
# The MNI152 template is a standard brain used for spatial normalization.
# FNIRT will align individual brain data to this template for comparison across subjects.
# - The `_brain` versions are skull-stripped, typically used when the subject data is also skull-stripped.
# - The 2mm resolution version is more computationally efficient, while 1mm offers higher precision.

# FNIRT Output Files Explanation:
# - brain_mni.nii.gz: Skull-stripped brain after spatial normalization to MNI152 standard space.
# - brain_n4_warpcoef.nii.gz: Warp coefficient (info of transformation) file generated from FNIRT, storing deformation fields.

# print("Applying Spatial Normalization...")
# fnirt = FNIRT(
#     in_file=os.path.join(output_dir, "brain_n4.nii.gz"),  # Skull-Stripped Input
#     ref_file="/usr/lib/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz",  # Skull-Stripped Template
#     warped_file=os.path.join(output_dir, "brain_mni.nii.gz")
# )
# fnirt.run()

# Smoothing - Reducing noise with Gaussian filter
# Gaussian smoothing is applied to enhance signal-to-noise ratio. fwhm=4 means a 4mm blurring effect.

# Output from Smoothing:
# brain_smoothed.nii.gz - Smoothing Output

# print("Applying Gaussian Smoothing...")
# smoothed_img = smooth_img(os.path.join(output_dir, "brain_mni.nii.gz"), fwhm=4)
# nib.save(smoothed_img, os.path.join(output_dir, "brain_smoothed.nii.gz"))

# ==========================================
# Multi-Subject MRI Preprocessing Pipeline
# ==========================================

def preprocess_all_subjects(base_dir, measurement_type, ref_template):
    """
    Preprocess all subjects' MRI data from the given base directory.

    Args:
    - base_dir (str): Root directory containing all subject folders.
    - measurement_type (str): The measurement folder to process.
    - ref_template (str): The reference template for spatial normalization.
    """

    # List and sort subject folders
    subject_list = sorted([s for s in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, s))])
    total_subjects = len(subject_list)

    log_print(f"Starting MRI Preprocessing for {total_subjects} subjects...\n")

    for subject_index, subject_id in enumerate(subject_list, start=1):
        subject_path = os.path.join(base_dir, subject_id)
        preprocess_subject(subject_path, measurement_type, ref_template, total_subjects, subject_index)

    log_print("All MRI Preprocessing Completed!")

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

        # Step 1: Skull Stripping (BET - Brain Extraction)
        log_print(f"Step 1/5: Skull Stripping (BET) - {file_id}")
        bet = BET(in_file=input_nifti, out_file=os.path.join(output_dir, f"brain_{file_id}.nii.gz"), mask=True)
        bet.run()

        # Step 2: Bias Field Correction (N4ITK - ANTs)
        log_print(f"Step 2/5: Bias Field Correction (N4ITK) - {file_id}")
        n4 = N4BiasFieldCorrection(
            input_image=os.path.join(output_dir, f"brain_{file_id}.nii.gz"),
            output_image=os.path.join(output_dir, f"brain_n4_{file_id}.nii.gz")
        )
        n4.run()

        # Step 3: Tissue Segmentation (FAST - FSL)
        log_print(f"Step 3/5: Tissue Segmentation (FAST) - {file_id}")
        fast = FAST(in_files=os.path.join(output_dir, f"brain_n4_{file_id}.nii.gz"), number_classes=3)
        fast.run()

        # Step 4: Spatial Normalization (FNIRT - FSL)
        log_print(f"Step 4/5: Spatial Normalization (FNIRT) - {file_id}")
        fnirt = FNIRT(
            in_file=os.path.join(output_dir, f"brain_n4_{file_id}.nii.gz"),
            ref_file=ref_template,
            warped_file=os.path.join(output_dir, f"brain_mni_{file_id}.nii.gz")
        )
        fnirt.inputs.log_file = os.path.join(output_dir, f"FNIRT_log_{file_id}.txt")
        fnirt.run()

        # Step 5: Smoothing (Gaussian Smoothing)
        log_print(f"Step 5/5: Applying Gaussian Smoothing - {file_id}")
        smoothed_img = smooth_img(os.path.join(output_dir, f"brain_mni_{file_id}.nii.gz"), fwhm=4)
        nib.save(smoothed_img, os.path.join(output_dir, f"brain_smoothed_{file_id}.nii.gz"))

        log_print(f"Completed processing: {file_id}\n")

if __name__ == "__main__":

    preprocess_all_subjects(
        base_dir = "/root/data/ADNI/example/MRI/nifti/",
        measurement_type = "Accelerated_Sagittal_MPRAGE__MSV22_",
        ref_template = "/usr/lib/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz"
    )
