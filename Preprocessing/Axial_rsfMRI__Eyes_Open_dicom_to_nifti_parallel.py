
# -*- coding: utf-8 -*-

import sys
sys.path.append("/root/Project/ADNI/Python")

from dicom_to_nifti_parallel import convert_dicom_to_nifti_parallel

from logging_utils import setup_logging

setup_logging("output_Axial_rsfMRI__Eyes_Open_dicom_to_nifti_parallel.log")

NUM_CORES = 30

# fMRI (Axial rsfMRI (Eyes Open))
convert_dicom_to_nifti_parallel(
    dicom_dir="/root/data/ADNI/Axial_rsfMRI__Eyes_Open_/dicom",
    nifti_dir="/root/data/ADNI/Axial_rsfMRI__Eyes_Open_/nifti",
    measurement_type_sequences=["Axial_rsfMRI__Eyes_Open_"],
    num_workers=NUM_CORES
)
