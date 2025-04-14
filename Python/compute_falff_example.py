
# -*- coding: utf-8 -*-

import os
import nibabel as nib
from nilearn import plotting

import matplotlib.pyplot as plt

from compute_falff import compute_falff

fmri_smoothed = "/root/Project/ADNI/data/example/fMRI/nifti/002_S_0413/Axial_rsfMRI__Eyes_Open_/preprocessed/2017-06-21_13_23_38.0_I863058/brain_smoothed_2017-06-21_13_23_38.0_I863058.nii.gz"

compute_falff(fmri_smoothed, low_freq=0.01, high_freq=0.1)

fmri_smoothed_falff = "/root/Project/ADNI/data/example/fMRI/nifti/002_S_0413/Axial_rsfMRI__Eyes_Open_/preprocessed/2017-06-21_13_23_38.0_I863058/falff_brain_smoothed_2017-06-21_13_23_38.0_I863058.nii.gz"
output_dir = "/root/Project/ADNI/result"

img = nib.load(fmri_smoothed_falff)
img.shape

display = plotting.plot_anat(
    img,
    display_mode="ortho",
    cut_coords=(0, 0, 0),
    draw_cross=True,
    colorbar=True,
    black_bg=True,
    title="fALFF of the smoothed fMRI",
    cmap=plt.cm.nipy_spectral
)
display.savefig(os.path.join(output_dir, "fALFF.pdf"))
display.close()
