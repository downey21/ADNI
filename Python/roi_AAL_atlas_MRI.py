
# -*- coding: utf-8 -*-

import nibabel as nib
import numpy as np

aal_atlas_path = "/root/Project/ADNI/atlas/aal_for_SPM12/ROI_MNI_V4.nii"

atlas_img = nib.load(aal_atlas_path)
atlas_data = atlas_img.get_fdata()

mri_path = "/root/Project/ADNI/data/example/MRI/nifti/135_S_6509/Accelerated_Sagittal_MPRAGE__MSV22_/preprocessed/2024-08-08_11_16_51.0_I10914001/brain_smoothed_2024-08-08_11_16_51.0_I10914001.nii.gz"
mri_img = nib.load(mri_path)
mri_data = mri_img.get_fdata()

# Average intensitiy for each ROI
roi_values_dict = {}
for roi_idx in np.unique(atlas_data):
    if roi_idx == 0:
        continue
    roi_mask = atlas_data == roi_idx
    roi_mean = np.mean(mri_data[roi_mask])
    roi_values_dict[int(roi_idx)] = roi_mean

# Volume
gm_path = "/root/Project/ADNI/data/example/MRI/nifti/135_S_6509/Accelerated_Sagittal_MPRAGE__MSV22_/preprocessed/2024-08-08_11_16_51.0_I10914001/brain_n4_2024-08-08_11_16_51.0_I10914001_pve_GM_mni.nii.gz"
wm_path = "/root/Project/ADNI/data/example/MRI/nifti/135_S_6509/Accelerated_Sagittal_MPRAGE__MSV22_/preprocessed/2024-08-08_11_16_51.0_I10914001/brain_n4_2024-08-08_11_16_51.0_I10914001_pve_WM_mni.nii.gz"
csf_path = "/root/Project/ADNI/data/example/MRI/nifti/135_S_6509/Accelerated_Sagittal_MPRAGE__MSV22_/preprocessed/2024-08-08_11_16_51.0_I10914001/brain_n4_2024-08-08_11_16_51.0_I10914001_pve_CSF_mni.nii.gz"

gm = nib.load(gm_path)
wm = nib.load(wm_path)
csf = nib.load(csf_path)

gm_data = gm.get_fdata()
wm_data = wm.get_fdata()
csf_data = csf.get_fdata()

# Voxel volumn (mm^3)
np.prod(gm.header.get_zooms()[:3])
np.prod(wm.header.get_zooms()[:3])
np.prod(csf.header.get_zooms()[:3])

voxel_volume = np.prod(gm.header.get_zooms()[:3])

gm_volume = np.sum(gm_data) * voxel_volume
wm_volume = np.sum(wm_data) * voxel_volume
csf_volume = np.sum(csf_data) * voxel_volume

print(f"GM volume: {gm_volume:.2f} mm³")
print(f"WM volume: {wm_volume:.2f} mm³")
print(f"CSF volume: {csf_volume:.2f} mm³")

# Volume for each ROI
aal_atlas_path = "/root/Project/ADNI/atlas/aal_for_SPM12/ROI_MNI_V4.nii"
aal_atlas_roi_label_path = "/root/Project/ADNI/atlas/aal_for_SPM12/ROI_MNI_V4.txt"
pve_paths = {
    "CSF": csf_path,
    "GM": gm_path,
    "WM": wm_path,
}

roi_labels_dict = {}
with open(aal_atlas_roi_label_path) as f:
    for line in f:
        parts = line.strip().split('\t')
        if len(parts) == 3:
            _, name, idx = parts
            roi_labels_dict[int(idx)] = name.strip()

atlas_data = nib.load(aal_atlas_path).get_fdata()
pve_data = {tissue: nib.load(path).get_fdata() for tissue, path in pve_paths.items()}

# Voxel volumn (mm^3)
np.prod(gm.header.get_zooms()[:3])
np.prod(wm.header.get_zooms()[:3])
np.prod(csf.header.get_zooms()[:3])

voxel_volume = np.prod(gm.header.get_zooms()[:3])

roi_volumes = {tissue: {} for tissue in pve_paths}

for roi_idx in np.unique(atlas_data):
    if roi_idx == 0:
        continue
    mask = atlas_data == roi_idx
    for tissue, data in pve_data.items():
        volume = np.sum(data[mask]) * voxel_volume
        roi_volumes[tissue][roi_labels_dict.get(int(roi_idx), f"ROI_{roi_idx}")] = volume

# print example: GM
print("ROI-wise Gray Matter Volume:")
for roi_name, vol in roi_volumes["GM"].items():
    print(f"{roi_name:25}: {vol:.2f} mm³")
