import os
import uproot
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd



def process_and_plot_histogram(file_path, output_folder, csv_filename):
    try:
        # Open the ROOT file
        with uproot.open(file_path) as file:
            # Access the 'Event' tree inside the file
            tree = file["Event"]

            # Get the arrays of relevant columns for all events
            data = tree.arrays(["nDutDigits", "nTelTracks", "iRun"], library="np")

            # Filter events where nTelTracks == 0
            filtered_data = {key: value[data["nTelTracks"] == 0] for key, value in data.items()}

            # Plot histogram for nDutDigits
            plt.hist(data["nDutDigits"], bins=50, range=(0, 50), alpha=0.7, color='blue', edgecolor='black', label='All Events')
            plt.hist(filtered_data["nDutDigits"], bins=50, range=(0, 50), alpha=0.7, color='orange', edgecolor='black', label='Filtered Events')
            plt.xlabel('nDutDigits')
            plt.ylabel('Frequency')
            plt.title(f'Histogram of nDutDigits for All and Filtered Events (nTelTracks == 0)')
            plt.legend()

            # Find the x position of the maximum in the histogram
            histogram_all, bin_edges_all = np.histogram(data["nDutDigits"], range=(0, 50), bins=50)
            histogram_filtered, bin_edges_filtered = np.histogram(filtered_data["nDutDigits"], range=(0, 50), bins=50)

            max_bin_index_all = np.argmax(histogram_all)
            bin_centers_all = (bin_edges_all[:-1] + bin_edges_all[1:]) / 2
            mean_all = np.average(bin_centers_all, weights=histogram_all)
            std_all = np.sqrt(np.average((bin_centers_all - mean_all)**2, weights=histogram_all))
            max_x_position_all = bin_centers_all[max_bin_index_all]
            max_bin_index_all_excluded = np.argmax(histogram_all[1:]) + 1  # Exclude the first bin
            max_x_position_all_excluded = bin_centers_all[max_bin_index_all_excluded]


            max_bin_index_filtered = np.argmax(histogram_filtered)
            bin_centers_filtered = (bin_edges_filtered[:-1] + bin_edges_filtered[1:]) / 2
            mean_filtered = np.average(bin_centers_filtered, weights=histogram_filtered)
            std_filtered = np.sqrt(np.average((bin_centers_filtered - mean_filtered)**2, weights=histogram_filtered))
            max_x_position_filtered = bin_centers_filtered[max_bin_index_filtered]
            max_bin_index_filtered_excluded = np.argmax(histogram_filtered[1:]) + 1  # Exclude the first bin
            max_x_position_filtered_excluded = bin_centers_filtered[max_bin_index_filtered_excluded]


            plt.text(0.5, 0.7, f'Max (All Events): {max_x_position_all:.2f}\nMean (All Events): {mean_all:.2f}± {std_all:.2f}', transform=plt.gca().transAxes, ha='left', va='bottom', color='blue')
            plt.text(0.5, 0.6, f'Max (Filtered Events): {max_x_position_filtered:.2f}\nMean (Filtered Events): {mean_filtered:.2f}± {std_filtered:.2f}', transform=plt.gca().transAxes, ha='left', va='bottom', color='orange')

            # Save the plot with the corresponding filename in the output folder
            output_filename = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(file_path))[0]}_nDutDigits_filtered.pdf")
            plt.savefig(output_filename)
            plt.close()

            #print(f"Plot saved as: {output_filename}")
            #print(f"The x position of the maximum for All Events is: {max_x_position_all:.2f}")
            #print(f"The x position of the maximum for Filtered Events is: {max_x_position_filtered:.2f}")

            # Write max_x_position_all and max_x_position_filtered to CSV
            run_number = int(os.path.splitext(os.path.basename(file_path))[0].split("-run")[1][:6])
            data_dict = {
                "RunNumber": run_number,
                "MaxPositionAll": max_x_position_all,
                "MaxPositionFiltered": max_x_position_filtered,
                "MaxPosition[1:]All": max_x_position_all_excluded,
                "MaxPosition[1:]Filtered": max_x_position_filtered_excluded,
                "MeanAll": mean_all,
                "STDMeanAll": std_all,
                "MeanFiltered": mean_filtered,
                "STDMeanFiltered": std_filtered,
            }
            df = pd.DataFrame(data_dict, index=[0])

            if not os.path.isfile(csv_filename):
                # If the CSV file doesn't exist, create it with header
                df.to_csv(csv_filename, index=False, mode='w')
            else:
                # If the CSV file exists, append to it without writing header
                df.to_csv(csv_filename, index=False, mode='a', header=False)

            #print(f"Max positions written to CSV: {csv_filename}")

    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")
        pass

def process_all_files_in_folder(input_folder, output_folder, csv_filename):
    # Get all files in the input folder with the .root extension
    root_files = [f for f in os.listdir(input_folder) if f.endswith(".root")]

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    for root_file in root_files:
        file_path = os.path.join(input_folder, root_file)
        result = process_and_plot_histogram(file_path, output_folder, csv_filename)


if __name__ == "__main__":
    input_folder_path = "/media/bgnet/TB2023_TBSW_Data/tbsw_workspace_july_2023/root-files"  # Replace with the path to your folder containing ROOT files
    output_folder_path = "/media/bgnet/TB2023_TBSW_Data/tbsw_workspace_july_2023/nDutDigits_clustDB_1000000ev"  # Replace with the desired path for the output folder
    csv_filename = "/media/bgnet/TB2023_TBSW_Data/tbsw_workspace_july_2023/nDutDigits_clustDB_1000000ev/max_positions.csv"  # Replace with the desired path for the CSV file
    
    # Check if the file exists
    if os.path.isfile(csv_filename):
        # If the file exists, delete it
        os.remove(csv_filename)
        print(f"Existing file deleted: {csv_filename}")
    process_all_files_in_folder(input_folder_path, output_folder_path, csv_filename)
