# EEG-Bench: Data Processing Guide

## Data Acquisition
Download the EEG dataset from the following link:  
[EEG2100 Dataset](https://husteduvn-my.sharepoint.com/personal/hieu_pc224848_sis_hust_edu_vn/_layouts/15/onedrive.aspx?ga=1&id=%2Fpersonal%2Fhieu%5Fpc224848%5Fsis%5Fhust%5Fedu%5Fvn%2FDocuments%2FDataset%20108%20for%20EEG%20Foundation%20models%2FEEG2100%2Ezip&parent=%2Fpersonal%2Fhieu%5Fpc224848%5Fsis%5Fhust%5Fedu%5Fvn%2FDocuments%2FDataset%20108%20for%20EEG%20Foundation%20models)

## EDF Converter Setup
To convert raw EEG data into EDF format, download the EDF converter tool from: [nk2edf Converter](https://www.teuniz.net/edf/nk2edf_ver15_source.tar.gz) and run the following command:
```
tar -xvf nk2edf_ver15_source.tar.gz
```

Organize your directory structure as follows:  
```
./
├── EEG2100/
└── nk2edf_ver15_source/
```

Navigate to the `nk2edf_ver15_source` directory and build the EDF converter by executing:  
```bash
bash build.sh
```

## Data Preprocessing
To preprocess the raw EEG data, run the following scripts in sequence:  
```bash
bash scripts/upper_to_lower.sh
bash scripts/group_by_subject.sh
bash scripts/raw_to_edf.sh
```

## Data Exploration
To inspect the processed data, execute the `edf_reader.py` script for detailed information about the dataset.
