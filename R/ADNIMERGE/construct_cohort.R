
# -*- coding: utf-8 -*-

rm(list = ls())

setwd("/root/Project/ADNI")

suppressPackageStartupMessages({
    library(readr)
    library(dplyr)
})

adnimerge_col_vector <- c(
    "PTID",           # Patient ID
    "COLPROT",        # ADNI study protocol at the time of data acquisition (e.g., ADNI1, ADNI2)
    "ORIGPROT",       # ADNI study protocol at the time of enrollment (e.g., ADNI1, ADNI2)
    "VISCODE",        # Visit code (e.g., bl = baseline, m06 = month 6, m12 = month 12)
    "DX_bl",          # Baseline diagnosis (e.g., CN = cognitively normal, MCI = mild cognitive impairment, AD = Alzheimer's disease)
    "DX",             # Diagnosis at the current visit (e.g., CN = cognitively normal, MCI = mild cognitive impairment, AD = Alzheimer's disease)
    "AGE",            # Age
    "PTGENDER",       # Sex
    "APOE4",          # Number of APOE4 alleles (0, 1, 2)
    "PTETHCAT",       # Ethnicity
    "PTRACCAT",       # Race
    "EXAMDATE",       # Exam date
    "EXAMDATE_bl",    # Baseline exam date
    "AV45",           # Amyloid PET scan (commonly AV45, PIB, or FBB)
    "AV45_bl",        # Baseline amyloid PET scan
    "ABETA",          # CSF or plasma amyloid-beta biomarker
    "ABETA_bl",       # Baseline CSF or plasma amyloid-beta biomarker
    "TAU",            # CSF total tau biomarker
    "TAU_bl",         # Baseline CSF total tau biomarker
    "PTAU",           # CSF phosphorylated tau (specific to Alzheimer's disease)
    "PTAU_bl",        # Baseline CSF phosphorylated tau
    "FLDSTRENG",      # MRI field strength in Tesla (e.g., 1.5T or 3T)
    "FLDSTRENG_bl",   # Baseline MRI field strength
    "FSVERSION",      # FreeSurfer software version used for MRI analysis
    "Ventricles",     # Volume of the ventricles
    "Ventricles_bl",  # Baseline volume of the ventricles
    "Hippocampus",    # Volume of the hippocampus
    "Hippocampus_bl", # Baseline volume of the hippocampus
    "WholeBrain",     # Whole brain volume
    "WholeBrain_bl",  # Baseline whole brain volume
    "Entorhinal",     # Entorhinal cortex thickness or volume (related to AD)
    "Entorhinal_bl",  # Baseline entorhinal cortex thickness or volume
    "Fusiform",       # Fusiform gyrus thickness or volume (related to AD)
    "Fusiform_bl",    # Baseline fusiform gyrus thickness or volume
    "MidTemp",        # Middle temporal gyrus thickness or volume (related to AD)
    "MidTemp_bl",     # Baseline middle temporal gyrus thickness or volume
    "ICV",            # Intracranial volume
    "ICV_bl"          # Baseline intracranial volume
)

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

adnimerge <-
    adnimerge %>% 
    dplyr::select(dplyr::any_of(adnimerge_col_vector))

fmri <- readr::read_csv(
    "./R/ADNIMERGE/IDA_ADNI/All_Subjects_fMRI_Images_24Mar2025.csv",
    col_types = cols(
        .default = col_double(),
        subject_id = col_character(),
        fmri_visit = col_character(),
        fmri_date = col_date(format = ""),
        fmri_description = col_character(),
        fmri_mfr = col_character(),
        fmri_mfr_model = col_character(),
        fmri_sequence = col_character()
    )
)

fmri %>% count(fmri_description, name = "count", sort = TRUE) %>% print(n = 20)

fmri <-
    fmri %>%
    dplyr::select(c("subject_id", "fmri_date", "fmri_description", "fmri_mfr", "fmri_mfr_model")) %>%
    dplyr::rename(PTID = subject_id)

# Axial rsfMRI (Eyes Open); Axial_rsfMRI__Eyes_Open_
fmri <-
    fmri %>%
    dplyr::filter(fmri_description == "Axial rsfMRI (Eyes Open)")

fmri_bl <-
    fmri %>%
    dplyr::group_by(PTID) %>%
    dplyr::slice_min(order_by = fmri_date, n = 1, with_ties = FALSE) %>%
    dplyr::ungroup()

data_info <-
    fmri_bl %>%
    dplyr::left_join(adnimerge, by = "PTID") %>%
    dplyr::mutate(date_diff = abs(as.numeric(fmri_date - EXAMDATE))) %>%
    dplyr::group_by(PTID, fmri_date) %>%
    dplyr::slice_min(order_by = date_diff, n = 1, with_ties = FALSE) %>%
    dplyr::ungroup()

# data_info %>% filter(is.na(EXAMDATE)) %>% count()
# data_info[is.na(data_info$EXAMDATE), ]

data_info <- data_info %>% filter(!is.na(EXAMDATE))

# data_info %>%
#     dplyr::arrange(dplyr::desc(date_diff)) %>%
#     dplyr::select(PTID, fmri_date, EXAMDATE, date_diff) %>%
#     head()

data_info
