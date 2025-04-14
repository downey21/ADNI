
# -*- coding: utf-8 -*-

rm(list = ls())

setwd("/root/Project/ADNI")

suppressPackageStartupMessages({
    library(readr)
    library(dplyr)
    library(tidyr)
})

adnimerge_col_vector <- c(
    "PTID",           # Patient ID
    "COLPROT",        # ADNI study protocol at the time of data acquisition (e.g., ADNI1, ADNI2)
    "ORIGPROT",       # ADNI study protocol at the time of enrollment (e.g., ADNI1, ADNI2)
    "DX",             # Diagnosis at the current visit (e.g., CN = cognitively normal, MCI = mild cognitive impairment, AD = Alzheimer's disease)
    "AGE",            # Age
    "PTGENDER",       # Sex
    "APOE4",          # Number of APOE4 alleles (0, 1, 2)
    "PTETHCAT",       # Ethnicity
    "PTRACCAT",       # Race
    "EXAMDATE"        # Exam date
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

# fmri %>% count(fmri_description, name = "count", sort = TRUE) %>% print(n = 20)

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
    dplyr::ungroup() %>%
    dplyr::select(-date_diff)

# data_info %>% filter(is.na(EXAMDATE)) %>% count()
# data_info[is.na(data_info$EXAMDATE), ]
# data_info %>% dplyr::count(DX)

data_info <- 
    data_info %>%
    dplyr::filter(!is.na(EXAMDATE)) %>%
    dplyr::filter(!is.na(DX)) %>%
    dplyr::filter(!is.na(APOE4))

# data_info %>%
#     dplyr::arrange(dplyr::desc(date_diff)) %>%
#     dplyr::select(PTID, fmri_date, EXAMDATE, date_diff) %>%
#     head()

data_info <-
    data_info %>%
    dplyr::select(-EXAMDATE)

# data_info %>%
#     dplyr::count(DX)

# data_info %>%
#     dplyr::summarise(dplyr::across(dplyr::everything(), ~sum(is.na(.)))) %>%
#     tidyr::pivot_longer(cols = dplyr::everything(), names_to = "column", values_to = "na_count") %>%
#     print(n = 50)

data_info <-
    data_info %>%
    dplyr::rename(
        SEX = PTGENDER,
        ETHNICITY = PTETHCAT,
        RACE = PTRACCAT   
    ) %>%
    dplyr::relocate(
        c("DX", "AGE", "SEX", "APOE4", "RACE", "ETHNICITY"),
        .after = PTID
    )

data_info %>%
    readr::write_csv("./result/data_info.csv")

data_info %>%
    dplyr::select(PTID, fmri_date) %>%
    dplyr::mutate(
        fmri_date = format(fmri_date, "%Y-%m-%d")
    ) %>%
    readr::write_csv("./result/ptid_date_list.csv")

data_info %>%
    dplyr::filter(DX == "Dementia") %>%
    readr::write_csv("./result/data_info_Dementia.csv")

data_info %>%
    dplyr::filter(DX == "CN") %>%
    readr::write_csv("./result/data_info_CN.csv")

data_info %>%
    dplyr::filter(DX == "MCI") %>%
    readr::write_csv("./result/data_info_MCI.csv")
