import uproot
import os
import pandas as pd
from argparse import ArgumentParser
import numpy as np
from statsmodels.stats.weightstats import DescrStatsW
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pylandau
import re
import awkward as ak

def parse_args():
    """Parse command line arguments."""
    parser = ArgumentParser(description='Crawl root files')
    add_arg = parser.add_argument
    add_arg('-s', '--start', type=int, default=0, help='Start run')
    add_arg('-e', '--end', type=int, default=1500, help='End run')
    add_arg('-p', '--path', type=str, default='/home/bgnet/tbsw_workspace_july_2023/root-files/', help='Path to root files')

    return parser.parse_args()

def extract_plotter_run_files(path, start_run, end_run):
    file_list = []
    for filename in os.listdir(path):
        if filename.startswith("Histos-TJ2") and filename.endswith(".root"):
            # Check if the file name contains "_cal"
            if "_cal" in filename:
                continue  # Skip the file if it contains "_cal"

            match = re.search(r'run(\d+)', filename)
            if match:
                run_number = int(match.group(1))
                if start_run <= run_number <= end_run:
                    file_list.append(os.path.join(path, filename))
    return file_list

def extract_runs_from_files(file_list):
    runs = []
    for filename in file_list:
        parts = filename.split("-")
        for part in parts:
            if part.startswith("run") and part[3:].isdigit():
                runs.append(int(part[3:]))
                break
    return runs


def get_chargeMPV(file_list):
    chargeMPV=[]
    for file in file_list:
        directory_path, filename_file = os.path.split(file)
        try:
            file_name = uproot.open(file)
            #print('opend filfe')

            keys = file_name.keys()
            tree = file_name["Event;1"]
            nDutDigits_branch = tree["nDutDigits"]

            histogram_data = nDutDigits_branch.array(library="np")
            bin_heights, bin_edges = np.histogram(histogram_data, bins='auto')

            max_value = np.max(bin_heights)
            max_position = np.argmax(bin_heights)
            # Find the corresponding position in bin_edges
            corresponding_bin_edge = bin_edges[1:][max_position]

            value = float(corresponding_bin_edge)
            chargeMPV.append(value)

        except Exception as e:
            print('excepltion', e)
            value = float(0)
            chargeMPV.append(value)

    return chargeMPV



if __name__ == '__main__':
    args = parse_args()

    plotter_run_files = extract_plotter_run_files(args.path, args.start, args.end)
    result_df = pd.DataFrame(data={'MPV': get_chargeMPV(plotter_run_files)}, index=extract_runs_from_files(plotter_run_files))

    result_df = result_df.sort_index()
    result_df.to_csv(os.path.join(args.path, 'results.csv'))
    print('finished!')