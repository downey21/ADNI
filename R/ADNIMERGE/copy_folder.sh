#!/bin/bash

src_root="/node05_storage/ADNI/fMRI/dicom"
dst_root="/node05_storage/ADNI/Axial_rsfMRI__Eyes_Open_/dicom"
csv_file="/home/dhseo/Project/ADNI/result/ptid_date_list.csv"

count=0

while IFS=, read -r PTID DATE; do
    # Skip header
    [[ "$PTID" == "PTID" ]] && continue

    src_folder="${src_root}/${PTID}/Axial_rsfMRI__Eyes_Open_"
    dst_folder="${dst_root}/${PTID}/Axial_rsfMRI__Eyes_Open_"

    # Search for subfolder containing the date
    for folder in "$src_folder"/*"$DATE"*; do
        if [ -d "$folder" ]; then
            mkdir -p "$dst_folder"
            rsync -av --ignore-existing "$folder" "$dst_folder/"
            ((count++))
        fi
    done
done < "$csv_file"

echo "Total copied: $count"
