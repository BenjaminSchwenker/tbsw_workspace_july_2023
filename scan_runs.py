import pandas as pd
import os
import argparse
import subprocess
from multiprocessing import Pool


def run_script(input):
    (command, arg_str) = input
    print("Starting command :{} with argument {}".format(command, arg_str))
    result = subprocess.call(command+" -e "+arg_str, shell=True)
    print("Completed command :{} with argument {}".format(command, arg_str))
    return result


def main(start, stop, only_plot, only_scan):

    df = pd.read_csv("runDB.csv", sep=",")
    df = df[(df["runno"] >= start) & (df["runno"] <= stop)]
    args_scan = []
    args_plot = []
    print(df)
    if not only_scan:
        for index in range(len(df.index)):
            args_plot.append(
                f"python3 histo-plotter-tj2.py --runno {int(df.iloc[index]['runno'])}  --colstart {int(df.iloc[index]['roi_colstart'])} --colstop {int(df.iloc[index]['roi_colstop'])} --rowstart {int(df.iloc[index]['roi_rowstart'])} --rowstop {int(df.iloc[index]['roi_rowstop'])}")

    df = df.drop_duplicates(subset=['runno'])
    if not only_plot:
        for index in range(len(df.index)):
            print(index)
            args_scan.append(
                f"python3 tj2-reco.py --runno {int(df.iloc[index]['runno'])}  --gearfile gear_geoid{int(df.iloc[index]['geoID'])}.xml --minocc {df.iloc[index]['minocc']} --prefix _clustdb")
    

    with Pool(4) as p:  # choose appropriate level of parallelism
        # choose appropriate command and argument, can be fetched from sys.argv if needed
        exit_codes = p.map(run_script, [('xterm', arg) for arg in args_scan])
        print("Exit codes : {}".format(exit_codes))

    with Pool(4) as p:  # choose appropriate level of parallelism
        # choose appropriate command and argument, can be fetched from sys.argv if needed
        exit_codes = p.map(run_script, [('xterm', arg) for arg in args_plot])
        print("Exit codes : {}".format(exit_codes))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Perform calibration and reconstruction of a test beam run")
    parser.add_argument('--start', dest='start',
                        type=int, help='Start run number')
    parser.add_argument('--stop', dest='stop', type=int,
                        help='Stop run number')
    parser.add_argument('--only_plot', dest='only_plot', type=bool, default=False,
                        help='only do plotting')
    parser.add_argument('--only_scan', dest='only_scan', type=bool, default=False,
                        help='only do reco')
    args = parser.parse_args()
    main(args.start, args.stop, args.only_plot, args.only_scan)
