import pandas as pd
import os
import numpy as np
from multiprocessing import Pool, cpu_count

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio

def read_and_prepare_data(folder_col, folder_vir):
    df_col = pd.read_csv(folder_col, sep='\t')
    df_vir = pd.read_csv(folder_vir, sep='\t')
    df_vir['VIR'] = 1
    df_col['COL'] = 1
    merged_df = pd.merge(df_vir, df_col, on=['ID','Position'], how='outer')
    df_filled = merged_df.fillna(0)
    df_filled['COL'] = df_filled['COL'].astype(int)
    df_filled['VIR'] = df_filled['VIR'].astype(int)
    return df_filled

def process_single_file(df_filled, file_path):
    df = pd.read_csv(file_path, sep='\t')[['position', 'nucleotide_martin', 'nucleotide_origin', 'label_mar', 'label_ori']]
    file_id = os.path.splitext(os.path.basename(file_path))[0]
    
    if file_id in df_filled['ID'].values:
        row = df_filled[df_filled['ID'] == file_id].iloc[0]
        if row['Position'] in df['position'].values:
            df.loc[df['position'] == row['Position'], 'VIR'] = row['VIR']
            df.loc[df['position'] == row['Position'], 'COL'] = row['COL']
        else:
            return file_id, None
    else:
        df['COL'] = np.nan
        df['VIR'] = np.nan

    df_v1 = df.fillna(0).astype({'VIR': int, 'COL': int})
    return None, df_v1

def compute_statistics(df_v1):
    stats = [
        sum(df_v1['label_mar'] == 1),
        sum(df_v1['label_ori'] == 1),
        sum((df_v1['label_mar'] == 0) & (df_v1['VIR'] == 0)),
        sum((df_v1['label_ori'] == 0) & (df_v1['COL'] == 0)),
        sum(df_v1['VIR'] == 1),
        sum(df_v1['COL'] == 1),

        sum((df_v1['VIR'] == 1) & (df_v1['label_ori'] == 1)),
        sum((df_v1['VIR'] == 1) & (df_v1['COL'] == 1) & (df_v1['label_ori'] == 0) & (df_v1['label_mar'] == 0) &(df_v1['nucleotide_martin'] == df_v1['nucleotide_origin'])),
        sum((df_v1['VIR'] == 1) & (df_v1['COL'] == 0) & (df_v1['label_ori'] == 0) & (df_v1['label_mar'] == 0) &(df_v1['nucleotide_martin'] == df_v1['nucleotide_origin'])),
        sum((df_v1['VIR'] == 1) & (df_v1['COL'] == 1) & (df_v1['label_ori'] == 0) & (df_v1['label_mar'] == 0) &(df_v1['nucleotide_martin'] != df_v1['nucleotide_origin'])),
        sum((df_v1['VIR'] == 1) & (df_v1['COL'] == 0) & (df_v1['label_ori'] == 0) & (df_v1['label_mar'] == 0) &(df_v1['nucleotide_martin'] != df_v1['nucleotide_origin'])),

        sum((df_v1['COL'] == 1) & (df_v1['label_mar'] == 1)),
        sum((df_v1['COL'] == 1) & (df_v1['VIR'] == 1) & (df_v1['label_ori'] == 0) & (df_v1['label_mar'] == 0) &(df_v1['nucleotide_martin'] == df_v1['nucleotide_origin'])),
        sum((df_v1['COL'] == 1) & (df_v1['VIR'] == 0) & (df_v1['label_ori'] == 0) & (df_v1['label_mar'] == 0) &(df_v1['nucleotide_martin'] == df_v1['nucleotide_origin'])),
        sum((df_v1['COL'] == 1) & (df_v1['VIR'] == 1) & (df_v1['label_ori'] == 0) & (df_v1['label_mar'] == 0) &(df_v1['nucleotide_martin'] != df_v1['nucleotide_origin'])),
        sum((df_v1['COL'] == 1) & (df_v1['VIR'] == 0) & (df_v1['label_ori'] == 0) & (df_v1['label_mar'] == 0) &(df_v1['nucleotide_martin'] != df_v1['nucleotide_origin'])),
    ]
    return stats

def process_file_parallel(args):
    df_filled, file_path = args
    not_found_id, df_v1 = process_single_file(df_filled, file_path)
    
    if not_found_id:
        return (not_found_id, None)
    
    stats = compute_statistics(df_v1)
    return (None, stats)

def combine_assemblies(folder_col, folder_vir, folder_data, not_found_ids_file):
    df_filled = read_and_prepare_data(folder_col, folder_vir)
    all_not_found_ids = []
    total_stats = [0] * 16

    # Get all file paths
    all_files = [os.path.join(folder_data, file_name) for file_name in os.listdir(folder_data)]
    
    # Parallel processing with multiprocessing
    with Pool(cpu_count()) as pool:
        results = pool.map(process_file_parallel, [(df_filled, file_path) for file_path in all_files])
    
    for result in results:
        not_found_id, stats = result
        if not_found_id:
            all_not_found_ids.append(not_found_id)
        else:
            total_stats = [x + y for x, y in zip(total_stats, stats)]


    # Extract statistics from the stats list
    num_viridian_masked, num_colman_masked, num_viridian_unmasked_no_error, num_colman_unmasked_no_error, num_viridian_error, num_colman_error, NB_VIR_masked, NB_VIR_sameError, NB_VIR_same, NB_VIR_diffError, NB_VIR_diff, NB_COL_masked, NB_COL_sameError, NB_COL_same, NB_COL_diffError, NB_COL_diff = total_stats
    
    # Save not found IDs to a file
    with open(not_found_ids_file, 'w') as f:
        for item in all_not_found_ids:
            f.write("%s\n" % item)

    # Print the location of not_found_ids_file
    print(f"The not found IDs file has been saved to: {not_found_ids_file}")

    # Print the number of not found IDs
    print(f"The number of not found IDs: {len(all_not_found_ids)}")

    # Print the statistics
    print('====================== Info ======================')
    print('Total masked positions in Virdian assembly: ', num_viridian_masked)
    print('Total masked positions in Data-Portal assembly: ', num_colman_masked)
    
    print('====================== Info ======================')
    print('Total unmasked positions in Virdian assembly, without errors '
          'identified by MAPLE: ', num_viridian_unmasked_no_error)
    print('Total unmasked positions in Data-Portal assembly, without errors '
          'identified by MAPLE: ', num_colman_unmasked_no_error)
    
    print('====================== Info ======================')
    print('Total positions in Virdian assembly identified as errors by MAPLE '
          '(Virdian\'s errors): ', num_viridian_error)
    print('Total positions in Data-Portal assembly identified as errors by MAPLE '
          '(Data-Portal\'s errors): ', num_colman_error)
    
    print('====================== For VIR error ======================')
    print('Viridian\'s assemblies are masked: ',NB_VIR_masked)
    print('Same nucleotide, Viridian\'s assembly error: ',NB_VIR_sameError)
    print('Same nucleotide, Viridian\'s assembly not error: ',NB_VIR_same)
    print('Diff nucleotide, Viridian\'s assembly error: ',NB_VIR_diffError)
    print('Diff nucleotide, Viridian\'s assembly not error: ',NB_VIR_diff)
    print('====================== For COL error ======================')
    print('Data-Portal\'s assemblies are masked: ',NB_COL_masked)
    print('Same nucleotide, Data-Portal\'s assembly error: ',NB_COL_sameError)
    print('Same nucleotide, Data-Portal\'s assembly not error: ',NB_COL_same)
    print('Diff nucleotide, Data-Portal\'s assembly error: ',NB_COL_diffError)
    print('Diff nucleotide, Data-Portal\'s assembly not error: ',NB_COL_diff)

    return total_stats

folder_col = '/nfs/research/goldman/zihao/Datas/p2_compViridian_P3/Folder_mapleOutput/COL_output_modified.txt'
folder_vir = '/nfs/research/goldman/zihao/Datas/p2_compViridian_P3/Folder_mapleOutput/VIR_output_modified.txt'
folder_data = '/nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_2_combination/folderData_addInfo'
not_found_ids_file = '/nfs/research/goldman/zihao/Datas/p2_compViridian_P3/notFound_idsError.txt'

total_stats = combine_assemblies(folder_col, folder_vir, folder_data, not_found_ids_file)
# *************************************************
# *************** For visualisation ***************
# *************************************************
num_viridian_masked, num_colman_masked, num_viridian_unmasked_no_error, num_colman_unmasked_no_error, num_viridian_error, num_colman_error, NB_VIR_masked, NB_VIR_sameError, NB_VIR_same, NB_VIR_diffError, NB_VIR_diff, NB_COL_masked, NB_COL_sameError, NB_COL_same, NB_COL_diffError, NB_COL_diff = total_stats

def format_number(number):
    suffixes = ['', 'K', 'M', 'B', 'T']

    for i in range(len(suffixes)):
        magnitude = number / (1000 ** i)
        if magnitude < 1000:
            if magnitude < 10:
                formatted = f"{magnitude:.1f}"
            else:
                formatted = f"{magnitude:.0f}"
            return f"{formatted}{suffixes[i]}"
    
    return f"{number:.1e}"
# Define a function to format percentages
def format_percentage(value):
    # If the value is greater than 0 but less than 0.01 (i.e., 1% when multiplied by 100)
    if 0 < value < 0.01:
        return f"{value*100:.1e}%"
    # Otherwise, multiply the value by 100 and round to two decimal places
    formatted = round(value * 100, 2)
    # If the value is 0, return "0.0%"
    if formatted == 0:
        return "0.0%"
    # Return the formatted string
    return f"{formatted:.2f}%"

def format_data(masked, unmasked, error, error_othMasked, error_sameError, error_sameCorrect, error_diffError, error_diffCorrect):
    both = masked + unmasked + error
    error_both = error_othMasked + error_sameError + error_sameCorrect + error_diffError + error_diffCorrect
    
    formatted_numbers = [format_number(x) for x in [masked, unmasked, error]]
    formatted_numbers_error = [format_number(x) for x in [error_othMasked, error_sameError, error_sameCorrect, error_diffError, error_diffCorrect]]
    
    data = {
        'Category': ['Masked', 'Not Error', 'Error'],
        'Percentage': [np.log(x)/both for x in [masked, unmasked, error]],
        'Raw_Percentage': [x/both for x in [masked, unmasked, error]],
        'Raw_number': formatted_numbers
    }
    
    data_error = {
        'Category': ['otherMasked', 'sameError', 'sameCorrect', 'diffError', 'diff'],
        'Percentage': [x/error_both for x in [error_othMasked, error_sameError, error_sameCorrect, error_diffError, error_diffCorrect]],
        'Raw_number': formatted_numbers_error
    }
    
    return pd.DataFrame(data), pd.DataFrame(data_error)
## Part1_for Viridian Alignment
df_VIR_plot, df_VIR_ERR_plot = format_data(num_viridian_masked, num_viridian_unmasked_no_error, num_viridian_error, NB_VIR_masked, NB_VIR_sameError, NB_VIR_same, NB_VIR_diffError, NB_VIR_diff)
## Part2_for COVID-19 Data Portal Alignment
df_COL_plot, df_COL_ERR_plot = format_data(num_colman_masked, num_colman_unmasked_no_error, num_colman_error, NB_COL_masked, NB_COL_sameError, NB_COL_same, NB_COL_diffError, NB_COL_diff)


colors = ['#EBD67E', '#7FB7D1', '#89A78E']
colors_ERROR = ['#C9DFCC', '#9AC2A0', '#7AAC9A', '#688462', '#AAB07C']
label_err = ['otherMasked', 'sameError', 'sameCorrect', 'diffError', 'diff']

## Plot for Viridian Alignment
fig = make_subplots(rows=1, cols=2, subplot_titles=['Viridian Alignment', 'COVID-19 Data Portal Alignment'],
                    specs=[[{'type':'pie'}, {'type':'pie'}]])
fig.add_trace(go.Pie(labels=df_VIR_plot['Category'], values=df_VIR_plot['Percentage'], hole=0.4,
                 text=df_VIR_plot['Category']+': <br>' + df_VIR_plot['Raw_number'].astype(str)+
                 ' ('+df_VIR_plot['Raw_Percentage'].apply(format_percentage)+')',
                 textinfo='percent+text',
                 marker={'colors': colors},
                 hovertemplate='%{label}<br>Current percentage: %{percent:.1%}<br>: %{text}',
                 textfont={'size': 15},
                 texttemplate='%{text}'), row=1, col=1)
fig.add_trace(go.Pie(labels=df_COL_plot['Category'], values=df_COL_plot['Percentage'], hole=0.4,
                 text=df_COL_plot['Category']+': <br>' + df_COL_plot['Raw_number'].astype(str)+
                 ' ('+df_COL_plot['Raw_Percentage'].apply(format_percentage)+')',
                 textinfo='percent+text',
                 marker={'colors': colors},
                 hovertemplate='%{label}<br>Current percentage: %{percent:.1%}<br>: %{text}',
                 textfont={'size': 15},
                 texttemplate='%{text}'), row=1, col=2)
pio.write_html(fig, '/nfs/research/goldman/zihao/Code/jupyterLab/Project_2_vircolComp/2.mapleComp_P3/Figure/P3-all.html')

## Plot for COVID-19 Data Portal Alignment
fig = make_subplots(rows=1, cols=2, subplot_titles=['Viridian Alignment', 'COVID-19 Data Portal Alignment'], 
                    specs=[[{'type':'domain'}, {'type':'domain'}]])
fig.add_trace(go.Pie(labels=label_err, values=df_VIR_ERR_plot['Percentage'], hole=0.35,
                     text=df_VIR_ERR_plot['Raw_number'].astype(str) + ' (' + df_VIR_ERR_plot['Percentage'].apply(format_percentage) + ')',
                     textinfo='percent+text',
                     marker={'colors': colors_ERROR},
                     hovertemplate='%{label}<br>Current percentage: %{percent:.1%}<br>: %{text}',
                     textfont={'size': 15},
                     texttemplate='%{text}'
                    ), 
              row=1, col=1)
fig.add_trace(go.Pie(labels=label_err, values=df_COL_ERR_plot['Percentage'], hole=0.35,
                     text=df_COL_ERR_plot['Raw_number'].astype(str) + ' (' + df_COL_ERR_plot['Percentage'].apply(format_percentage) + ')',
                     textinfo='percent+text',
                     marker={'colors': colors_ERROR},
                     hovertemplate='%{label}<br>Current percentage: %{percent:.1%}<br>: %{text}',
                     textfont={'size': 15},
                     texttemplate='%{text}'
                    ), 
              row=1, col=2)
pio.write_html(fig, '/nfs/research/goldman/zihao/Code/jupyterLab/Project_2_vircolComp/2.mapleComp_P3/Figure/P3-err.html')
