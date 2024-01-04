import pandas as pd

# Replace 'MaxPositionFiltered.csv' and 'pixelnumber_info.csv' with the actual paths to your CSV files
max_position_file = '/media/bgnet/TB2023_TBSW_Data/tbsw_workspace_july_2023/nDutDigits_clustDB_1000000ev/max_positions.csv'
pixel_info_file = 'pixelnumber_info.csv'

# Read the CSV files into DataFrames
df_max_position = pd.read_csv(max_position_file)
df_pixel_info = pd.read_csv(pixel_info_file)

# Merge DataFrames on 'RunNumber'
df_merged = pd.merge(df_max_position, df_pixel_info, left_on='RunNumber', right_on='Runno', how='inner')

# Calculate the fake rate
df_merged['FakeRate_MaxPosition'] = df_merged['MaxPositionFiltered'] / df_merged['TotalPixels']
df_merged['FakeRate_MaxPosition[1:]'] = df_merged['MaxPosition[1:]Filtered'] / df_merged['TotalPixels']
df_merged['FakeRate_Mean'] = df_merged['MeanFiltered'] / df_merged['TotalPixels']
df_merged = df_merged.sort_values(by='RunNumber')
# Print the resulting DataFrame with the calculated fake rate
print(df_merged)
df_merged.to_csv('/media/bgnet/TB2023_TBSW_Data/tbsw_workspace_july_2023/fakerate.csv', index=False)