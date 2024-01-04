import pandas as pd

# Assuming you have two CSV files named 'file1.csv' and 'file2.csv'
file1_path = 'Plotter/results.csv'
file2_path = 'root-files/results.csv'

# Reading CSV files into pandas dataframes
df1 = pd.read_csv(file1_path, index_col="Unnamed: 0")
df2 = pd.read_csv(file2_path, index_col="Unnamed: 0")
df1 = df1[~df1.index.duplicated(keep='first')]
df2 = df2[~df2.index.duplicated(keep='first')]
print(df2)

# Extracting information from the first dataframe
start_col = df1['start_col'].values
stop_col = df1['stop_col']
start_row = df1['start_row']
stop_row = df1['stop_row']

# Calculating the number of pixels enabled
num_pixels_enabled = (stop_col - start_col + 1) * (stop_row - start_row + 1)

# Calculating MPV divided by the number of pixels enabled from the last file
df2['MPV_normalized'] = df2['MPV'] / num_pixels_enabled

# Adding start_col, stop_col, start_row, stop_row, and num_pixels_enabled to the dataframe
df2['start_col'] = start_col
df2['stop_col'] = stop_col
df2['start_row'] = start_row
df2['stop_row'] = stop_row
df2['num_pixels_enabled'] = num_pixels_enabled
df2['runno']=df2.index
# Reordering columns for better organization
df2 = df2[['start_col', 'stop_col', 'start_row', 'stop_row', 'num_pixels_enabled', 'MPV', 'MPV_normalized', 'runno']]

# Writing the result to a new CSV file
output_file_path = 'fake_rate.csv'
df2.to_csv(output_file_path, index=False)

# Optionally, you can also display the resulting dataframe
print(df2)
