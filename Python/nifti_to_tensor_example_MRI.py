
# -*- coding: utf-8

# nohup python3 nifti_to_tensor_example_MRI.py > output_nifti_to_tensor_example_MRI.log 2>&1 < /dev/null &

import nibabel as nib
import numpy as np
from nilearn import plotting
import matplotlib.pyplot as plt

nifti_path = "/root/data/ADNI/example/MRI/nifti/135_S_6509/Accelerated_Sagittal_MPRAGE__MSV22_/2024-08-08_11_16_51.0_I10914001.nii.gz"
img = nib.load(nifti_path)

print(img.shape) # (208, 256, 256)
print(img.header)

# NumPy array
img_data = img.get_fdata()

print(f"NIfTI Shape: {img_data.shape}") # (208, 256, 256)
print(f"Data Type: {img_data.dtype}") # float64

# Plot using nilearn
plotting.plot_anat(img,
    display_mode="ortho", # "ortho", "x", "y", "z", "xz", "yz", "yx"
    cut_coords=(0, 0, 0),
    draw_cross=True,
    annotate=True,
    title="T1-weighted MRI"
)
plotting.show()

# Plot using matplotlib

# Selecting the middle slice
slice_x = img_data.shape[0] // 2
slice_y = img_data.shape[1] // 2
slice_z = img_data.shape[2] // 2

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

axes[0].imshow(img_data[slice_x, :, :], cmap="gray", origin="lower")
axes[0].set_title("Sagittal View")
axes[0].axis("off")

axes[1].imshow(img_data[:, slice_y, :], cmap="gray", origin="lower")
axes[1].set_title("Coronal View")
axes[1].axis("off")

axes[2].imshow(img_data[:, :, slice_z], cmap="gray", origin="lower")
axes[2].set_title("Axial View")
axes[2].axis("off")

plt.show()

# Histogram of MRI Intensity Values
plt.hist(img_data.flatten(), bins=100, color="blue", alpha=0.7)
plt.xlabel("Voxel Intensity")
plt.ylabel("Frequency")
plt.title("Histogram of MRI Intensity Values")
plt.show()
