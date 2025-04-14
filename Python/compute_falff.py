
# -*- coding: utf-8 -*-

import nibabel as nib
import numpy as np
import os

def compute_falff(nifti_file, output_path=None, low_freq=0.01, high_freq=0.1):
    """
    Calculate fALFF map from a 4D NIfTI file and save as a 3D NIfTI file.

    Parameters:
    - nifti_file: path to the preprocessed (but not bandpass filtered) 4D fMRI NIfTI file
    - output_path: directory where the output NIfTI will be saved. 
                   If None, saves to the same directory as nifti_file.
    - low_freq: lower bound of low-frequency band (Hz)
    - high_freq: upper bound of low-frequency band (Hz)
    """
    # Load NIfTI
    img = nib.load(nifti_file)
    data = img.get_fdata()
    
    # Automatically get TR from header
    tr = img.header.get_zooms()[3]
    print(f"Detected TR from NIfTI header: {tr} seconds")

    # Sampling frequency
    fs = 1.0 / tr
    n_timepoints = data.shape[-1]
    freqs = np.fft.fftfreq(n_timepoints, d=tr)

    # Create frequency mask
    low_freq_mask = (np.abs(freqs) >= low_freq) & (np.abs(freqs) <= high_freq)

    # Pre-allocate fALFF output
    falff_map = np.zeros(data.shape[:-1])

    # Loop over voxels
    for x in range(data.shape[0]):
        for y in range(data.shape[1]):
            for z in range(data.shape[2]):
                timeseries = data[x, y, z, :]
                if np.all(timeseries == 0):
                    continue

                # FFT
                fft_values = np.abs(np.fft.fft(timeseries))

                # fALFF calculation
                low_freq_power = np.sum(fft_values[low_freq_mask])
                total_power = np.sum(fft_values[freqs >= 0]) # Only positive frequencies
                if total_power > 0:
                    falff_map[x, y, z] = low_freq_power / total_power

    # Determine output path
    input_dir = os.path.dirname(nifti_file)
    input_filename = os.path.basename(nifti_file)
    output_dir = output_path if output_path is not None else input_dir
    output_filename = "falff_" + input_filename
    output_full_path = os.path.join(output_dir, output_filename)

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save the fALFF map
    falff_img = nib.Nifti1Image(falff_map, affine=img.affine, header=img.header)
    nib.save(falff_img, output_full_path)
