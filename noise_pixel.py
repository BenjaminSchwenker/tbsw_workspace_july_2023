import os
import ROOT
import pandas as pd
import re

def extract_run_number_from_path(path):
    match = re.search(r'run(\d+)', path)
    if match:
        return match.group(1)
    else:
        return None

def count_entries_with_value(histogram, value):
    count = 0
    try:

        for bin_x in range(1, histogram.GetNbinsX() + 1):
            for bin_y in range(1, histogram.GetNbinsY() + 1):
                bin_content = histogram.GetBinContent(bin_x, bin_y)
                if bin_content == value:
                    count += 1
        return count
    except:
        return None

def process_folder(folder_path):
    # Extract run number from folder name
    run_number = extract_run_number_from_path(folder_path)

    try:
        # Open the ROOT file
        file_path = os.path.join(folder_path, "NoiseDB-TJ2.root")
        root_file = ROOT.TFile.Open(file_path)

    except:
        print(f"Error: Unable to open file {file_path}")
        return None

    # Access the 2D histogram (heatmap)
    try:
        histogram_name = "hDB_sensor22_mask;1"
        histogram = root_file.Get(histogram_name)

    except:
        print(f"Error: Unable to retrieve histogram {histogram_name}")
        root_file.Close()
        return None

    # Count the number of entries with a value of 1
    value_to_count = 1
    entry_count = count_entries_with_value(histogram, value_to_count)

    # Close the ROOT file
    root_file.Close()

    return run_number, entry_count

def main():
    root_folder = "/media/bgnet/TB2023_TBSW_Data/tbsw_workspace_july_2023/localDB"  # Change this to the root folder containing subfolders

    # Create an empty DataFrame
    columns = ["name_of_subfolder", "runnumber_from_subfolder", "number_of_entries_with_1"]
    df = pd.DataFrame(columns=columns)

    # Iterate through subfolders
    for subfolder in os.listdir(root_folder):
        subfolder_path = os.path.join(root_folder, subfolder)

        if os.path.isdir(subfolder_path):
            result = process_folder(subfolder_path)

            if result:
                run_number, entry_count = result
                df = df.append({"name_of_subfolder": subfolder,
                                "runnumber_from_subfolder": run_number,
                                "number_of_entries_with_1": entry_count}, ignore_index=True)
    # Sort the DataFrame by "runnumber_from_subfolder"
    df.sort_values(by="runnumber_from_subfolder", inplace=True)
    # Save the DataFrame to a CSV file
    df.to_csv("output_dataframe.csv", index=False)

if __name__ == "__main__":
    ROOT.gROOT.SetBatch(ROOT.kTRUE)  # Enable batch mode to suppress graphics
    main()
