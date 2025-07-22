import mne
import matplotlib.pyplot as plt
import warnings
import os
import glob
from pathlib import Path

def read_edf_duration_only(file_path):
    """Read EDF file and return duration without plotting"""
    try:
        # Load the EDF file
        raw = mne.io.read_raw_edf(file_path, preload=False, verbose=False)
        
        # Get the duration of the recording
        duration = raw.times[-1]
        
        return duration, True, None
    except Exception as e:
        return 0, False, str(e)

def count_total_edf_duration(folder_path):
    """
    Iterate through folder and count total recording duration from all .edf files
    
    Parameters:
    folder_path (str): Path to the folder containing .edf files
    """
    
    # Find all .edf files in the folder
    edf_files = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.edf'):
                edf_files.append(os.path.join(root, file))
    
    if not edf_files:
        print(f"No .edf files found in {folder_path}")
        return
    
    total_duration = 0
    successful_files = []
    failed_files = []
    
    print(f"Found {len(edf_files)} .edf files to process...")
    print("=" * 80)
    
    for file_path in edf_files:
        filename = os.path.basename(file_path)
        
        # Read duration from EDF file
        duration, success, error = read_edf_duration_only(file_path)
        
        if success:
            total_duration += duration
            successful_files.append((filename, duration))
            print(f"✓ {filename:<40} | {duration:>8.2f}s | {duration/60:>6.2f}m")
        else:
            failed_files.append((filename, error))
            print(f"✗ {filename:<40} | Failed: {error}")
    
    # Print detailed summary
    print("=" * 80)
    print(f"DURATION SUMMARY:")
    print(f"Successfully processed: {len(successful_files)} files")
    print(f"Failed to process: {len(failed_files)} files")
    print(f"Total recording duration: {total_duration:.2f} seconds")
    print(f"Total recording duration: {total_duration/60:.2f} minutes")
    print(f"Total recording duration: {total_duration/3600:.2f} hours")
    
    if len(successful_files) > 0:
        avg_duration = total_duration / len(successful_files)
        print(f"Average duration per file: {avg_duration:.2f} seconds ({avg_duration/60:.2f} minutes)")
    
    # Show longest and shortest recordings
    if successful_files:
        successful_files.sort(key=lambda x: x[1], reverse=True)
        print(f"\nLongest recording: {successful_files[0][0]} ({successful_files[0][1]:.2f}s)")
        print(f"Shortest recording: {successful_files[-1][0]} ({successful_files[-1][1]:.2f}s)")
    
    if failed_files:
        print(f"\nFailed files:")
        for filename, error in failed_files:
            print(f"  ✗ {filename}: {error}")
    
    return {
        'total_duration_seconds': total_duration,
        'total_duration_minutes': total_duration/60,
        'total_duration_hours': total_duration/3600,
        'successful_files': successful_files,
        'failed_files': failed_files,
        'file_count': len(successful_files)
    }

def read_edf_with_details(file_path):
    """Your original read_edf function for detailed analysis"""
    # Load the EDF file
    raw = mne.io.read_raw_edf(file_path, preload=True)
    
    # Print basic information about the data
    print("Info:")
    print(raw.info)

    # Plot the raw data
    fig1 = raw.plot(title="Raw EEG Data")
    
    # Get the duration of the recording
    duration = raw.times[-1]
    print(f"Recording duration: {duration:.2f} seconds")

    # Get the channel names
    channels = raw.ch_names
    print(f"Channels: {channels}")

    # Filter to only standard EEG channels, excluding problematic channels
    eeg_channels = [ch for ch in raw.ch_names if any(eeg_name in ch.upper() for eeg_name in ['FP1', 'FP2', 'F3', 'F4', 'C3', 'C4', 'P3', 'P4', 'O1', 'O2', 'F7', 'F8', 'T3', 'T4', 'T5', 'T6', 'FZ', 'CZ', 'PZ']) and ch not in ['SpO2', 'EtCO2', 'Pulse', 'CO2Wave', 'DC03', 'DC04', 'DC05', 'DC06']]

    if eeg_channels:
        raw_eeg = raw.copy().pick(eeg_channels)
        # Compute and plot the power spectral density for EEG channels only
        fig2 = raw_eeg.compute_psd().plot()
        fig2.suptitle("Power Spectral Density (EEG Channels)")
    else:
        # Fallback to all channels if no standard EEG channels found
        fig2 = raw.compute_psd().plot()
        fig2.suptitle("Power Spectral Density")
    
    # Save figures
    fig2.savefig('power_spectral_density.png', dpi=300, bbox_inches='tight')
    
    # Save all matplotlib figures
    for i, fig_num in enumerate(plt.get_fignums()):
        fig = plt.figure(fig_num)
        fig.savefig(f'eeg_figure_{i+1}.png', dpi=300, bbox_inches='tight')
    
    print("Figures saved as PNG files")
    
    return raw

# Example usage
if __name__ == "__main__":
    # Suppress warnings
    warnings.filterwarnings("ignore", message="Channel locations not available")
    
    # Count total duration from all EDF files
    eeg_folder = "./EEG2100"
    results = count_total_edf_duration(eeg_folder)
    
    # Optionally, analyze a specific file in detail
    # edf_file_path = "/mnt/disk2/pqhung/EEG/EEG/FA5551T1_1-1+.edf"
    # raw_data = read_edf_with_details(edf_file_path)
    # plt.show()