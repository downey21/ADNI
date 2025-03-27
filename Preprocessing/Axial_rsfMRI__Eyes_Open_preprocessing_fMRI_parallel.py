
# -*- coding: utf-8 -*-

import sys
sys.path.append("/root/Project/ADNI/Python")

from preprocessing_fMRI_parallel import fmri_preprocess_all_subjects_parallel

from logging_utils import setup_logging

setup_logging("output_Axial_rsfMRI__Eyes_Open_preprocessing_fMRI_parallel.log")

NUM_CORES = 10

# fMRI (Axial rsfMRI (Eyes Open))
fmri_preprocess_all_subjects_parallel(
    base_dir="/root/data/ADNI/Axial_rsfMRI__Eyes_Open_/nifti/",
    measurement_type="Axial_rsfMRI__Eyes_Open_",
    ref_template="/usr/lib/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz",
    num_workers=NUM_CORES
)
