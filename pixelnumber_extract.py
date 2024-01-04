import pandas as pd

# Replace 'your_file.csv' with the path to your CSV file
file_path = 'export.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path, encoding='latin-1', sep=';')

print(df.columns)
# Select only the columns 'User', 'Run no', 'ConfigID', 'Device', and 'Text'
selected_columns = ['Run no', 'ConfigID', 'Device', 'Text']
df_selected = df[selected_columns]

# Extract the information matching the pattern "Pixels: xxx:xxx" from the 'Text' column
df_selected['PixelsInfo'] = df_selected['Text'].str.extract(r'Pixels: (\d+:\d+)')

# Split the 'PixelsInfo' column into two separate columns
df_selected[['StartCol', 'StopCol']] = df_selected['PixelsInfo'].str.split(':', expand=True)

# Convert 'StartCol' and 'StopCol' to numeric values
df_selected['StartCol'] = pd.to_numeric(df_selected['StartCol'])
df_selected['StopCol'] = pd.to_numeric(df_selected['StopCol'])

# Calculate the 'Total Pixels' column
df_selected['TotalPixels'] = (df_selected['StopCol'] - df_selected['StartCol']) * 512

# Drop the original 'Text' and 'PixelsInfo' columns if you no longer need them
df_selected = df_selected.drop(columns=['Text', 'PixelsInfo'])

# Sort the DataFrame by 'Run no'
df_selected = df_selected.sort_values(by='Run no')

# Drop rows with NaN values in 'Run no'
df_selected = df_selected.dropna(subset=['Run no'])

df_selected = df_selected.rename(columns={'Run no': 'Runno'})

# Save the DataFrame to a new CSV file
df_selected.to_csv('pixelnumber_info.csv', index=False)