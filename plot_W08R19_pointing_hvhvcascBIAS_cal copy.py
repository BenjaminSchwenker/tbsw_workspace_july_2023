import csv
import ast
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Function to convert string representation of list to a list and extract the first element
def extract_first_element(x,b):
    values = ast.literal_eval(x)
    return float(values[b])

# Specify the path to your CSV file
csv_file_path = 'Plotter_cal/results.csv'
csv_file_path_uncal = 'Plotter/results.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_file_path, index_col=0)
df_uncal = pd.read_csv(csv_file_path_uncal, index_col=0)

# Print the DataFrame
print(df.index)



selected_indices = [994,995,996,997,998,999,1000,1001,1002,1003,1004,1005,1006,1007,1008]
angles = [2,4,6,8,10,12,14,16,18,20,22,24,26,28,30]

# Specify the conditions for filtering
lower_limit = 480
upper_limit = 492

# Filter the data based on the conditions
filtered_data = df[(df['start_col'] > lower_limit) & (df['start_col'] < upper_limit)]
filtered_data_uncal = df_uncal[(df_uncal['start_col'] > lower_limit) & (df_uncal['start_col'] < upper_limit)]

# Extract the data for the specified indices
selected_data = filtered_data.loc[selected_indices]
selected_data_uncal = filtered_data_uncal.loc[selected_indices]

# Extract the first element from the 'pointing_u' and 'pointing_error_u' columns
selected_data['pointing_u'] = selected_data['pointing_u'].apply(lambda x:extract_first_element(x,0))
selected_data['pointing_error_u'] = selected_data['pointing_error_u'].apply(lambda x:extract_first_element(x,0))
fig1, ax1 = plt.subplots()
ax1.errorbar(angles, selected_data['pointing_u'], yerr=selected_data['pointing_error_u'], fmt='o', capsize=5, label='size>0')

# Extract the data for the specified indices
selected_data = filtered_data.loc[selected_indices]
# Extract the first element from the 'pointing_u' and 'pointing_error_u' columns
selected_data['pointing_u'] = selected_data['pointing_u'].apply(lambda x:extract_first_element(x,1))
selected_data['pointing_error_u'] = selected_data['pointing_error_u'].apply(lambda x:extract_first_element(x,1))
ax1.errorbar(angles, selected_data['pointing_u'], yerr=selected_data['pointing_error_u'], fmt='o', capsize=5, label='size==1')


# Extract the data for the specified indices
selected_data = filtered_data.loc[selected_indices]
# Extract the first element from the 'pointing_u' and 'pointing_error_u' columns
selected_data['pointing_u'] = selected_data['pointing_u'].apply(lambda x:extract_first_element(x,2))
selected_data['pointing_error_u'] = selected_data['pointing_error_u'].apply(lambda x:extract_first_element(x,2))
ax1.errorbar(angles, selected_data['pointing_u'], yerr=selected_data['pointing_error_u'], fmt='o', capsize=5, label='size==2')
ax1.set_xlabel('Bias voltage [V]')
ax1.set_ylabel('Pointing_u')
ax1.set_title('W08R19 HV bias scan pointing resolution in u')
ax1.legend()


# Extract the first element from the 'pointing_v' and 'pointing_error_v' columns
selected_data['pointing_v'] = selected_data['pointing_v'].apply(lambda x:extract_first_element(x,0))
selected_data['pointing_error_v'] = selected_data['pointing_error_v'].apply(lambda x:extract_first_element(x,0))
fig2, ax2 = plt.subplots()
ax2.errorbar(angles, selected_data['pointing_v'], yerr=selected_data['pointing_error_v'], fmt='o', capsize=5, label='size>0')



# Extract the data for the specified indices
selected_data = filtered_data.loc[selected_indices]
# Extract the first element from the 'pointing_v' and 'pointing_error_v' columns
selected_data['pointing_v'] = selected_data['pointing_v'].apply(lambda x:extract_first_element(x,1))
selected_data['pointing_error_v'] = selected_data['pointing_error_v'].apply(lambda x:extract_first_element(x,1))
ax2.errorbar(angles, selected_data['pointing_v'], yerr=selected_data['pointing_error_v'], fmt='o', capsize=5, label='size==1')


# Extract the data for the specified indices
selected_data = filtered_data.loc[selected_indices]
# Extract the first element from the 'pointing_v' and 'pointing_error_v' columns
selected_data['pointing_v'] = selected_data['pointing_v'].apply(lambda x:extract_first_element(x,2))
selected_data['pointing_error_v'] = selected_data['pointing_error_v'].apply(lambda x:extract_first_element(x,2))
ax2.errorbar(angles, selected_data['pointing_v'], yerr=selected_data['pointing_error_v'], fmt='o', capsize=5, label='size==2')
ax2.set_xlabel('Bias voltage [V]')
ax2.set_ylabel('Pointing_v')
ax2.set_title('W08R19 HV bias scan pointing resolution in v')
ax2.legend()
  
# Extract the data for the specified indices
selected_data = filtered_data.loc[selected_indices]
# Extract the first element from the 'pointing_u' and 'pointing_error_u' columns
selected_data['cluster_size_u'] = selected_data['cluster_size_u'].apply(ast.literal_eval)
selected_data['cluster_size_u_error'] = selected_data['cluster_size_u_error'].apply(ast.literal_eval)
fig1, ax1 = plt.subplots()
ax1.errorbar(angles, selected_data['cluster_size_u'], yerr=selected_data['cluster_size_u_error'], fmt='o', capsize=5, label='cluster_size_u')
# Extract the data for the specified indices
selected_data = filtered_data.loc[selected_indices]
# Extract the first element from the 'pointing_u' and 'pointing_error_u' columns
selected_data['cluster_size_v'] = selected_data['cluster_size_v'].apply(ast.literal_eval)
selected_data['cluster_size_v_error'] = selected_data['cluster_size_v_error'].apply(ast.literal_eval)
ax1.errorbar(angles, selected_data['cluster_size_v'], yerr=selected_data['cluster_size_v_error'], fmt='o', capsize=5, label='cluster_size_v')
ax1.set_xlabel('Bias voltage [V]')
ax1.set_ylabel('cluster_size_u mean')
ax1.set_title('W08R19 HV bias scan cluster_size_u')
ax1.legend()

######################################################

# Specify the conditions for filtering
lower_limit = 448
upper_limit = 480

# Filter the data based on the conditions
filtered_data = df[(df['start_col'] > lower_limit) & (df['start_col'] < upper_limit)]
filtered_data_uncal = df_uncal[(df_uncal['start_col'] > lower_limit) & (df_uncal['start_col'] < upper_limit)]

# Extract the data for the specified indices
selected_data = filtered_data.loc[selected_indices]
selected_data_uncal = filtered_data_uncal.loc[selected_indices]

# Extract the first element from the 'pointing_u' and 'pointing_error_u' columns
selected_data['pointing_u'] = selected_data['pointing_u'].apply(lambda x:extract_first_element(x,0))
selected_data['pointing_error_u'] = selected_data['pointing_error_u'].apply(lambda x:extract_first_element(x,0))
fig1, ax1 = plt.subplots()
ax1.errorbar(angles, selected_data['pointing_u'], yerr=selected_data['pointing_error_u'], fmt='o', capsize=5, label='size>0')

# Extract the data for the specified indices
selected_data = filtered_data.loc[selected_indices]
# Extract the first element from the 'pointing_u' and 'pointing_error_u' columns
selected_data['pointing_u'] = selected_data['pointing_u'].apply(lambda x:extract_first_element(x,1))
selected_data['pointing_error_u'] = selected_data['pointing_error_u'].apply(lambda x:extract_first_element(x,1))
ax1.errorbar(angles, selected_data['pointing_u'], yerr=selected_data['pointing_error_u'], fmt='o', capsize=5, label='size==1')


# Extract the data for the specified indices
selected_data = filtered_data.loc[selected_indices]
# Extract the first element from the 'pointing_u' and 'pointing_error_u' columns
selected_data['pointing_u'] = selected_data['pointing_u'].apply(lambda x:extract_first_element(x,2))
selected_data['pointing_error_u'] = selected_data['pointing_error_u'].apply(lambda x:extract_first_element(x,2))
ax1.errorbar(angles, selected_data['pointing_u'], yerr=selected_data['pointing_error_u'], fmt='o', capsize=5, label='size==2')
ax1.set_xlabel('Bias voltage [V]')
ax1.set_ylabel('Pointing_u')
ax1.set_title('W08R19 HVCASC bias scan pointing resolution in u')
ax1.legend()


# Extract the first element from the 'pointing_v' and 'pointing_error_v' columns
selected_data['pointing_v'] = selected_data['pointing_v'].apply(lambda x:extract_first_element(x,0))
selected_data['pointing_error_v'] = selected_data['pointing_error_v'].apply(lambda x:extract_first_element(x,0))
fig2, ax2 = plt.subplots()
ax2.errorbar(angles, selected_data['pointing_v'], yerr=selected_data['pointing_error_v'], fmt='o', capsize=5, label='size>0')



# Extract the data for the specified indices
selected_data = filtered_data.loc[selected_indices]
# Extract the first element from the 'pointing_v' and 'pointing_error_v' columns
selected_data['pointing_v'] = selected_data['pointing_v'].apply(lambda x:extract_first_element(x,1))
selected_data['pointing_error_v'] = selected_data['pointing_error_v'].apply(lambda x:extract_first_element(x,1))
ax2.errorbar(angles, selected_data['pointing_v'], yerr=selected_data['pointing_error_v'], fmt='o', capsize=5, label='size==1')


# Extract the data for the specified indices
selected_data = filtered_data.loc[selected_indices]
# Extract the first element from the 'pointing_v' and 'pointing_error_v' columns
selected_data['pointing_v'] = selected_data['pointing_v'].apply(lambda x:extract_first_element(x,2))
selected_data['pointing_error_v'] = selected_data['pointing_error_v'].apply(lambda x:extract_first_element(x,2))
ax2.errorbar(angles, selected_data['pointing_v'], yerr=selected_data['pointing_error_v'], fmt='o', capsize=5, label='size==2')
ax2.set_xlabel('Bias voltage [V]')
ax2.set_ylabel('Pointing_v')
ax2.set_title('W08R19 HVCASC bias scan pointing resolution in v')
ax2.legend()
  
# Extract the data for the specified indices
selected_data = filtered_data.loc[selected_indices]
# Extract the first element from the 'pointing_u' and 'pointing_error_u' columns
selected_data['cluster_size_u'] = selected_data['cluster_size_u'].apply(ast.literal_eval)
selected_data['cluster_size_u_error'] = selected_data['cluster_size_u_error'].apply(ast.literal_eval)
fig1, ax1 = plt.subplots()
ax1.errorbar(angles, selected_data['cluster_size_u'], yerr=selected_data['cluster_size_u_error'], fmt='o', capsize=5, label='cluster_size_u')
# Extract the data for the specified indices
selected_data = filtered_data.loc[selected_indices]
# Extract the first element from the 'pointing_u' and 'pointing_error_u' columns
selected_data['cluster_size_v'] = selected_data['cluster_size_v'].apply(ast.literal_eval)
selected_data['cluster_size_v_error'] = selected_data['cluster_size_v_error'].apply(ast.literal_eval)
ax1.errorbar(angles, selected_data['cluster_size_v'], yerr=selected_data['cluster_size_v_error'], fmt='o', capsize=5, label='cluster_size_v')
ax1.set_xlabel('Bias voltage [V]')
ax1.set_ylabel('cluster_size_u mean')
ax1.set_title('W08R19 HVCASC bias scan cluster_size_u')
ax1.legend()

######################################################

lower_limit = 480
upper_limit = 492
filtered_data = df[(df['start_col'] > lower_limit) & (df['start_col'] < upper_limit)]
filtered_data_uncal = df_uncal[(df_uncal['start_col'] > lower_limit) & (df_uncal['start_col'] < upper_limit)]

# Extract the data for the specified indices
selected_data = filtered_data.loc[selected_indices]
selected_data_uncal = filtered_data_uncal.loc[selected_indices]

# Extract the first element from the 'pointing_u' and 'pointing_error_u' columns
selected_data['pointing_u'] = selected_data['pointing_u'].apply(lambda x:extract_first_element(x,0))
selected_data['pointing_error_u'] = selected_data['pointing_error_u'].apply(lambda x:extract_first_element(x,0))
selected_data_uncal['pointing_u'] = selected_data_uncal['pointing_u'].apply(lambda x:extract_first_element(x,0))
selected_data_uncal['pointing_error_u'] = selected_data_uncal['pointing_error_u'].apply(lambda x:extract_first_element(x,0))
fig1, ax1 = plt.subplots()
ax1.errorbar(angles, selected_data['pointing_u'], yerr=selected_data['pointing_error_u'], fmt='o', capsize=5, label='size>0 calibrated')
ax1.errorbar(angles, selected_data_uncal['pointing_u'], yerr=selected_data_uncal['pointing_error_u'], fmt='o', capsize=5, label='size>0 uncalibrated')

ax1.set_xlabel('Bias voltage [V]')
ax1.set_ylabel('Pointing_u')
ax1.set_title('W08R19 HV bias scan  comparison of cal. and uncal. pointing resolution in u')
ax1.legend()
####################################################################

lower_limit = 448
upper_limit = 480
filtered_data = df[(df['start_col'] > lower_limit) & (df['start_col'] < upper_limit)]
filtered_data_uncal = df_uncal[(df_uncal['start_col'] > lower_limit) & (df_uncal['start_col'] < upper_limit)]

# Extract the data for the specified indices
selected_data = filtered_data.loc[selected_indices]
selected_data_uncal = filtered_data_uncal.loc[selected_indices]

# Extract the first element from the 'pointing_u' and 'pointing_error_u' columns
selected_data['pointing_u'] = selected_data['pointing_u'].apply(lambda x:extract_first_element(x,0))
selected_data['pointing_error_u'] = selected_data['pointing_error_u'].apply(lambda x:extract_first_element(x,0))
selected_data_uncal['pointing_u'] = selected_data_uncal['pointing_u'].apply(lambda x:extract_first_element(x,0))
selected_data_uncal['pointing_error_u'] = selected_data_uncal['pointing_error_u'].apply(lambda x:extract_first_element(x,0))
fig1, ax1 = plt.subplots()
ax1.errorbar(angles, selected_data['pointing_u'], yerr=selected_data['pointing_error_u'], fmt='o', capsize=5, label='size>0 calibrated')
ax1.errorbar(angles, selected_data_uncal['pointing_u'], yerr=selected_data_uncal['pointing_error_u'], fmt='o', capsize=5, label='size>0 uncalibrated')

ax1.set_xlabel('Bias voltage [V]')
ax1.set_ylabel('Pointing_u')
ax1.set_title('W08R19 HVCASC bias scan  comparison of cal. and uncal. pointing resolution in u')
ax1.legend()



# call the function 
def save_image(filename): 
    
    # PdfPages is a wrapper around pdf  
    # file so there is no clash and create 
    # files with no error. 
    p = PdfPages(filename) 
      
    # get_fignums Return list of existing  
    # figure numbers 
    fig_nums = plt.get_fignums()   
    figs = [plt.figure(n) for n in fig_nums] 
      
    # iterating over the numbers in list 
    for fig in figs:  
        
        # and saving the files 
        fig.savefig(p, format='pdf')  
      
    # close the object 
    p.close()   
  
# name your Pdf file 
filename = "/home/bgnet/tbsw_workspace_july_2023/pointing_clustersize/W08R19_cal_HV_HVCASC_Bias.pdf"  
  
# call the function 
save_image(filename)