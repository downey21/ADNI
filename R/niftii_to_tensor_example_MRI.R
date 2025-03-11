
# -*- coding: utf-8 -*-

rm(list = ls())

library(oro.nifti)
library(ggplot2)
library(reshape2)

dir.create("./Project/ADNI/result/MRI", showWarnings = FALSE, recursive = TRUE)

nifti_path <- "/root/data/ADNI/example/MRI/nifti/135_S_6509/Accelerated_Sagittal_MPRAGE__MSV22_/2024-08-08_11_16_51.0_I10914001.nii.gz"

mri_data <- oro.nifti::readNIfTI(nifti_path, reorient = FALSE)

print(dim(mri_data))  # (208, 256, 256)

# array
mri_matrix <- as.array(mri_data)

cat("NIfTI Shape:", dim(mri_matrix), "\n")
cat("Data Type:", class(mri_matrix), "\n")

# Selecting the middle slice
slice_x <- dim(mri_matrix)[1] %/% 2
slice_y <- dim(mri_matrix)[2] %/% 2
slice_z <- dim(mri_matrix)[3] %/% 2

# Plot using oro.nifti::orthographic

# oro.nifti::tim.colors()
# oro.nifti::hotmetal()

pdf("./Project/ADNI/result/MRI/orthographic_view.pdf", width = 8, height = 6)
oro.nifti::orthographic(mri_data, col = oro.nifti::tim.colors(), xyz = c(slice_x, slice_y, slice_z), main = "T1-weighted MRI")
invisible(dev.off())

# Plot using ggplot2
plot_slice <- function(slice_matrix, title, filename) {
    df <- reshape2::melt(slice_matrix)
    p <-
        ggplot2::ggplot(df, ggplot2::aes(x = Var1, y = Var2, fill = value)) +
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
sagittal_plot <- plot_slice(mri_matrix[slice_x, , ], "Sagittal View", "./Project/ADNI/result/MRI/sagittal_view.pdf")
# Coronal View
plot_slice(mri_matrix[, slice_y, ], "Coronal View", "./Project/ADNI/result/MRI/coronal_view.pdf")
# Axial View
plot_slice(mri_matrix[, , slice_z], "Axial View", "./Project/ADNI/result/MRI/axial_view.pdf")

# Histogram of MRI Intensity Values
pdf("./Project/ADNI/result/MRI/mri_intensity_histogram.pdf", width = 8, height = 6)
p <-
    ggplot2::ggplot(data.frame(value = as.vector(mri_matrix)), ggplot2::aes(x = value)) +
    ggplot2::geom_histogram(bins=100, fill="blue", alpha=0.7) +
    ggplot2::xlab("Voxel Intensity") +
    ggplot2::ylab("Frequency") +
    ggplot2::ggtitle("Histogram of MRI Intensity Values") +
    ggplot2::theme_minimal()
print(p)
invisible(dev.off())
