#!/bin/bash

# ANTs Installation Script
# This script downloads, installs ANTs, sets up environment variables, and removes installation files.

# Define installation directory
ANTS_DIR="$HOME/ants-2.5.4"

# Download ANTs binary package
wget -O ants.zip https://github.com/ANTsX/ANTs/releases/download/v2.5.4/ants-2.5.4-ubuntu-20.04-X64-gcc.zip

# Extract the package
unzip ants.zip -d $HOME

# Set up environment variables
# echo "export ANTSPATH=$ANTS_DIR/bin" >> ~/.bashrc
# echo "export PATH=\$ANTSPATH:\$PATH" >> ~/.bashrc
# echo "export LD_LIBRARY_PATH=$ANTS_DIR/lib:\$LD_LIBRARY_PATH" >> ~/.bashrc

# Function to safely add an environment variable to ~/.bashrc
add_to_bashrc() {
    local VAR_NAME="$1"
    local VAR_VALUE="$2"
    local EXPORT_CMD="export $VAR_NAME=$VAR_VALUE"

    if ! grep -q "$EXPORT_CMD" ~/.bashrc; then
        echo "$EXPORT_CMD" >> ~/.bashrc
    fi
}

# Add ANTs environment variables only if they don't exist in ~/.bashrc
add_to_bashrc "ANTSPATH" "$ANTS_DIR/bin"
add_to_bashrc "PATH" "\$ANTSPATH:\$PATH"
add_to_bashrc "LD_LIBRARY_PATH" "$ANTS_DIR/lib:\$LD_LIBRARY_PATH"

# Apply changes immediately
# source ~/.bashrc

# Remove installation zip file
rm ants.zip

# Verify installation
echo "ANTs installation complete! Run 'which N4BiasFieldCorrection' and 'N4BiasFieldCorrection --version' to verify."
