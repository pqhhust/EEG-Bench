#!/bin/bash
# filepath: /mnt/disk2/pqhung/EEG/scripts/rename_extensions.sh

# Convert .PNT files to .pnt (lowercase)
find ./EEG -type f -name '*.PNT' -exec bash -c 'for f; do mv "$f" "${f%.PNT}.pnt"; done' bash {} +

# Convert .LOG files to .log (lowercase)
find ./EEG -type f -name '*.LOG' -exec bash -c 'for f; do mv "$f" "${f%.LOG}.log"; done' bash {} +

echo "Renamed all .PNT files to .pnt and .LOG files to .log"