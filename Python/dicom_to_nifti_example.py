
# -*- coding: utf-8

# nohup env PYTHONDONTWRITEBYTECODE=1 python3 dicom_to_nifti_example.py > output_dicom_to_nifti_example.log 2>&1 < /dev/null &

import os
from subprocess import call

from logging_utils import setup_logging, log_print

setup_logging("output_dicom_to_nifti_example.log")

def convert_dicom_to_nifti(dicom_dir, nifti_dir, measurement_type_sequences):
    """DICOM -> NIfTI"""
    subject_list = sorted([s for s in os.listdir(dicom_dir) if os.path.isdir(os.path.join(dicom_dir, s))])
    total_subjects = len(subject_list)

    for i, subject_id in enumerate(subject_list, start=1):
        subject_path = os.path.join(dicom_dir, subject_id)

        log_print(f"Processing subject {subject_id} ({i}/{total_subjects})")

        for seq in measurement_type_sequences:
            seq_path = os.path.join(subject_path, seq)

            if not os.path.isdir(seq_path):
                continue

            date_folders = [d for d in sorted(os.listdir(seq_path)) if os.path.isdir(os.path.join(seq_path, d))]

            for scan_date in date_folders:
                scan_date_path = os.path.join(seq_path, scan_date)

                dicom_folders = [d for d in sorted(os.listdir(scan_date_path)) if os.path.isdir(os.path.join(scan_date_path, d))]

                for dicom_folder in dicom_folders:
                    dicom_path = os.path.join(scan_date_path, dicom_folder)

                    nii_subject_path = os.path.join(nifti_dir, subject_id, seq)
                    os.makedirs(nii_subject_path, exist_ok=True)

                    nii_filename = f"{scan_date}_{dicom_folder}.nii.gz"
                    nii_output_path = os.path.join(nii_subject_path, nii_filename)

                    log_print(f"Converting: {dicom_path} to {nii_output_path}")

                    # call(["dcm2niix", "-o", nii_subject_path, "-f", f"{scan_date}_{dicom_folder}", dicom_path])
                    call(["dcm2niix", "-z", "y", "-o", nii_subject_path, "-f", f"{scan_date}_{dicom_folder}", dicom_path])

if __name__ == "__main__":
    
    # MRI
    convert_dicom_to_nifti(
        dicom_dir="/root/data/ADNI/example/MRI/dicom",
        nifti_dir="/root/data/ADNI/example/MRI/nifti",
        measurement_type_sequences=["Accelerated_Sagittal_MPRAGE__MSV22_"]
    )

    # fMRI
    convert_dicom_to_nifti(
        dicom_dir="/root/data/ADNI/example/fMRI/dicom",
        nifti_dir="/root/data/ADNI/example/fMRI/nifti",
        measurement_type_sequences=["Axial_HB_rsfMRI__Eyes_Open___MSV22_"]
    )
