
# -*- coding: utf-8 -*-

# nohup env PYTHONDONTWRITEBYTECODE=1 python3 compute_falff_parallel.py > output_compute_falff_parallel.log 2>&1 < /dev/null &

import os
import glob
import multiprocessing

from compute_falff import compute_falff

from logging_utils import setup_logging, log_print

setup_logging("output_compute_falff_parallel.log")

def falff_preprocess_subject(subject_id, base_dir, measurement_type, total_subjects, subject_index):
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

        log_print(f"Processing {subject_id} ({subject_index}/{total_subjects}) - File {file_index}/{len(nifti_files)}: {file_id}")

        # Step 1: fALFF
        log_print(f"Step 1/1: Calculate fALFF - {file_id}")
        smoothed_path = os.path.join(output_dir, f"brain_smoothed_{file_id}.nii.gz")
        compute_falff(smoothed_path, low_freq=0.01, high_freq=0.1)

        log_print(f"Completed processing: {file_id}\n")

def falff_preprocess_all_subjects_parallel(base_dir, measurement_type, num_workers):
    """Preprocess all subjects in parallel using multiprocessing."""
    subject_list = sorted([s for s in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, s))])
    total_subjects = len(subject_list)

    log_print(f"Starting parallel fALFF Preprocessing for {total_subjects} subjects using {num_workers} workers...\n")

    with multiprocessing.Pool(processes=num_workers) as pool:
        pool.starmap(falff_preprocess_subject, [(subject, base_dir, measurement_type, total_subjects, i+1) for i, subject in enumerate(subject_list)])

    log_print("All fALFF Preprocessing Completed!")

if __name__ == "__main__":
    
    NUM_CORES = 10

    falff_preprocess_all_subjects_parallel(
        base_dir="/root/Project/ADNI/data/example/fMRI/nifti",
        measurement_type="Axial_HB_rsfMRI__Eyes_Open___MSV22_",
        num_workers=NUM_CORES
    )
