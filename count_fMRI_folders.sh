#!/bin/bash

# Set target directory
TARGET_DIR="/node05_storage/ADNI/fMRI/dicom"
OUTPUT_CSV="/home/dhseo/Project/ADNI/folder_counts.csv"

# Count subject folders
SUBJECT_COUNT=$(find "$TARGET_DIR" -mindepth 1 -maxdepth 1 -type d | wc -l)

# Output header
echo "Folder_Name,Count" > "$OUTPUT_CSV"

# Count inner folders and append to CSV
find "$TARGET_DIR" -mindepth 2 -maxdepth 2 -type d \
  | awk -F/ '{print $7}' \
  | sort | uniq -c \
  | sort -nr \
  | awk '{print $2 "," $1}' >> "$OUTPUT_CSV"

# Also print subject count info
echo "Total_Subject_Folders,$SUBJECT_COUNT" >> "$OUTPUT_CSV"

# Confirmation
echo "CSV file saved to: $OUTPUT_CSV"
