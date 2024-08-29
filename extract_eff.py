import uproot
import os
import pandas as pd
from argparse import ArgumentParser
import numpy as np
from statsmodels.stats.weightstats import DescrStatsW

def parse_args():
    """Parse command line arguments."""
    parser = ArgumentParser(description='Crawl root files')
    add_arg = parser.add_argument
    add_arg('-s', '--start', type=int, default=1, help='Start run')
    add_arg('-e', '--end', type=int, default=1500, help='End run')
    add_arg('-p', '--path', type=str, default='Plotter/', help='Path to root files')

    return parser.parse_args()

def extract_plotter_run_files(path):
    file_list = []
    for filename in os.listdir(path):
        if filename.startswith("Plotter-run") and filename.endswith(".root"):
            file_list.append(os.path.join(path, filename))
    #print(file_list)
    return file_list

def extract_runs_from_files(file_list):
    runs = []
    for filename in file_list:
        parts = filename.split("-")
        #print(parts)
        for part in parts:
            if part.startswith("run") and part[3:9].isdigit():
                runs.append(int(part[3:9]))
                #print(int(part[3:9]))
                break
    return runs

def extract_and_add_to_dataframe(file_list):
    columns = ['start_col', 'stop_col', 'start_row', 'stop_row']
    result_df = pd.DataFrame(columns=columns)

    runs = extract_runs_from_files(file_list)

    data_to_concat = []

    for filename in file_list:
        parts = filename.split("-")
        for i, part in enumerate(parts):
            if part.isdigit() and len(parts) >= i + 4:
                start_col = int(parts[i])
                stop_col = int(parts[i + 1])
                start_row = int(parts[i + 2])
                stop_row = int(parts[i + 3].split("_")[0].split(".")[0])

                row_data = {
                    'start_col': start_col,
                    'stop_col': stop_col,
                    'start_row': start_row,
                    'stop_row': stop_row
                }

                data_to_concat.append(row_data)
                break

    if data_to_concat:
        df_to_add = pd.DataFrame(data_to_concat)
        result_df = pd.concat([result_df, df_to_add], ignore_index=True)

    result_df.index = runs
    return result_df

def extract_pointing(file_list, key, error=False, asym=False, entrie = False, mean = False):
    pointing = []
    for file in file_list:
        try:
            file_name = uproot.open(file)
            if entrie:
                values_array = file_name[key].counts()
                values_array = [np.sum(values_array)]
                #print((values_array))
            elif mean:
                #values = file_name[key].values()
                N1, N2 = file_name[key].to_numpy()
                if error:
                    values_array=DescrStatsW(N2[:-1], weights=N1, ddof=1).std_mean
                else:
                    values_array=np.average(N2[:-1], weights=N1) 

            elif error:
                if asym:
                    values_array1 = file_name[key].errors('low', axis='y')
                    values_array2 = file_name[key].errors('high', axis='y')
                    values_array = [values_array1, values_array2]
                    #print((values_array))
                else:
                    values_array = file_name[key].errors()
            else:
                values_array = file_name[key].values()
                #print(len(values_array)) 
            if isinstance(values_array, float):
                pointing.append(values_array)
            else:
                if len(values_array) == 3:
                    pointing.append(values_array.tolist())
                elif len(values_array) == 2:
                    pointing.append(values_array)
                else:
                    pointing.append(values_array)
        except Exception as e:
            print(f"Error processing {key}: {str(e)}")
            value = [0]
            pointing.append(value)
    return pointing


if __name__ == '__main__':
    args = parse_args()
    plotter_run_files = extract_plotter_run_files(args.path)

    result_df = extract_and_add_to_dataframe(plotter_run_files)

    result_df['pointing_u'] = extract_pointing(plotter_run_files, "hpoint_resolution_u;1")
    result_df['pointing_v'] = extract_pointing(plotter_run_files, "hpoint_resolution_v;1")
    result_df['pointing_error_u'] = extract_pointing(plotter_run_files, "hpoint_resolution_u;1", error=True)
    result_df['pointing_error_v'] = extract_pointing(plotter_run_files, "hpoint_resolution_v;1", error=True)
    result_df['cluster_size_u_roi'] = extract_pointing(plotter_run_files, "hsizeUroi;1", mean=True)
    result_df['cluster_size_v_roi'] = extract_pointing(plotter_run_files, "hsizeVroi;1", mean=True)
    result_df['cluster_size_u_error_roi'] = extract_pointing(plotter_run_files, "hsizeUroi;1", mean=True, error =True)
    result_df['cluster_size_v_error_roi'] = extract_pointing(plotter_run_files, "hsizeVroi;1", mean=True, error =True)
    result_df['eff_roi'] = extract_pointing(plotter_run_files, "g_efficiency_roi;1")
    result_df['eff_roi_error'] = extract_pointing(plotter_run_files, "g_efficiency_roi;1", error=True, asym=True)
    result_df['h_roi_pass'] = extract_pointing(plotter_run_files, "h_track_pass;3", entrie=True)
    result_df['h_roi_total'] = extract_pointing(plotter_run_files, "h_track_total;3", entrie=True)

    # Perform the division
    result_df['eff'] = result_list = [(x[0] / y[0])*100 if y[0] != 0 else 0 for x, y in zip(result_df['h_roi_pass'], result_df['h_roi_total'])]
    result_df['eff_error'] = result_list = [(np.sqrt(((x[0] / y[0])*(1-(x[0] / y[0])))/y[0]))*100 if y[0] != 0 else 0 for x, y in zip(result_df['h_roi_pass'], result_df['h_roi_total'])]
    result_df = result_df.sort_index()
    result_df.to_csv(os.path.join(args.path, 'results.csv'))
    print('finished! Saved to', os.path.join(args.path, 'results.csv') )

    



    
    
    
    
    
    
    
    
    
    
