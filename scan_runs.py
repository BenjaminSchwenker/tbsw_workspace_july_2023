import pandas as pd
import os
import argparse


def main(start, stop):

    df = pd.read_csv("runDB.csv", sep=" ")
    df = df[(df["runno"] >= start) & (df["runno"] <= stop)]
    for index in df.index:
        os.system(
            f"python3 tj2-reco.py --runno {df.iloc[index]['runno']}  --gearfile gear_geoid{df.iloc[index]['geoID']}.xml"
        )
        os.system(
            f"python3 histo-plotter-tj2.py --runno {df.iloc[index]['runno']}  --colstart {df.iloc[index]['roi_colstart']} --colstop {df.iloc[index]['roi_colstop']} --rowstart {df.iloc[index]['roi_rowstart']} --rowstop {df.iloc[index]['roi_rowstop']}"
        )


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Perform calibration and reconstruction of a test beam run")
    parser.add_argument('--start', dest='start',
                        type=int, help='Start run number')
    parser.add_argument('--stop', dest='stop', type=int,
                        help='Stop run number')
    args = parser.parse_args()
    main(args.start, args.stop)
