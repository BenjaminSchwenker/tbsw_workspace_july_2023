import os
import subprocess

# Define the folder where you want to search for .h5 files
folder_path = '/home/bgnet/tbsw_workspace_july_2023/TB2023_tuning/W14R12/04_HV_THR22/'

# Recursive function to execute the script on .h5 files
def process_h5_files(folder):
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith('charge_calib.h5'):
                input_file = os.path.join(root, file)
                print(input_file)
                output_file = os.path.join(root, file.replace('.h5', '.root'))
                cmd = [
                    'python3',
                    'calibFuncExample.py',
                    '-input',
                    input_file,
                    '-output',
                    output_file
                ]
                subprocess.run(cmd)

# Call the function to start processing
process_h5_files(folder_path)