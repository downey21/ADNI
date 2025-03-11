
# -*- coding: utf-8 -*-

rm(list = ls())

library(oro.nifti)
library(ggplot2)
library(reshape2)

dir.create("./Project/ADNI/result/fMRI", showWarnings = FALSE, recursive = TRUE)

nifti_path <- "/root/data/ADNI/example/fMRI/nifti/135_S_6509/Axial_HB_rsfMRI__Eyes_Open___MSV22_/2024-08-08_12_03_24.0_I10910954.nii.gz"

fmri_data <- oro.nifti::readNIfTI(nifti_path, reorient = FALSE)

print(dim(fmri_data))  # (64, 64, 48, 200)

# array 변환
fmri_matrix <- as.array(fmri_data)

cat("NIfTI Shape:", dim(fmri_matrix), "\n")
cat("Data Type:", class(fmri_matrix), "\n")

num_timepoints <- dim(fmri_matrix)[4]

# First time point
fmri_3d <- fmri_matrix[,,,1]

# Selecting the middle slice
slice_x <- dim(fmri_matrix)[1] %/% 2
slice_y <- dim(fmri_matrix)[2] %/% 2
slice_z <- dim(fmri_matrix)[3] %/% 2

# Plot using oro.nifti::orthographic
pdf("./Project/ADNI/result/fMRI/fmri_orthographic.pdf", width = 8, height = 6)
oro.nifti::orthographic(nifti(fmri_3d), xyz = c(slice_x, slice_y, slice_z), main = "fMRI Baseline Image (First Time Point)")
invisible(dev.off())

# Selecting the middle time point
time_point <- num_timepoints %/% 2

# Plot using ggplot2
plot_slice <- function(slice_matrix, title, filename) {
    df <- reshape2::melt(slice_matrix)
    p <- ggplot2::ggplot(df, ggplot2::aes(x = Var1, y = Var2, fill = value)) +
        ggplot2::geom_tile() +
        ggplot2::scale_fill_gradient(low = "black", high = "white") +
        ggplot2::theme_minimal() +
        ggplot2::ggtitle(title) +
        ggplot2::coord_fixed()
    
    pdf(filename, width = 6, height = 6)
    print(p)
    invisible(dev.off())
}

# Sagittal View
plot_slice(fmri_matrix[slice_x, , , time_point], paste("Sagittal View (t=", time_point, ")"), "./Project/ADNI/result/fMRI/fmri_sagittal.pdf")
# Coronal View
plot_slice(fmri_matrix[, slice_y, , time_point], paste("Coronal View (t=", time_point, ")"), "./Project/ADNI/result/fMRI/fmri_coronal.pdf")
# Axial View
plot_slice(fmri_matrix[, , slice_z, time_point], paste("Axial View (t=", time_point, ")"), "./Project/ADNI/result/fMRI/fmri_axial.pdf")

# Histogram of MRI Intensity Values
pdf("./Project/ADNI/result/fMRI/fmri_intensity_histogram.pdf", width = 8, height = 6)
intensity_data <- data.frame(value = as.vector(fmri_matrix[, , , time_point]))
p <- ggplot2::ggplot(intensity_data, ggplot2::aes(x=value)) +
    ggplot2::geom_histogram(bins=100, fill="blue", alpha=0.7) +
    ggplot2::xlab("Voxel Intensity") +
    ggplot2::ylab("Frequency") +
    ggplot2::ggtitle(paste("Histogram of fMRI Intensity at t=", time_point)) +
    ggplot2::theme_minimal()
print(p)
invisible(dev.off())

# intensity changes over time at specific point
voxel_x <- slice_x
voxel_y <- slice_y
voxel_z <- slice_z

pdf("./Project/ADNI/result/fMRI/fmri_signal_over_time.pdf", width = 8, height = 6)
time_series <- data.frame(time = 1:num_timepoints, intensity = fmri_matrix[voxel_x, voxel_y, voxel_z, ])
p <- ggplot2::ggplot(time_series, ggplot2::aes(x=time, y=intensity)) +
    ggplot2::geom_line(color="blue") +
    ggplot2::xlab("Time Points") +
    ggplot2::ylab("Signal Intensity") +
    ggplot2::ggtitle(paste("fMRI Signal at Voxel (", voxel_x, ",", voxel_y, ",", voxel_z, ")")) +
    ggplot2::theme_minimal()
print(p)
invisible(dev.off())
