
# -*- coding: utf-8 -*-

import os
import nibabel as nib
from nilearn import plotting

import matplotlib.pyplot as plt

from matplotlib.colors import LinearSegmentedColormap

# Create a colormap for range -2 to +2
colors = [
    (-2.0, "blue"),     # Deep blue for lowest values
    (-1.0, "deepskyblue"),  # Lighter blue
    (0.0, "black"),     # Black at zero
    (0.5, "green"),     # Green near mid positive
    (1.0, "yellow"),    # Yellow higher
    (2.0, "red")        # Red for highest values
]
# Normalize position to 0~1 scale for colormap
positions = [(val + 2) / 4 for val, _ in colors]
color_values = [color for _, color in colors]

custom_cmap = LinearSegmentedColormap.from_list("blue_black_red", list(zip(positions, color_values)))

output_dir = "/root/Project/ADNI/Python/result_fMRI_visualization"

fmri_step_0 = "/root/Project/ADNI/data/example/fMRI/nifti/135_S_6509/Axial_HB_rsfMRI__Eyes_Open___MSV22_/2024-08-08_12_03_24.0_I10910954.nii.gz"
fmri_step_1 = "/root/Project/ADNI/data/example/fMRI/nifti/135_S_6509/Axial_HB_rsfMRI__Eyes_Open___MSV22_/preprocessed/2024-08-08_12_03_24.0_I10910954/slice_time_corrected_2024-08-08_12_03_24.0_I10910954.nii.gz"
fmri_step_2 = "/root/Project/ADNI/data/example/fMRI/nifti/135_S_6509/Axial_HB_rsfMRI__Eyes_Open___MSV22_/preprocessed/2024-08-08_12_03_24.0_I10910954/motion_corrected_2024-08-08_12_03_24.0_I10910954.nii.gz"
fmri_step_3 = "/root/Project/ADNI/data/example/fMRI/nifti/135_S_6509/Axial_HB_rsfMRI__Eyes_Open___MSV22_/preprocessed/2024-08-08_12_03_24.0_I10910954/brain_2024-08-08_12_03_24.0_I10910954.nii.gz"
fmri_step_4 = "/root/Project/ADNI/data/example/fMRI/nifti/135_S_6509/Axial_HB_rsfMRI__Eyes_Open___MSV22_/preprocessed/2024-08-08_12_03_24.0_I10910954/brain_mni_2024-08-08_12_03_24.0_I10910954.nii.gz"
fmri_step_5 = "/root/Project/ADNI/data/example/fMRI/nifti/135_S_6509/Axial_HB_rsfMRI__Eyes_Open___MSV22_/preprocessed/2024-08-08_12_03_24.0_I10910954/brain_smoothed_2024-08-08_12_03_24.0_I10910954.nii.gz"
fmri_step_6 = "/root/Project/ADNI/data/example/fMRI/nifti/135_S_6509/Axial_HB_rsfMRI__Eyes_Open___MSV22_/preprocessed/2024-08-08_12_03_24.0_I10910954/bandpass_filtered_2024-08-08_12_03_24.0_I10910954.nii.gz"

mask = "/root/Project/ADNI/data/example/fMRI/nifti/135_S_6509/Axial_HB_rsfMRI__Eyes_Open___MSV22_/preprocessed/2024-08-08_12_03_24.0_I10910954/brain_mean_2024-08-08_12_03_24.0_I10910954_mask.nii.gz"
mask_mni = "/root/Project/ADNI/data/example/fMRI/nifti/135_S_6509/Axial_HB_rsfMRI__Eyes_Open___MSV22_/preprocessed/2024-08-08_12_03_24.0_I10910954/brain_mean_2024-08-08_12_03_24.0_I10910954_mask_mni.nii.gz"

time_point = 50

# Step 0
fmri_img = nib.load(fmri_step_0)
fmri_img.shape

display = plotting.plot_epi(
    fmri_img.slicer[..., time_point],
    display_mode="ortho",
    cut_coords=(0, 0, 0),
    draw_cross=True,
    colorbar=True,
    black_bg=True,
    title="Step 0 (raw data)",
    cmap=plt.cm.nipy_spectral
)
display.savefig(os.path.join(output_dir, "step0.pdf"))
display.close()

# Step 1
fmri_img = nib.load(fmri_step_1)
fmri_img.shape

display = plotting.plot_epi(
    fmri_img.slicer[..., time_point],
    display_mode="ortho",
    cut_coords=(0, 0, 0),
    draw_cross=True,
    colorbar=True,
    black_bg=True,
    title="Step 1 (Slice Timing Correction)",
    cmap=plt.cm.nipy_spectral
)
display.savefig(os.path.join(output_dir, "step1.pdf"))
display.close()

# Step 2
fmri_img = nib.load(fmri_step_2)
fmri_img.shape

display = plotting.plot_epi(
    fmri_img.slicer[..., time_point],
    display_mode="ortho",
    cut_coords=(0, 0, 0),
    draw_cross=True,
    colorbar=True,
    black_bg=True,
    title="Step 2 (Motion Correction)",
    cmap=plt.cm.nipy_spectral
)
display.savefig(os.path.join(output_dir, "step2.pdf"))
display.close()

# Step 3
fmri_img = nib.load(fmri_step_3)
fmri_img.shape

display = plotting.plot_epi(
    fmri_img.slicer[..., time_point],
    display_mode="ortho",
    cut_coords=(0, 0, 0),
    draw_cross=True,
    colorbar=True,
    black_bg=True,
    title="Step 3 (Skull Stripping) with boundary",
    cmap=plt.cm.nipy_spectral
)
display.add_contours(
    nib.load(mask),
    colors='r',
    linewidths=1
)
display.savefig(os.path.join(output_dir, "step3.pdf"))
display.close()

# Step 4
fmri_img = nib.load(fmri_step_4)
fmri_img.shape

display = plotting.plot_epi(
    fmri_img.slicer[..., time_point],
    display_mode="ortho",
    cut_coords=(0, 0, 0),
    draw_cross=True,
    colorbar=True,
    black_bg=True,
    title="Step 4 (Spatial Normalization) with boundary",
    cmap=plt.cm.nipy_spectral
)
display.add_contours(
    nib.load(mask_mni),
    colors='r',
    linewidths=1
)
display.savefig(os.path.join(output_dir, "step4.pdf"))
display.close()

# Step 5
fmri_img = nib.load(fmri_step_5)
fmri_img.shape

display = plotting.plot_epi(
    fmri_img.slicer[..., time_point],
    display_mode="ortho",
    cut_coords=(0, 0, 0),
    draw_cross=True,
    colorbar=True,
    black_bg=True,
    title="Step 5 (Smoothing) with boundary",
    cmap=plt.cm.nipy_spectral
)
display.add_contours(
    nib.load(mask_mni),
    colors='r',
    linewidths=1
)
display.savefig(os.path.join(output_dir, "step5.pdf"))
display.close()

# Step 6
fmri_img = nib.load(fmri_step_6)
fmri_img.shape

display = plotting.plot_epi(
    fmri_img.slicer[..., time_point],
    display_mode="ortho",
    cut_coords=(0, 0, 0),
    draw_cross=True,
    colorbar=True,
    black_bg=True,
    title="Step 6 (Band-pass Filtering) with boundary",
    cmap=custom_cmap,
    vmin=-2,
    vmax=2
)
display.add_contours(
    nib.load(mask_mni),
    colors='r',
    linewidths=1
)
display.savefig(os.path.join(output_dir, "step6.pdf"))
display.close()
