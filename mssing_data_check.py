import os
import pandas as pd
import re
import subprocess

def get_run_number(file_name):
    # Extracts the run number from the file name
    parts = re.split('-|_', file_name)
    for part in parts:
        if part.startswith('run'):
            return int(part[3:])
    return None

def find_missing_runs(folder_path, csv_path):
    # Get all file names in the specified folder
    files = os.listdir(folder_path)

    # Filter files to only include those matching the specified pattern
    run_numbers = [get_run_number(file) for file in files if "Histos-TJ2" in file and file.endswith("_cal-reco.root")]

    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_path)

    # Extract the run numbers from the DataFrame
    csv_run_numbers = df['runno'].tolist()

    # Find missing run numbers
    missing_runs = set(csv_run_numbers) - set(run_numbers)
    sorted_missing_runs = sorted(missing_runs)

    # Print the missing run numbers
    if missing_runs:
        print("Missing runs:")
        for run in sorted_missing_runs:
            print(f"Run {run}")
            # Run the script for each missing run
            script_command = f"python3 scan_runs.py --start {run} --stop {run}"
            subprocess.run(script_command, shell=True)
    else:
        print("No missing runs.")

if __name__ == "__main__":
    # Specify the folder path and CSV file path
    folder_path = "root-files"
    csv_path = "runDB_calib.csv"

    # Call the function to find and print missing runs
    find_missing_runs(folder_path, csv_path)
