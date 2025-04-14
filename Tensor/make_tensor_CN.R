
# -*- coding: utf-8 -*-

rm(list = ls())

suppressPackageStartupMessages({
    library(rTensor)
    library(oro.nifti)
    library(readr)
})

data_info <- readr::read_csv(
    "/root/Project/ADNI/result/data_info_CN.csv",
    col_types = cols(
        .default = col_character(),
        AGE = col_double(),
        APOE4 = col_double(),
        fmri_date = col_date(format = "%Y-%m-%d")
    ),
    progress = FALSE
)

ptid_list <- data_info$PTID
fmri_date_list <- data_info$fmri_date

dims <- c(91, 109, 91)

measurement <- "Axial_rsfMRI__Eyes_Open_"
base_path <- paste0("/root/data/ADNI/", measurement, "/nifti")

n_subjects <- length(ptid_list)
tensor_array <- array(NA, dim = c(dims, n_subjects))

find_falff_brain_smoothed_file <- function(ptid, date) {

    preproc_dir <- file.path(
        base_path, ptid, measurement,
        "preprocessed"
    )
    subdirs <- list.dirs(preproc_dir, full.names = TRUE, recursive = FALSE)
    if (length(subdirs) == 0) {
        stop(paste("No subdirectories in preprocessed for", ptid))
    }
  
    found_path <- NULL
    for (subdir in subdirs) {
        files <- list.files(subdir, pattern = "^falff_brain_smoothed_.*\\.nii\\.gz$", full.names = TRUE)
        if (length(files) == 1) {
            found_path <- files
            break
        }
    }
  
    if (is.null(found_path)) {
        stop(paste("No file found for", ptid))
    }

    return(found_path)
}

for (i in seq_along(ptid_list)) {
    ptid <- ptid_list[i]
    fmri_date <- fmri_date_list[i]

    cat(sprintf("[%d/%d] Processing %s\n", i, n_subjects, ptid))

    nii_file_path <- find_falff_brain_smoothed_file(ptid, fmri_date)
    nii_data <- oro.nifti::readNIfTI(nii_file_path, reorient = FALSE)

    if (!all(dim(nii_data) == dims)) {
        stop(paste("Dimension mismatch at", ptid))
    }

    tensor_array[,,,i] <- nii_data
}
rm(nii_data); gc()
cat("All subjects processed.\n")

cat("Converting array to rTensor...\n")
tensor_rtensor <- rTensor::as.tensor(tensor_array)
rm(tensor_array); gc()
cat("rTensor object created.\n")

save(tensor_rtensor, file = "/root/data/ADNI/Axial_rsfMRI__Eyes_Open_/falff_tensor_CN.RData")
cat("rTensor object saving complete.\n")
