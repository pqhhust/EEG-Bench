#!/bin/bash
# filepath: /mnt/disk2/pqhung/EEG/convert_all_eeg.sh

# Find and convert all .eeg files recursively
find ./EEG2100 -type f \( -name "*.eeg" -o -name "*.EEG" \) -exec bash -c '
    for file; do
        echo "Converting: $file"
        ./nk2edf_ver15_source/nk2edf "$file"
        if [ $? -eq 0 ]; then
            echo "  ✓ Success: $(basename "$file")"
        else
            echo "  ✗ Error converting: $(basename "$file")"
        fi
    done
' bash {} +

echo "Conversion completed!"