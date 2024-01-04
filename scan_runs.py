import pandas as pd
import os
import argparse
import subprocess
from multiprocessing import Pool
import time
import shutil


def run_script(input):
    (command, arg_str) = input
    print("Starting command :{} with argument {}".format(command, arg_str))
    result = subprocess.call(command+" -e "+arg_str, shell=True)
    print("Completed command :{} with argument {}".format(command, arg_str))
    # Extract run number from the argument string
    run_number = int(arg_str.split('--runno')[1].split()[0])
    print(run_number)
    formatted_run_number = f"{run_number:06d}"
    # Delete the folders in temp-runs
    temp_runs_path = "tmp-runs"
    for folder_name in os.listdir(temp_runs_path):
        print(folder_name)
        if formatted_run_number in folder_name:
            folder_path = os.path.join(temp_runs_path, folder_name)
            shutil.rmtree(folder_path)
            print(f"Deleted folder: {folder_path}")

    return result


def main(start, stop, only_plot, only_scan,cal):
    start_time = time.time() 

    df = pd.read_csv("runDB_calib.csv", sep=",")
    df = df[(df["runno"] >= start) & (df["runno"] <= stop)]
    args_scan = []
    args_plot = []
    print(df)
    if not cal:
        if not only_scan:
            for index in range(len(df.index)):
                args_plot.append(
                    f"python3 histo-plotter-tj2.py --runno {int(df.iloc[index]['runno'])}  --colstart {int(df.iloc[index]['roi_colstart'])} --colstop {int(df.iloc[index]['roi_colstop'])} --rowstart {int(df.iloc[index]['roi_rowstart'])} --rowstop {int(df.iloc[index]['roi_rowstop'])}")
                

        df = df.drop_duplicates(subset=['runno'])
        if not only_plot:
            for index in range(len(df.index)):
                args_scan.append(
                    f"python3 tj2-reco.py --runno {int(df.iloc[index]['runno'])}  --gearfile gear_geoid{int(df.iloc[index]['geoID'])}.xml --minocc {df.iloc[index]['minocc']} --prefix {args.prefix} --datapath /media/bgnet/corry_2/textwriter_dumps/")
    else:
        if not only_scan:
            for index in range(len(df.index)):
                if str(df.iloc[index]['cal_file']) == 'None':
                    continue
                else:
                    args_plot.append(
                        f"python3 histo-plotter-tj2.py --runno {int(df.iloc[index]['runno'])}  --colstart {int(df.iloc[index]['roi_colstart'])} --colstop {int(df.iloc[index]['roi_colstop'])} --rowstart {int(df.iloc[index]['roi_rowstart'])} --rowstop {int(df.iloc[index]['roi_rowstop'])} --calib electrons")
                    args_plot.append(
                        f"python plot_clustercharge_cluster.py -file Plotter-run000{int(df.iloc[index]['runno'])}-roi-{int(df.iloc[index]['roi_colstart'])}-{int(df.iloc[index]['roi_colstop'])}-{int(df.iloc[index]['roi_rowstart'])}-{int(df.iloc[index]['roi_rowstop'])}.root")


        df = df.drop_duplicates(subset=['runno'])
        if not only_plot:
            for index in range(len(df.index)):
                print(str(df.iloc[index]['cal_file']))
                if str(df.iloc[index]['cal_file']) == 'None':
                    args_scan.append(
                    f"python3 tj2-reco.py --runno {int(df.iloc[index]['runno'])}  --gearfile gear_geoid{int(df.iloc[index]['geoID'])}.xml --minocc {df.iloc[index]['minocc']} --prefix {args.prefix+'_cal'} --datapath /media/bgnet/corry_2/textwriter_dumps/")
                else:
                    args_scan.append(
                       f"python3 tj2-reco.py --runno {int(df.iloc[index]['runno'])}  --gearfile gear_geoid{int(df.iloc[index]['geoID'])}.xml --minocc {df.iloc[index]['minocc']} --prefix {args.prefix+'_cal'} --datapath /media/bgnet/corry_2/textwriter_dumps/ --pixel_cal --pixel_cal_file {str(df.iloc[index]['cal_file'])}")
    

    with Pool(4) as p:  # choose appropriate level of parallelism
        # choose appropriate command and argument, can be fetched from sys.argv if needed
        exit_codes = p.map(run_script, [('xterm', arg) for arg in args_scan])
        print("Exit codes : {}".format(exit_codes))

    with Pool(4) as p:  # choose appropriate level of parallelism
        # choose appropriate command and argument, can be fetched from sys.argv if needed
        exit_codes = p.map(run_script, [('xterm', arg) for arg in args_plot])
        print("Exit codes : {}".format(exit_codes))
        
    end_time = time.time()  # Record the end time
    elapsed_time = end_time - start_time  # Calculate elapsed time
    print(f"Total time taken: {elapsed_time} seconds")

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Perform calibration and reconstruction of a test beam run")
    parser.add_argument('--start', dest='start',
                        type=int, help='Start run number')
    parser.add_argument('--stop', dest='stop', type=int,
                        help='Stop run number')
    parser.add_argument('--only_plot', dest='only_plot', action='store_true',
                    	help='only do plotting')
    parser.add_argument('--only_scan', dest='only_scan', type=bool, default=False,
                        help='only do reco')
    parser.add_argument('--cal', dest='cal', type=bool, default=False,
                        help='add calibration to analysis')
    parser.add_argument('--prefix', type=str, default='_CoG', 
                        help='Prefix for the data processing')

    args = parser.parse_args()
    main(args.start, args.stop, args.only_plot, args.only_scan, args.cal)
