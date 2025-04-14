
# -*- coding: utf-8 -*-

rm(list = ls())

suppressPackageStartupMessages({
    library(rTensor)
    library(oro.nifti)
})

dims <- c(91, 109, 91, 200)

ptid_list <- c("135_S_6509", "135_S_6703")
fmri_date_list <- c("2024-08-08", "2024-03-28")

measurement <- "Axial_HB_rsfMRI__Eyes_Open___MSV22_"
base_path <- "/root/Project/ADNI/data/example/fMRI/nifti"

n_subjects <- length(ptid_list)
tensor_array <- array(NA, dim = c(dims, n_subjects))

find_brain_smoothed_file <- function(ptid, date) {

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
        files <- list.files(subdir, pattern = "^brain_smoothed_.*\\.nii\\.gz$", full.names = TRUE)
        if (length(files) == 1) {
            found_path <- files
            break
        }
    }
  
    if (is.null(found_path)) {
        stop(paste("No brain_smoothed file found for", ptid))
    }

    return(found_path)
}

for (i in seq_along(ptid_list)) {
    ptid <- ptid_list[i]
    fmri_date <- fmri_date_list[i]

    nii_file_path <- find_brain_smoothed_file(ptid, fmri_date)
    nii_data <- oro.nifti::readNIfTI(nii_file_path, reorient = FALSE)

    if (!all(dim(nii_data) == dims)) {
        stop(paste("Dimension mismatch at", ptid))
    }

    tensor_array[,,,,i] <- nii_data
}
rm(nii_data); gc()
tensor_rtensor <- rTensor::as.tensor(tensor_array)
rm(tensor_array); gc()

save(tensor_rtensor, file = "/root/Project/ADNI/result/tensor_example.RData")
