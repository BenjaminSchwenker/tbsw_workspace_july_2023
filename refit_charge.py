import ROOT
import pandas as pd
from argparse import ArgumentParser
import pylandau
from scipy.optimize import curve_fit
import uproot
import os

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import re





selected_keys = {
"hres_u_all":'RMS+Mean',
"hres_v_all":'RMS+Mean',
"hfit_sigma_u":'RMS+Mean',
"hfit_sigma_v":'RMS+Mean',
"hsizeU":'RMS+Mean',
"hsizeV":'RMS+Mean',
#"g_efficiency":'RMS+Mean',
}

def parse_args():
    """Parse command line arguments."""
    parser = ArgumentParser(description='Crawl root files')
    add_arg = parser.add_argument
    add_arg('-s', '--start', type=int, default=1, help='run')
    add_arg('-p', '--path', type=str, default='/home/bgnet/tbsw_workspace_july_2023/Plotter_cal/', help='Path to root files')
    add_arg('-bs', '--binseed', type=int, default=1, help='binwidth for fitting')
    add_arg('-bc', '--bincluster', type=int, default=1, help='binwidth for fitting')
    add_arg('-rs', '--rangeseed', type=float, default=0.5, help='percent cut for range determination')
    add_arg('-rc', '--rangecluster', type=float, default=0.5, help='percent cut for range determination')
    return parser.parse_args()

def weighted_average_m1(distribution, weights):
  
    numerator = sum([distribution[i]*weights[i] for i in range(len(distribution))])
    denominator = sum(weights)
    
    return round(numerator/denominator,2)

def extract_plotter_run_files(path, start_run):
    file_list = []
    for filename in os.listdir(path):
        if filename.startswith("Plotter-run") and filename.endswith(".root"):
            match = re.search(r'run(\d+)', filename)
            if match:
                run_number = int(match.group(1))
                if start_run <= run_number <= start_run:
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



def get_chargeMPV(file_list):
    print('say something')
    bin_width = args.bincluster
    bin_contraction = True
    chargeMPV=[]
    for file in file_list:
        directory_path, filename_file = os.path.split(file)
        bin_width=args.bincluster
        bin_contraction =True
        try:
            file_name = uproot.open(file)
            print('opend filfe')
            x=file_name["hCChargeroi;1"].axis().edges()
            y=file_name["hCChargeroi;1"].values()

            y_new_list=[]
            x_new = []

            for i in range(0, int((len(y) // bin_width) * bin_width), bin_width):
                if bin_width == 1:
                    y_new = np.sum(y[i])
                else:
                    y_new = np.sum(y[i:(i + bin_width - 1)])
                y_new_list.append(y_new)
                x_new.append(i * x[1])

            y_new = np.array(y_new_list)
            x_new = np.array(x_new)

            if bin_contraction == True:
                x=x_new
                y=y_new
            
            yerr=np.sqrt(y)

            d = {'x': x, 'y': y,'yerr': yerr,}
            df = pd.DataFrame(data=d)
            filename =os.path.join(directory_path, 'charge_fit', filename_file + '.csv')
            df.to_csv(filename)

            x_fit = [n for n, i in enumerate(y) if i > (args.rangecluster * y.max())]
            y_fit = y[x_fit[0]:x_fit[-1] + 1]
                
            yerr=yerr[x_fit[0]:x_fit[-1]]

            # Fit
            mpv, eta, sigma, A = x[y.argmax()], 4, 130, y.max()
            lower_bounds = [0, 0, 0, 0]
            upper_bounds = [np.inf, np.inf, np.inf, np.inf]
            try:
                coeff, pcov = curve_fit(pylandau.langau, x[x_fit[0]:x_fit[-1]], y[x_fit[0]:x_fit[-1]],
                                        sigma=yerr,
                                        absolute_sigma=True,
                                        p0=(mpv, eta, sigma, A),
                                        bounds=(lower_bounds, upper_bounds))
                print('hat gefittet')
                print(coeff)
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
            # Extracting start column, stop column, start row, and stop row
            match_roi = re.search(r'roi-(\d+)-(\d+)-(\d+)-(\d+)', filename)
            if match_roi:
                start_col = match_roi.group(1)
                stop_col = match_roi.group(2)
                start_row = match_roi.group(3)
                stop_row = match_roi.group(4)

                #print("Start Column:", start_col)
                #print("Stop Column:", stop_col)
                #print("Start Row:", start_row)
                #print("Stop Row:", stop_row)
            else:
                print("ROI information not found in the filename.")
            plt.title('run {} CLuster Charge, cols{}-{}'.format(run_number,start_col,stop_col))
            plt.ylabel('number of clusters')
            plt.xlim([0, 10000])
            plt.xlabel('charge [electron]')
            

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
            plt.show()
            plt.close()

            value = [coeff[0], round(np.sqrt(pcov[0, 0]), 5)]
            chargeMPV.append(value)

        except Exception as e:
            print('something failed')
            print(e)
            value = [0, 0]
            chargeMPV.append(value)

    

    csv_file = '/home/bgnet/tbsw_workspace_july_2023/Plotter_cal/results.csv'

    if os.path.isfile(csv_file):
        df_replace = pd.read_csv(csv_file)
        print(df_replace.head(3))
        df_replace.set_index('Unnamed: 0', inplace=True)
        #print("Index:", df_replace.index)
        #print(df_replace.loc[int(run_number)])
        selected_row = df_replace[(df_replace.index == int(run_number)) & (df_replace['start_col'] == int(start_col))]
        print(selected_row)
        selected_index = selected_row.index[0]  # Assuming there's only one matching row
        print(value)
        print(df_replace.loc[selected_index, 'cluster_MPV'])
        df_replace['cluster_MPV'].loc[selected_index] =  value 
        df_replace.to_csv(csv_file, index=True)

    return chargeMPV


def get_seedchargeMPV(file_list):
    print('say something')
    bin_width = args.binseed
    bin_contraction = True
    chargeMPV=[]
    for file in file_list:
        directory_path, filename_file = os.path.split(file)
        bin_width=args.binseed
        bin_contraction =True
        try:
            file_name = uproot.open(file)
            print('opend filfe')
            x=file_name["hChargeroi;1"].axis().edges()
            y=file_name["hChargeroi;1"].values()

            y_new_list=[]
            x_new = []

            for i in range(0, int((len(y) // bin_width) * bin_width), bin_width):
                if bin_width == 1:
                    y_new = np.sum(y[i])
                else:
                    y_new = np.sum(y[i:(i + bin_width - 1)])
                y_new_list.append(y_new)
                x_new.append(i * x[1])

            y_new_list=[]
            x_new = []

            for i in range(0, int((len(y) // bin_width) * bin_width), bin_width):
                if bin_width == 1:
                    y_new = np.sum(y[i])
                else:
                    y_new = np.sum(y[i:(i + bin_width - 1)])
                y_new_list.append(y_new)
                x_new.append(i * x[1])

            y_new = np.array(y_new_list)
            x_new = np.array(x_new)

            if bin_contraction == True:
                x=x_new
                y=y_new
            
            yerr=np.sqrt(y)

            d = {'x': x, 'y': y,'yerr': yerr,}
            df = pd.DataFrame(data=d)
            filename =os.path.join(directory_path, 'charge_fit', filename_file + '.csv')
            df.to_csv(filename)

            x_fit = [n for n, i in enumerate(y) if i > (args.rangeseed * y.max())]
            y_fit = y[x_fit[0]:x_fit[-1] + 1]
                
            yerr=yerr[x_fit[0]:x_fit[-1]]

            # Fit
            mpv, eta, sigma, A = x[y.argmax()], 4, 130, y.max()
            lower_bounds = [0, 0, 0, 0]
            upper_bounds = [np.inf, np.inf, np.inf, np.inf]
            try:
                coeff, pcov = curve_fit(pylandau.langau, x[x_fit[0]:x_fit[-1]], y[x_fit[0]:x_fit[-1]],
                                        sigma=yerr,
                                        absolute_sigma=True,
                                        p0=(mpv, eta, sigma, A),
                                        bounds=(lower_bounds, upper_bounds))
                print('hat gefittet')
                print(coeff)
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
            # Extracting start column, stop column, start row, and stop row
            match_roi = re.search(r'roi-(\d+)-(\d+)-(\d+)-(\d+)', filename)
            if match_roi:
                start_col = match_roi.group(1)
                stop_col = match_roi.group(2)
                start_row = match_roi.group(3)
                stop_row = match_roi.group(4)

                #print("Start Column:", start_col)
                #print("Stop Column:", stop_col)
                #print("Start Row:", start_row)
                #print("Stop Row:", stop_row)
            else:
                print("ROI information not found in the filename.")
            plt.title('run {} Seed Charge, cols{}-{}'.format(run_number,start_col,stop_col))
            plt.ylabel('number of events')
            plt.xlim([0, 10000])
            plt.xlabel('charge [electron]')
            

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
            plt.show()
            plt.close()

            value = [coeff[0], round(np.sqrt(pcov[0, 0]), 5)]
            chargeMPV.append(value)

        except Exception as e:
            print('something failed')
            print(e)
            value = [0, 0]
            chargeMPV.append(value)
    

    csv_file = '/home/bgnet/tbsw_workspace_july_2023/Plotter_cal/results.csv'

    if os.path.isfile(csv_file):
        df_replace = pd.read_csv(csv_file)
        df_replace.set_index('Unnamed: 0', inplace=True)
        #print("Index:", df_replace.index)
        #print(df_replace.loc[int(run_number)])
        selected_row = df_replace[(df_replace.index == int(run_number)) & (df_replace['start_col'] == int(start_col))]
        print(selected_row)
        selected_index = selected_row.index[0]  # Assuming there's only one matching row
        print(value)
        print(df_replace.loc[selected_index, 'seed_MPV'])
        df_replace['seed_MPV'].loc[selected_index] =  value 
        df_replace.to_csv(csv_file, index=True)

    return chargeMPV



if __name__ == '__main__':

    args = parse_args()
    path = args.path
    plotter_run_files = extract_plotter_run_files(args.path, args.start)


    result_df = extract_and_add_to_dataframe(plotter_run_files)

    result_df['chargeMPV']=get_chargeMPV(plotter_run_files)
    result_df['seedMPV']=get_seedchargeMPV(plotter_run_files)
    #result_df['chargeseedMPV in ToT']=get_chargeseedMPV('ToT',args.path, args.FrontEnd, args.prefix)
    print( result_df['chargeMPV'])
    print( result_df['seedMPV'])
    #print(result_df['chargeseedMPV in ToT'])
    #print(result_df['chargeMPV'],result_df['chargeMPV_CZcal'],result_df['chargeMPV_EPIcal'])
    
    #result_df.to_csv('/home/bgnet/vtx/tbsw_workspace_tjmp2_desy/refit'+str(args.start)+'.csv')


    
    
    
    
    
    
    
    
    
    
