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

def parse_args():
    """Parse command line arguments."""
    parser = ArgumentParser(description='Crawl root files')
    add_arg = parser.add_argument
    add_arg('-s', '--start', type=int, default=0, help='Start run')
    add_arg('-e', '--end', type=int, default=1500, help='End run')
    add_arg('-p', '--path', type=str, default='/home/bgnet/tbsw_workspace_july_2023/Plotter_cal/', help='Path to root files')

    return parser.parse_args()

def extract_plotter_run_files(path, start_run, end_run):
    file_list = []
    for filename in os.listdir(path):
        if filename.startswith("Plotter-run") and filename.endswith(".root"):
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
                stop_row = int(parts[i + 3].split(".")[0])

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


def get_chargeMPV(file_list):
    chargeMPV=[]
    for file in file_list:
        directory_path, filename_file = os.path.split(file)
        bin_width=4
        bin_contraction =True
        try:
            file_name = uproot.open(file)
            print('opend filfe')
            x=file_name["hCChargeroi;1"].axis().edges()
            y=file_name["hCChargeroi;1"].values()

            y_new_list=[]
            x_new = []
            for i in range(0,int((len(y)//bin_width)*bin_width),bin_width):
                if bin_width==1:
                    y_new=np.sum(y[i])
                else:
                    y_new=np.sum(y[i:(i+bin_width-1)])
                y_new_list.append(y_new)
                
                x_new.append(i*x[1])
            y_new=np.array(y_new_list)
            x_new=np.array(x_new)

            if bin_contraction == True:
                x=x_new
                y=y_new
            
            yerr=np.sqrt(y)

            d = {'x': x, 'y': y,'yerr': yerr,}
            df = pd.DataFrame(data=d)
            filename =os.path.join(directory_path, 'charge_fit', filename_file + '.csv')
            df.to_csv(filename)

            y_range =0.4
            x_fit=[ n for n,i in enumerate(y) if i>y_range*y.max() ]
            y_fit=[el for el in y if el>y_range* y.max()]
                
            yerr=yerr[x_fit[0]:x_fit[-1]]
            print('pre fit')
            mpv, eta, sigma, A = x[y.argmax()], 10, 40, y.max()
            lower_bounds = [0, 0, 0, 0]
            upper_bounds = [np.inf, np.inf, np.inf, np.inf]
            print('Fir parameter:',mpv, eta, sigma, A)
            try:
                coeff, pcov = curve_fit(pylandau.langau, x[x_fit[0]:x_fit[-1]], y[x_fit[0]:x_fit[-1]],
                                        sigma=yerr,
                                        absolute_sigma=True,
                                        p0=(mpv, eta, sigma, A),
                                        bounds=(lower_bounds, upper_bounds))
                print('hat gefittet')
            except Exception as e:
                print('fit failed:', e)
                coeff = [0,0,0]
                pcov=np.array([[0,0,0],[0,0,0],[0,0,0]])

            fig = plt.figure()
            plt.plot(x,y, marker='o', label='Data Points')
            try:
                x_fit_fine = np.linspace(x[x_fit[0]], x[x_fit[-1]], 1000)
                plt.plot(x_fit_fine, pylandau.langau(x_fit_fine, *coeff),label='fit')
                #plt.plot(x[x_fit[0]:x_fit[-1]], pylandau.langau(np.array(x[x_fit[0]:x_fit[-1]]).astype('float64'), mpv, eta, sigma, A,),label='fot')
            except Exception as e:
                print('excepltion', e)
            plt.legend()
            match = re.search(r'run(\d+)', filename_file)

            if match:
                run_number = match.group(1)
                print("Run Number:", run_number)
            else:
                print("Run number not found in the filename.")
            plt.title('run {}'.format(run_number))
            plt.ylabel('number of clusters')
            plt.xlim([0, 10000])
            plt.xlabel('charge [electron]')
            #plt.show()


            print('determine chi')
            chi=0
            try:
                for n in range(len(pylandau.langau(np.array(x[x_fit[0]:x_fit[-1]]).astype('float64'), *coeff))):
                   chi+=((y[x_fit[0]:x_fit[-1]+1][n]-pylandau.langau(np.array(x[x_fit[0]:x_fit[-1]]).astype('float64'), *coeff)[n])/np.sqrt(y[x_fit[0]:x_fit[-1]][n]))**2
            except Exception as e:
                print('excepltion', e)        
            print('fine')
            plt.text(0.4, 0.7, 'mpv: {}\nerror: {} \nentries: {}\nchi-sqrt:{}'.format(int(coeff[0]), int(np.sqrt(pcov[0, 0])), int(np.sum(y)), int(chi)), style='italic', fontsize=10, transform=plt.gcf().transFigure)

                  
            print('jetzt nur noch speichern')
            #plt.savefig(path + 'charge_fit/ChargeMPV{}_{}_{}.pdf'.format(instance,args.FrontEnd,prefix), format="pdf", bbox_inches="tight")
            
            output_path_pdf = os.path.join(directory_path, 'charge_fit', filename_file+ '.pdf')
            plt.savefig(output_path_pdf)
            print('plot saved')
            value = [coeff[0],np.sqrt(pcov[0,0])]
            chargeMPV.append(value)
            plt.close()

        except Exception as e:
            print('excepltion', e)
            value = [0,0]
            chargeMPV.append(value)

    return chargeMPV

def get_seedchargeMPV(file_list):
    chargeMPV=[]
    for file in file_list:
        directory_path, filename_file = os.path.split(file)
        bin_width=4
        bin_contraction =True
        try:
            file_name = uproot.open(file)
            print('opend filfe')
            x=file_name["hChargeroi;1"].axis().edges()
            y=file_name["hChargeroi;1"].values()

            y_new_list=[]
            x_new = []
            for i in range(0,int((len(y)//bin_width)*bin_width),bin_width):
                if bin_width==1:
                    y_new=np.sum(y[i])
                else:
                    y_new=np.sum(y[i:(i+bin_width-1)])
                y_new_list.append(y_new)
                
                x_new.append(i*x[1])
            y_new=np.array(y_new_list)
            x_new=np.array(x_new)

            if bin_contraction == True:
                x=x_new
                y=y_new
            
            yerr=np.sqrt(y)

            d = {'x': x, 'y': y,'yerr': yerr,}
            df = pd.DataFrame(data=d)
            filename =os.path.join(directory_path, 'charge_fit', filename_file + '.csv')
            df.to_csv(filename)

            y_range =0.4
            x_fit=[ n for n,i in enumerate(y) if i>y_range*y.max() ]
            y_fit=[el for el in y if el>y_range* y.max()]
                
            yerr=yerr[x_fit[0]:x_fit[-1]]
            print('pre fit')
            mpv, eta, sigma, A = x[y.argmax()], 10, 40, y.max()
            lower_bounds = [0, 0, 0, 0]
            upper_bounds = [np.inf, np.inf, np.inf, np.inf]
            print('Fir parameter:',mpv, eta, sigma, A)
            try:
                coeff, pcov = curve_fit(pylandau.langau, x[x_fit[0]:x_fit[-1]], y[x_fit[0]:x_fit[-1]],
                                        sigma=yerr,
                                        absolute_sigma=True,
                                        p0=(mpv, eta, sigma, A),
                                        bounds=(lower_bounds, upper_bounds))
                print('hat gefittet')
            except Exception as e:
                print('fit failed:', e)
                coeff = [0,0,0]
                pcov=np.array([[0,0,0],[0,0,0],[0,0,0]])

            fig = plt.figure()
            plt.plot(x,y, marker='o', label='Data Points')
            try:
                x_fit_fine = np.linspace(x[x_fit[0]], x[x_fit[-1]], 1000)
                plt.plot(x_fit_fine, pylandau.langau(x_fit_fine, *coeff),label='fit')
                #plt.plot(x[x_fit[0]:x_fit[-1]], pylandau.langau(np.array(x[x_fit[0]:x_fit[-1]]).astype('float64'), mpv, eta, sigma, A,),label='fot')
            except Exception as e:
                print('excepltion', e)
            plt.legend()
            match = re.search(r'run(\d+)', filename_file)

            if match:
                run_number = match.group(1)
                print("Run Number:", run_number)
            else:
                print("Run number not found in the filename.")
            plt.title('run {}'.format(run_number))
            plt.ylabel('number of seed')
            plt.xlim([0, 10000])
            plt.xlabel('charge [electron]')
            #plt.show()


            print('determine chi')
            chi=0
            try:
                for n in range(len(pylandau.langau(np.array(x[x_fit[0]:x_fit[-1]]).astype('float64'), *coeff))):
                   chi+=((y[x_fit[0]:x_fit[-1]+1][n]-pylandau.langau(np.array(x[x_fit[0]:x_fit[-1]]).astype('float64'), *coeff)[n])/np.sqrt(y[x_fit[0]:x_fit[-1]][n]))**2
            except Exception as e:
                print('excepltion', e)        
            print('fine')
            plt.text(0.4, 0.7, 'mpv: {}\nerror: {} \nentries: {}\nchi-sqrt:{}'.format(int(coeff[0]), int(np.sqrt(pcov[0, 0])), int(np.sum(y)), int(chi)), style='italic', fontsize=10, transform=plt.gcf().transFigure)

                  
            print('jetzt nur noch speichern')
            #plt.savefig(path + 'charge_fit/ChargeMPV{}_{}_{}.pdf'.format(instance,args.FrontEnd,prefix), format="pdf", bbox_inches="tight")
            
            output_path_pdf = os.path.join(directory_path, 'charge_fit', filename_file+ '.pdf')
            plt.savefig(output_path_pdf)
            print('plot saved')
            value = [coeff[0],np.sqrt(pcov[0,0])]
            chargeMPV.append(value)
            plt.close()

        except Exception as e:
            print('excepltion', e)
            value = [0,0]
            chargeMPV.append(value)

    return chargeMPV




if __name__ == '__main__':
    args = parse_args()
    plotter_run_files = extract_plotter_run_files(args.path, args.start, args.end)

    result_df = extract_and_add_to_dataframe(plotter_run_files)

    result_df['pointing_u'] = extract_pointing(plotter_run_files, "hpoint_resolution_u;2")
    result_df['pointing_v'] = extract_pointing(plotter_run_files, "hpoint_resolution_v;2")
    result_df['pointing_error_u'] = extract_pointing(plotter_run_files, "hpoint_resolution_u;2", error=True)
    result_df['pointing_error_v'] = extract_pointing(plotter_run_files, "hpoint_resolution_v;2", error=True)
    result_df['cluster_size'] = extract_pointing(plotter_run_files, "hsize;2", mean=True)
    result_df['cluster_size_u'] = extract_pointing(plotter_run_files, "hsizeU;2", mean=True)
    result_df['cluster_size_v'] = extract_pointing(plotter_run_files, "hsizeV;2", mean=True)
    result_df['cluster_size_u_error'] = extract_pointing(plotter_run_files, "hsizeU;2", mean=True, error =True)
    result_df['cluster_size_v_error'] = extract_pointing(plotter_run_files, "hsizeV;2", mean=True, error =True)
    result_df['cluster_size_roi'] = extract_pointing(plotter_run_files, "hsizeroi;2", mean=True)
    result_df['cluster_size_u_roi'] = extract_pointing(plotter_run_files, "hsizeUroi;2", mean=True)
    result_df['cluster_size_v_roi'] = extract_pointing(plotter_run_files, "hsizeVroi;2", mean=True)
    result_df['cluster_size_u_roi_error'] = extract_pointing(plotter_run_files, "hsizeUroi;2", mean=True, error =True)
    result_df['cluster_size_v_roi_error'] = extract_pointing(plotter_run_files, "hsizeVroi;2", mean=True, error =True)
    result_df['eff_roi'] = extract_pointing(plotter_run_files, "g_efficiency_roi;1")
    result_df['eff_roi_error'] = extract_pointing(plotter_run_files, "g_efficiency_roi;1", error=True, asym=True)
    result_df['h_roi_pass'] = extract_pointing(plotter_run_files, "h_roi_pass;1", entrie=True)
    result_df['h_roi_total'] = extract_pointing(plotter_run_files, "h_roi_total;1", entrie=True)
    result_df['cluster_MPV'] = get_chargeMPV(plotter_run_files)
    result_df['seed_MPV'] = get_seedchargeMPV(plotter_run_files)

    # Perform the division
    result_df['eff'] = result_list = [x[0] / y[0] if y[0] != 0 else 0 for x, y in zip(result_df['h_roi_pass'], result_df['h_roi_total'])]
    result_df['eff_error'] = result_list = [np.sqrt(((x[0] + 1) * (x[0] + 2) / ((y[0] + 2) * (y[0] + 3))) - ((x[0] + 1)**2 / ((y[0] + 2)**2))) if y[0] != 0 else 0 for x, y in zip(result_df['h_roi_pass'], result_df['h_roi_total'])]
    result_df = result_df.sort_index()
    result_df.to_csv(os.path.join(args.path, 'results.csv'))
    print('finished!')