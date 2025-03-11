
# -*- coding: utf-8

# nohup python3 nifti_to_tensor_example_fMRI.py > output_nifti_to_tensor_example_fMRI.log 2>&1 < /dev/null &

import nibabel as nib
import numpy as np
from nilearn import plotting
import matplotlib.pyplot as plt

nifti_path = "/root/data/ADNI/example/fMRI/nifti/135_S_6509/Axial_HB_rsfMRI__Eyes_Open___MSV22_/2024-08-08_12_03_24.0_I10910954.nii.gz"
img = nib.load(nifti_path)

print(img.shape) # (64, 64, 48, 200)
print(img.header)

# NumPy array
img_data = img.get_fdata()

print(f"NIfTI Shape: {img_data.shape}") # (64, 64, 48, 200)
print(f"Data Type: {img_data.dtype}") # float64

# time
num_timepoints = img_data.shape[3]

# Plot using nilearn
fmri_3d = img.slicer[..., 0]
plotting.plot_epi(
    fmri_3d,
    display_mode="ortho",
    cut_coords=(0, 0, 0),
    title="fMRI Baseline Image (First Time Point)"
)
plotting.show()

# Plot using matplotlib

# Selecting the middle slice
time_point = num_timepoints // 2
slice_x = img_data.shape[0] // 2
slice_y = img_data.shape[1] // 2
slice_z = img_data.shape[2] // 2

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

axes[0].imshow(img_data[slice_x, :, :, time_point], cmap="gray", origin="lower")
axes[0].set_title(f"Sagittal View (t={time_point})")
axes[0].axis("off")

axes[1].imshow(img_data[:, slice_y, :, time_point], cmap="gray", origin="lower")
axes[1].set_title(f"Coronal View (t={time_point})")
axes[1].axis("off")

axes[2].imshow(img_data[:, :, slice_z, time_point], cmap="gray", origin="lower")
axes[2].set_title(f"Axial View (t={time_point})")
axes[2].axis("off")

plt.show()

# Histogram of MRI Intensity Values at time_point
plt.hist(img_data[:, :, :, time_point].flatten(), bins=100, color="blue", alpha=0.7)
plt.xlabel("Voxel Intensity")
plt.ylabel("Frequency")
plt.title(f"Histogram of fMRI Intensity at t={time_point}")
plt.show()

# intensity changes over time
voxel_x, voxel_y, voxel_z = slice_x, slice_y, slice_z  # specific point

plt.plot(range(num_timepoints), img_data[voxel_x, voxel_y, voxel_z, :], color="blue")
plt.xlabel("Time Points")
plt.ylabel("Signal Intensity")
plt.title(f"fMRI Signal at Voxel ({voxel_x}, {voxel_y}, {voxel_z})")
plt.show()
