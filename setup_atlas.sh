#!/bin/bash

# Set atlas directory
ATLAS_DIR="/root/Project/ADNI/atlas"

# AAL

# https://www.gin.cnrs.fr/en/tools/aal/
# https://search.kg.ebrains.eu/instances/Dataset/f8758eda-483e-45fe-8a88-a1fc806dde18

AAL_FOLDER="$ATLAS_DIR/aal_for_SPM12"
AAL_ZIP_URL="https://object.cscs.ch/v1/AUTH_4791e0a3b3de43e2840fe46d9dc2b334/ext-d000035_AAL1Atlas_pub/Release2018_SPM12/aal_for_SPM12.zip"
AAL_ZIP_FILE="$ATLAS_DIR/aal_for_SPM12.zip"

# Create atlas directory if it doesn't exist
mkdir -p "$ATLAS_DIR"

# Check if folder exists
if [ -d "$AAL_FOLDER" ]; then
    echo "AAL atlas already exists at $AAL_FOLDER. Skipping download."
else
    echo "Downloading AAL atlas..."
    mkdir -p "$ATLAS_DIR"
    wget -O "$AAL_ZIP_FILE" "$AAL_ZIP_URL"

    echo "Unzipping..."
    unzip "$AAL_ZIP_FILE" -d "$ATLAS_DIR"

    echo "Cleaning up zip file..."
    rm "$AAL_ZIP_FILE"
fi

# Clean up __MACOSX directory if it exists
MACOSX_DIR="$ATLAS_DIR/__MACOSX"
if [ -d "$MACOSX_DIR" ]; then
    echo "Removing macOS metadata folder: $MACOSX_DIR"
    rm -rf "$MACOSX_DIR"
fi

echo "AAL atlas is ready at $AAL_FOLDER"
