
# -*- coding: utf-8 -*-

import numpy as np
import nibabel as nib
from nilearn.input_data import NiftiLabelsMasker

aal_atlas_path = "/root/Project/ADNI/atlas/aal_for_SPM12/ROI_MNI_V4.nii"

fmri_path = "/root/Project/ADNI/data/example/fMRI/nifti/135_S_6509/Axial_HB_rsfMRI__Eyes_Open___MSV22_/preprocessed/2024-08-08_12_03_24.0_I10910954/bandpass_filtered_2024-08-08_12_03_24.0_I10910954.nii.gz"

fmri_img = nib.load(fmri_path)
tr = fmri_img.header.get_zooms()[3]

masker = NiftiLabelsMasker(
    labels_img=aal_atlas_path,
    t_r=tr
)

roi_time_series = masker.fit_transform(fmri_path)

type(roi_time_series)
print("Shape of ROI time series:", roi_time_series.shape)

# Label
aal_atlas_roi_label_path = "/root/Project/ADNI/atlas/aal_for_SPM12/ROI_MNI_V4.txt"

with open(aal_atlas_roi_label_path, "r") as f:
    roi_labels = [line.strip() for line in f.readlines()]

print(f"# of ROI labels: {len(roi_labels)}")
print(roi_labels[:5])

# Example:
# code: FAG
# ROI: Precentral_L (Left Precentral gyrus)
# id: 2001

# Mapping
atlas_img = nib.load(aal_atlas_path)
atlas_data = atlas_img.get_fdata()

roi_labels_dict = {}
with open(aal_atlas_roi_label_path) as f:
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) == 3:
            _, name, idx = parts
            roi_labels_dict[int(idx)] = name.strip()

def get_roi_name_from_coordinate(atlas_input, roi_labels_dict, coord):
    """
    Determine the ROI name for a given voxel coordinate using the atlas.

    Parameters:
    - atlas_input: Either a nibabel Nifti1Image object or a 3D NumPy array from get_fdata().
    - roi_labels_dict: Dictionary mapping ROI indices to ROI names.
    - coord: Tuple (x, y, z) indicating voxel coordinate.

    Returns:
    - A string message indicating ROI name or background.
    """
    x, y, z = coord

    # Handle atlas input
    if isinstance(atlas_input, nib.Nifti1Image):
        atlas_data = atlas_input.get_fdata()
    elif isinstance(atlas_input, np.ndarray):
        atlas_data = atlas_input
    else:
        raise TypeError("atlas_input must be a nibabel Nifti1Image or a NumPy ndarray.")

    # Extract ROI index at the given coordinate
    roi_index = int(atlas_data[x, y, z])

    # Determine ROI name
    if roi_index == 0:
        return "This voxel does not belong to any ROI (background)."
    elif roi_index in roi_labels_dict:
        return f"This voxel belongs to ROI: {roi_labels_dict[roi_index]}"
    else:
        return f"ROI index {roi_index} not found in the label dictionary."

get_roi_name_from_coordinate(atlas_data, roi_labels_dict, (40, 50, 40))
get_roi_name_from_coordinate(atlas_data, roi_labels_dict, (10, 10, 40))
