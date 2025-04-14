
# -*- coding: utf-8 -*-

import sys
sys.path.append("/root/Project/ADNI/Python")

from compute_falff_parallel import falff_preprocess_all_subjects_parallel

from logging_utils import setup_logging

setup_logging("output_Axial_rsfMRI__Eyes_Open_compute_falff_parallel.log")

NUM_CORES = 10

# fMRI (Axial rsfMRI (Eyes Open))
falff_preprocess_all_subjects_parallel(
    base_dir="/root/data/ADNI/Axial_rsfMRI__Eyes_Open_/nifti/",
    measurement_type="Axial_rsfMRI__Eyes_Open_",
    num_workers=NUM_CORES
)
