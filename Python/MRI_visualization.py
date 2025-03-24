
# -*- coding: utf-8 -*-

import os
import nibabel as nib
from nilearn import plotting

import matplotlib.pyplot as plt

output_dir = "/root/Project/ADNI/Python/result_MRI_visualization"

mri_step_0 = "/root/Project/ADNI/data/example/MRI/nifti/135_S_6509/Accelerated_Sagittal_MPRAGE__MSV22_/2024-08-08_11_16_51.0_I10914001.nii.gz"
mri_step_1 = "/root/Project/ADNI/data/example/MRI/nifti/135_S_6509/Accelerated_Sagittal_MPRAGE__MSV22_/preprocessed/2024-08-08_11_16_51.0_I10914001/n4_2024-08-08_11_16_51.0_I10914001.nii.gz"
mri_step_2 = "/root/Project/ADNI/data/example/MRI/nifti/135_S_6509/Accelerated_Sagittal_MPRAGE__MSV22_/preprocessed/2024-08-08_11_16_51.0_I10914001/brain_n4_2024-08-08_11_16_51.0_I10914001.nii.gz"

mri_step_3_gm = "/root/Project/ADNI/data/example/MRI/nifti/135_S_6509/Accelerated_Sagittal_MPRAGE__MSV22_/preprocessed/2024-08-08_11_16_51.0_I10914001/brain_n4_2024-08-08_11_16_51.0_I10914001_pve_1.nii.gz"
mri_step_3_wm = "/root/Project/ADNI/data/example/MRI/nifti/135_S_6509/Accelerated_Sagittal_MPRAGE__MSV22_/preprocessed/2024-08-08_11_16_51.0_I10914001/brain_n4_2024-08-08_11_16_51.0_I10914001_pve_2.nii.gz"
mri_step_3_csf = "/root/Project/ADNI/data/example/MRI/nifti/135_S_6509/Accelerated_Sagittal_MPRAGE__MSV22_/preprocessed/2024-08-08_11_16_51.0_I10914001/brain_n4_2024-08-08_11_16_51.0_I10914001_pve_0.nii.gz"

mri_step_4 = "/root/Project/ADNI/data/example/MRI/nifti/135_S_6509/Accelerated_Sagittal_MPRAGE__MSV22_/preprocessed/2024-08-08_11_16_51.0_I10914001/brain_mni_2024-08-08_11_16_51.0_I10914001.nii.gz"

mri_step_4_gm = "/root/Project/ADNI/data/example/MRI/nifti/135_S_6509/Accelerated_Sagittal_MPRAGE__MSV22_/preprocessed/2024-08-08_11_16_51.0_I10914001/brain_n4_2024-08-08_11_16_51.0_I10914001_pve_GM_mni.nii.gz"
mri_step_4_wm = "/root/Project/ADNI/data/example/MRI/nifti/135_S_6509/Accelerated_Sagittal_MPRAGE__MSV22_/preprocessed/2024-08-08_11_16_51.0_I10914001/brain_n4_2024-08-08_11_16_51.0_I10914001_pve_WM_mni.nii.gz"
mri_step_4_csf = "/root/Project/ADNI/data/example/MRI/nifti/135_S_6509/Accelerated_Sagittal_MPRAGE__MSV22_/preprocessed/2024-08-08_11_16_51.0_I10914001/brain_n4_2024-08-08_11_16_51.0_I10914001_pve_CSF_mni.nii.gz"

mri_step_5 = "/root/Project/ADNI/data/example/MRI/nifti/135_S_6509/Accelerated_Sagittal_MPRAGE__MSV22_/preprocessed/2024-08-08_11_16_51.0_I10914001/brain_smoothed_2024-08-08_11_16_51.0_I10914001.nii.gz"

mask = "/root/Project/ADNI/data/example/MRI/nifti/135_S_6509/Accelerated_Sagittal_MPRAGE__MSV22_/preprocessed/2024-08-08_11_16_51.0_I10914001/brain_n4_2024-08-08_11_16_51.0_I10914001_mask.nii.gz"
mask_mni = "/root/Project/ADNI/data/example/MRI/nifti/135_S_6509/Accelerated_Sagittal_MPRAGE__MSV22_/preprocessed/2024-08-08_11_16_51.0_I10914001/brain_n4_2024-08-08_11_16_51.0_I10914001_mask_mni.nii.gz"

# Step 0
mri_img = nib.load(mri_step_0)
mri_img.shape

display = plotting.plot_anat(
    mri_img,
    display_mode="ortho",
    cut_coords=(0, 0, 0),
    draw_cross=True,
    colorbar=True,
    black_bg=True,
    title="Step 0 (raw data)",
    cmap=plt.cm.gray
)
display.savefig(os.path.join(output_dir, "step0.pdf"))
display.close()

# Step 1
mri_img = nib.load(mri_step_1)
mri_img.shape

display = plotting.plot_anat(
    mri_img,
    display_mode="ortho",
    cut_coords=(0, 0, 0),
    draw_cross=True,
    colorbar=True,
    black_bg=True,
    title="Step 1 (Bias Field Correction)",
    cmap=plt.cm.gray
)
display.savefig(os.path.join(output_dir, "step1.pdf"))
display.close()

# Step 2
mri_img = nib.load(mri_step_2)
mri_img.shape

display = plotting.plot_anat(
    mri_img,
    display_mode="ortho",
    cut_coords=(0, 0, 0),
    draw_cross=True,
    colorbar=True,
    black_bg=True,
    title="Step 2 (Skull Stripping) with boundary",
    cmap=plt.cm.gray
)
display.add_contours(
    nib.load(mask),
    colors='r',
    linewidths=1
)
display.savefig(os.path.join(output_dir, "step2.pdf"))
display.close()

# Step 3

# Gray Matter
step_3_gm_img = nib.load(mri_step_3_gm)
display = plotting.plot_anat(
    nib.load(mri_step_2),
    display_mode="ortho",
    cut_coords=(0, 0, 0),
    draw_cross=True,
    colorbar=True,
    black_bg=True,
    title="Step 3 (Tissue Segmentation) Gray Matter (GM)",
    cmap=plt.cm.gray
)
display.add_overlay(step_3_gm_img, cmap=plt.cm.Reds, alpha=0.8)
display.savefig(os.path.join(output_dir, "step3_gm.pdf"))
display.close()

# White Matter
step_3_wm_img = nib.load(mri_step_3_wm)
display = plotting.plot_anat(
    nib.load(mri_step_2),
    display_mode="ortho",
    cut_coords=(0, 0, 0),
    draw_cross=True,
    colorbar=True,
    black_bg=True,
    title="Step 3 (Tissue Segmentation) White Matter (WM)",
    cmap=plt.cm.gray
)
display.add_overlay(step_3_wm_img, cmap=plt.cm.Blues, alpha=0.8)
display.savefig(os.path.join(output_dir, "step3_wm.pdf"))
display.close()

# CSF
step_3_csf_img = nib.load(mri_step_3_csf)
display = plotting.plot_anat(
    nib.load(mri_step_2),
    display_mode="ortho",
    cut_coords=(0, 0, 0),
    draw_cross=True,
    colorbar=True,
    black_bg=True,
    title="Step 3 (Tissue Segmentation) CSF",
    cmap=plt.cm.gray
)
display.add_overlay(step_3_csf_img, cmap=plt.cm.Greens, alpha=0.8)
display.savefig(os.path.join(output_dir, "step3_csf.pdf"))
display.close()

# together
display = plotting.plot_anat(
    nib.load(mri_step_2),
    display_mode="ortho",
    cut_coords=(0, 0, 0),
    draw_cross=True,
    colorbar=True,
    black_bg=True,
    title="Step 3 (Tissue Segmentation) GM (Red) / WM (Blue) / CSF (Green)",
    cmap=plt.cm.gray
)
display.add_overlay(step_3_gm_img, cmap=plt.cm.Reds, alpha=0.8)
display.add_overlay(step_3_wm_img, cmap=plt.cm.Blues, alpha=0.8)
display.add_overlay(step_3_csf_img, cmap=plt.cm.Greens, alpha=0.8)
display.savefig(os.path.join(output_dir, "step3_all_tissue_overlay.pdf"))
display.close()

# Step 4
mri_img = nib.load(mri_step_4)
mri_img.shape

display = plotting.plot_anat(
    mri_img,
    display_mode="ortho",
    cut_coords=(0, 0, 0),
    draw_cross=True,
    colorbar=True,
    black_bg=True,
    title="Step 4 (Spatial Normalization) with boundary",
    cmap=plt.cm.gray
)
display.add_contours(
    nib.load(mask_mni),
    colors='r',
    linewidths=1
)
display.savefig(os.path.join(output_dir, "step4.pdf"))
display.close()

# Gray Matter
step_4_gm_img = nib.load(mri_step_4_gm)
display = plotting.plot_anat(
    nib.load(mri_step_4),
    display_mode="ortho",
    cut_coords=(0, 0, 0),
    draw_cross=True,
    colorbar=True,
    black_bg=True,
    title="Step 4 (Spatial Normalization) Gray Matter (GM)",
    cmap=plt.cm.gray
)
display.add_overlay(step_4_gm_img, cmap=plt.cm.Reds, alpha=0.8)
display.savefig(os.path.join(output_dir, "step4_gm.pdf"))
display.close()

# White Matter
step_4_wm_img = nib.load(mri_step_4_wm)
display = plotting.plot_anat(
    nib.load(mri_step_4),
    display_mode="ortho",
    cut_coords=(0, 0, 0),
    draw_cross=True,
    colorbar=True,
    black_bg=True,
    title="Step 4 (Spatial Normalization) White Matter (WM)",
    cmap=plt.cm.gray
)
display.add_overlay(step_4_wm_img, cmap=plt.cm.Blues, alpha=0.8)
display.savefig(os.path.join(output_dir, "step4_wm.pdf"))
display.close()

# CSF
step_4_csf_img = nib.load(mri_step_4_csf)
display = plotting.plot_anat(
    nib.load(mri_step_4),
    display_mode="ortho",
    cut_coords=(0, 0, 0),
    draw_cross=True,
    colorbar=True,
    black_bg=True,
    title="Step 4 (Spatial Normalization) CSF",
    cmap=plt.cm.gray
)
display.add_overlay(step_4_csf_img, cmap=plt.cm.Greens, alpha=0.8)
display.savefig(os.path.join(output_dir, "step4_csf.pdf"))
display.close()

# together
display = plotting.plot_anat(
    nib.load(mri_step_4),
    display_mode="ortho",
    cut_coords=(0, 0, 0),
    draw_cross=True,
    colorbar=True,
    black_bg=True,
    title="Step 4 (Spatial Normalization) GM (Red) / WM (Blue) / CSF (Green)",
    cmap=plt.cm.gray
)
display.add_overlay(step_4_gm_img, cmap=plt.cm.Reds, alpha=0.8)
display.add_overlay(step_4_wm_img, cmap=plt.cm.Blues, alpha=0.8)
display.add_overlay(step_4_csf_img, cmap=plt.cm.Greens, alpha=0.8)
display.savefig(os.path.join(output_dir, "step4_all_tissue_overlay.pdf"))
display.close()

# Step 5
mri_img = nib.load(mri_step_5)
mri_img.shape

display = plotting.plot_anat(
    mri_img,
    display_mode="ortho",
    cut_coords=(0, 0, 0),
    draw_cross=True,
    colorbar=True,
    black_bg=True,
    title="Step 5 (Smoothing) with boundary",
    cmap=plt.cm.gray
)
display.add_contours(
    nib.load(mask_mni),
    colors='r',
    linewidths=1
)
display.savefig(os.path.join(output_dir, "step5.pdf"))
display.close()
