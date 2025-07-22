#!/bin/bash
# filepath: /mnt/disk2/pqhung/EEG/bash.sh

# Navigate to the EEG folder
cd ./EEG2100

# Create folders and move files/directories
for item in *; do
    # Skip if item doesn't exist
    [ ! -e "$item" ] && continue
    
    # Extract basename without extension (everything before last dot)
    basename="${item%.*}"
    
    # Skip if basename is empty or same as item (no extension)
    [ -z "$basename" ] || [ "$basename" = "$item" ] && continue
    
    # Create directory if it doesn't exist
    mkdir -p "$basename"
    
    # Move file or directory to the target directory
    mv "$item" "$basename/"
    echo "Moved: $item -> $basename/"
done

echo "Files and folders grouped by basename into folders"