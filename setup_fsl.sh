#!/bin/bash

# FSL Environment Setup Script
# This script adds FSL to the environment variables and makes the changes permanent.

# find /usr -name "bet" 2>/dev/null

# Define FSL installation path
FSLDIR=/usr/lib/fsl/5.0

# Add FSL to the environment variables
# echo "export FSLDIR=$FSLDIR" >> ~/.bashrc
# echo "export PATH=\$FSLDIR:\$PATH" >> ~/.bashrc
# echo "export FSLOUTPUTTYPE=NIFTI_GZ" >> ~/.bashrc
# echo "export LD_LIBRARY_PATH=\$FSLDIR:\$FSLDIR/bin:\$LD_LIBRARY_PATH" >> ~/.bashrc

# Function to safely add an environment variable to ~/.bashrc
add_to_bashrc() {
    local VAR_NAME="$1"
    local VAR_VALUE="$2"
    local EXPORT_CMD="export $VAR_NAME=$VAR_VALUE"

    if ! grep -q "$EXPORT_CMD" ~/.bashrc; then
        echo "$EXPORT_CMD" >> ~/.bashrc
    fi
}

# Add FSL environment variables only if they don't exist in ~/.bashrc
add_to_bashrc "FSLDIR" "$FSLDIR"
add_to_bashrc "PATH" "\$FSLDIR:\$PATH"
add_to_bashrc "FSLOUTPUTTYPE" "NIFTI_GZ"
add_to_bashrc "LD_LIBRARY_PATH" "\$FSLDIR:\$FSLDIR/bin:\$LD_LIBRARY_PATH"

# Create the bin directory if it doesn't exist
mkdir -p /usr/lib/fsl/5.0/bin

# Create symbolic links for executables
ln -s /usr/lib/fsl/5.0/* /usr/lib/fsl/5.0/bin/

# Register the library path
echo "/usr/lib/fsl/5.0" | tee /etc/ld.so.conf.d/fsl.conf > /dev/null
ldconfig

# Ensure FSL startup script is sourced in .bashrc
if ! grep -q "source /etc/fsl/fsl.sh" ~/.bashrc; then
    echo "source /etc/fsl/fsl.sh" >> ~/.bashrc
fi

# Apply changes immediately
# source ~/.bashrc

# Verify installation
echo "FSL environment setup complete! Run 'which bet' and 'bet --version' to verify."
