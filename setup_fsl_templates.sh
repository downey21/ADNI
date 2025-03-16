#!/bin/bash

# FSL Standard Template Setup Script
# This script downloads standard MNI templates for FSL and places them in the appropriate directory.

# Define FSL directory
FSLDIR=${FSLDIR:-/usr/lib/fsl/5.0}

# Create the standard template directory
mkdir -p $FSLDIR/data/standard/
cd $FSLDIR/data/standard/

# Download FSL standard MNI templates
wget -O /usr/lib/fsl/5.0/data/standard/MNI152_T1_2mm_brain.nii.gz \
    https://git.fmrib.ox.ac.uk/fsl/data_standard/-/raw/master/MNI152_T1_2mm_brain.nii.gz?ref_type=heads&inline=false

wget -O /usr/lib/fsl/5.0/data/standard/MNI152_T1_2mm.nii.gz \
    https://git.fmrib.ox.ac.uk/fsl/data_standard/-/raw/master/MNI152_T1_2mm.nii.gz?ref_type=heads&inline=false

wget -O /usr/lib/fsl/5.0/data/standard/MNI152_T1_1mm_brain.nii.gz \
    https://git.fmrib.ox.ac.uk/fsl/data_standard/-/raw/master/MNI152_T1_1mm_brain.nii.gz?ref_type=heads&inline=false

wget -O /usr/lib/fsl/5.0/data/standard/MNI152_T1_1mm.nii.gz \
    https://git.fmrib.ox.ac.uk/fsl/data_standard/-/raw/master/MNI152_T1_1mm.nii.gz?ref_type=heads&inline=false

# Verify the downloaded files
ls -l $FSLDIR/data/standard/

echo "FSL standard templates have been downloaded successfully!"
