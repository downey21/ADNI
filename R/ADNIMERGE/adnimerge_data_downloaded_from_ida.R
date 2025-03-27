
# -*- coding: utf-8 -*-

rm(list = ls())

# ADNIMERGE_18Feb2025.csv

# RID: Unique subject identifier
# * COLPROT: ADNI study protocol at the time of data acquisition (e.g., ADNI1, ADNI2)
# * ORIGPROT: ADNI study protocol at the time of enrollment (e.g., ADNI1, ADNI2)
# * PTID: Patient ID
# SITE: Study site code
# * VISCODE: Visit code (e.g., bl = baseline, m06 = month 6, m12 = month 12); indicates repeated measures
# EXAMDATE: Date of examination
# * DX_bl: Baseline diagnosis (e.g., CN = cognitively normal, MCI = mild cognitive impairment, AD = Alzheimer's disease)
# * AGE: Age
# * PTGENDER: Gender
# PTEDUCAT: Years of education
# PTETHCAT: Ethnicity category
# PTRACCAT: Race category
# PTMARRY: Marital status
# * APOE4: Number of APOE4 alleles (0, 1, or 2)
# FDG: FDG-PET (glucose metabolism)
# PIB: Amyloid PET scan result
# * AV45: Amyloid PET scan result (commonly used among PIB, AV45, FBB)
# FBB: Amyloid PET scan result
# * ABETA: CSF or plasma beta-amyloid biomarker
# * TAU: CSF tau protein biomarker
# * PTAU: CSF phosphorylated tau biomarker (specific to AD)
# CDRSB: Clinical Dementia Rating – Sum of Boxes
# ADAS11: ADAS-Cog cognitive assessment score (11-item)
# ADAS13: ADAS-Cog cognitive assessment score (13-item)
# ADASQ4: ADAS-Cog subtest score
# RAVLT_immediate: Score evaluating verbal memory and learning
# RAVLT_learning: Score evaluating verbal memory and learning
# RAVLT_forgetting: Score evaluating verbal memory and learning
# RAVLT_perc_forgetting: Score evaluating verbal memory and learning
# LDELTOTAL: Cognitive performance score for AD and MCI
# DIGITSCOR: Cognitive performance score for AD and MCI
# TRABSCOR: Cognitive performance score for AD and MCI
# FAQ: Functional Activities Questionnaire
# MOCA: Montreal Cognitive Assessment – general cognitive function
# Ecog~: Everyday Cognition questionnaire scores
# * FLDSTRENG: Magnetic field strength of the MRI scanner (e.g., 1.5T or 3T)
# * FSVERSION: FreeSurfer software version used for MRI analysis
# * IMAGEUID: MRI/PET scan image ID (used to match DICOM/NIfTI image files)
# * Ventricles: Volume of the ventricles
# * Hippocampus: Volume of the hippocampus
# * WholeBrain: Volume of the whole brain
# * Entorhinal: Thickness or volume of the entorhinal cortex (related to AD)
# * Fusiform: Thickness or volume of the fusiform gyrus (related to AD)
# * MidTemp: Thickness or volume of the middle temporal gyrus (related to AD)
# * ICV: Intracranial volume
# * DX: Diagnosis status (e.g., CN = cognitively normal, etc.)
# PCAA: Assessment score
# * _bl: Indicates baseline value

library(readr)

adnimerge <- readr::read_csv(
    "./R/ADNIMERGE/IDA_ADNI/ADNIMERGE_18Feb2025.csv",
    col_types = cols(
        .default = col_double(),
        COLPROT = col_character(),
        ORIGPROT = col_character(),
        PTID = col_character(),
        VISCODE = col_character(),
        EXAMDATE = col_date(format = ""),
        DX_bl = col_character(),
        PTGENDER = col_character(),
        PTETHCAT = col_character(),
        PTRACCAT = col_character(),
        PTMARRY = col_character(),
        ABETA = col_character(),
        TAU = col_character(),
        PTAU = col_character(),
        FLDSTRENG = col_character(),
        FSVERSION = col_character(),
        DX = col_character(),
        EXAMDATE_bl = col_date(format = ""),
        FLDSTRENG_bl = col_character(),
        FSVERSION_bl = col_character(),
        ABETA_bl = col_character(),
        TAU_bl = col_character(),
        PTAU_bl = col_character(),
        update_stamp = col_datetime(format = "")
    )
)

head(adnimerge)
colnames(adnimerge)
