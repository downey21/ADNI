# Neuroimaging Data Preprocessing

This repository provides preprocessing pipelines for neuroimaging data (MRI and fMRI).  
It includes code for converting and preprocessing neuroimaging datasets, primarily from the **ADNI (Alzheimer’s Disease Neuroimaging Initiative)**.

## 1. Overview of Neuroimaging Data  

Neuroimaging techniques are widely used to study brain structure and function.  
This repository focuses on MRI and fMRI data.

### 1.1. MRI (MRI)
- **T1-weighted MRI (T1w):** High contrast between gray/white matter, used for structural analysis.
- **T2-weighted MRI (T2w):** Highlights fluid-filled areas, useful for detecting lesions.
- **FLAIR MRI:** Similar to T2 but suppresses cerebrospinal fluid (CSF), enhancing lesion detection.
- **Diffusion Tensor Imaging (DTI):** Tracks white matter fiber tracts, useful for studying brain connectivity.

### 1.2. Functional MRI (fMRI)
- **Resting-state fMRI (rsfMRI):** Captures spontaneous brain activity at rest.
- **Task-based fMRI:** Monitors brain activation in response to cognitive or motor tasks.

## 2. Data Formats  

- **DICOM (Digital Imaging and Communications in Medicine)**
  - Standard format for medical imaging with metadata.
  
- **NIfTI (Neuroimaging Informatics Technology Initiative)**
  - Commonly used format in neuroimaging research.
  - Stores 3D/4D volumes (`.nii` or `.nii.gz`).

- **MINC (Medical Imaging NetCDF)**
  - Less common but used in some research pipelines.

## 3. Preprocessing Pipeline  

### 3.1. MRI Preprocessing Steps

1. **Bias Field Correction**  
   - Removes scanner-induced intensity inhomogeneity.
   - **Tool:** `ANTs N4BiasFieldCorrection`

2. **Skull Stripping**  
   - Removes non-brain tissues (e.g., skull, fat).
   - **Tool:** `FSL BET`

3. **Tissue Segmentation**  
   - Segments brain into gray matter (GM), white matter (WM), and cerebrospinal fluid (CSF).
   - **Tool:** `FSL FAST`

4. **Spatial Normalization (MNI Standard Space)**  
   - Aligns images to a standard template (MNI152).
   - **Tool:** `ANTs or FSL FNIRT`

5. **Smoothing (Gaussian Filter)**
   - Enhances signal-to-noise ratio.
   - **Tool:** `nilearn.image.smooth_img`

### 3.2. fMRI Preprocessing Steps

1. **Slice Timing Correction**  
   - Adjusts for timing differences between slice acquisitions.
   - **Tool:** `FSL Slicetimer`

2. **Motion Correction**  
   - Realigns images to correct head motion.
   - **Tool:** `FSL MCFLIRT`

3. **Skull Stripping**
   - Removes non-brain tissues.

4. **Spatial Normalization (MNI Space)**
   - Aligns images to a standard template.

5. **Band-pass Filtering (0.01–0.1 Hz)**
   - Removes low-frequency drifts and high-frequency noise.
   - **Tool:** `nilearn.image.clean_img`

## 4. ROI (Region of Interest) Analysis

**ROI analysis** is a technique used to extract meaningful information from specific brain regions.  
Instead of analyzing the whole brain, researchers focus on predefined anatomical or functional regions.

### 4.1. ROI Extraction from MRI
- **Purpose:** Measure volume or intensity of specific regions.
- **Example Applications:**
  - Gray matter volume analysis in Alzheimer’s Disease.
  - White matter integrity assessment using DTI.
- **Common Brain Atlases:**
  - **AAL (Automated Anatomical Labeling) Atlas**
  - **Harvard-Oxford Atlas**
- **Processing Steps:**
  1. Register the subject's MRI to MNI space.
  2. Apply the selected atlas to segment regions.
  3. Extract mean intensity or volume for each ROI.

### 4.2. ROI Extraction from fMRI
- **Purpose:** Extract fMRI data from specific brain regions for connectivity analysis.
- **Common Brain Atlases:**
    - **AAL (Automated Anatomical Labeling) Atlas**
    - **Harvard-Oxford Atlas**
- **Processing Steps:**
	1. Preprocess fMRI (motion correction, spatial normalization, etc.).
	2. Register the subject’s fMRI data to MNI space.
	3. Apply the selected atlas to segment functional regions.
	4. Extract mean data from each ROI.

## 5. Dataset Sources

| Dataset  | Description  | Data Types |
|----------|-------------|------------|
| **ADNI (Alzheimer’s Disease Neuroimaging Initiative)** | Longitudinal study on Alzheimer’s Disease (AD), Mild Cognitive Impairment (MCI), and normal aging. | MRI, fMRI, PET, Genetic Data |
| **OASIS (Open Access Series of Imaging Studies)** | Aging and Alzheimer’s disease cohort. | MRI, fMRI, PET |
| **UK Biobank** | Large-scale biomedical database. | MRI, fMRI |
| **OpenNeuro** | Open-access neuroimaging repository. | fMRI, EEG, MEG |
| **TCIA (The Cancer Imaging Archive)** | Neuro-oncology imaging data. | MRI, PET |
