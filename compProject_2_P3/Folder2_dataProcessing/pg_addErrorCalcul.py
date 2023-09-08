import pandas as pd
import os
import numpy as np
# import time

def combine_assemblies(folder_col, folder_vir, folder_data, not_found_ids_file):
    # start_time = time.time()

    # 1. Combine the Colman's Assembly and Viridian Assembly
    df_col = pd.read_csv(folder_col, sep='\t')
    df_vir = pd.read_csv(folder_vir, sep='\t')

    df_vir['VIR'] = 1
    df_col['COL'] = 1
    merged_df = pd.merge(df_vir, df_col, on=['ID','Position'], how='outer')
    df_filled = merged_df.fillna(0)

    df_filled['COL'] = df_filled['COL'].astype(int)
    df_filled['VIR'] = df_filled['VIR'].astype(int)

    # Store not found IDs
    not_found_ids = []

    # Variables for statistics
    num_viridian_masked = 0
    num_colman_masked = 0
    
    num_viridian_unmasked_no_error = 0
    num_colman_unmasked_no_error = 0
    
    num_viridian_error = 0
    num_colman_error = 0
    #======================
    NB_VIR_masked = 0
    NB_VIR_sameError = 0
    NB_VIR_same = 0
    NB_VIR_diffError = 0
    NB_VIR_diff = 0
    
    NB_COL_masked = 0
    NB_COL_sameError = 0
    NB_COL_same = 0
    NB_COL_diffError = 0
    NB_COL_diff = 0  

    # Get the names of all the files in the folder (without extensions)
    existing_files = {os.path.splitext(f)[0] for f in os.listdir(folder_data)}

    # Using isin for efficient lookup
    ids_in_existing_files = df_filled['ID'].isin(existing_files)
    for index, row in df_filled[ids_in_existing_files].iterrows():
        file_path = f'{folder_data}/{row["ID"]}.txt'
        df = pd.read_csv(file_path, sep='\t')[['position', 'nucleotide_martin', 'nucleotide_origin', 'label_mar', 'label_ori']]

        # Using isin for efficient position lookup
        if row['Position'] in df['position'].values:
            df.loc[df['position'] == row['Position'], 'VIR'] = row['VIR']
            df.loc[df['position'] == row['Position'], 'COL'] = row['COL']

            # Process the dataframe as in the second snippet
            df_v1 = df.fillna(0)
            df_v1["VIR"] = df_v1["VIR"].astype(int)
            df_v1["COL"] = df_v1["COL"].astype(int)
            
            # Process the dataframe as in the second snippet
            df_v1 = df.fillna(0)
            df_v1["VIR"] = df_v1["VIR"].astype(int)
            df_v1["COL"] = df_v1["COL"].astype(int)
            num_viridian_masked += sum(df_v1['label_mar'] == 1)
            num_colman_masked += sum(df_v1['label_ori'] == 1)
            num_viridian_unmasked_no_error += sum((df_v1['label_mar'] == 0) & (df_v1['VIR'] == 0))
            num_colman_unmasked_no_error += sum((df_v1['label_ori'] == 0) & (df_v1['COL'] == 0))
            num_viridian_error += sum(df_v1['VIR'] == 1)
            num_colman_error += sum(df_v1['COL'] == 1)
            #======================
            NB_COL_masked += sum((df_v1['COL'] == 1) & (df_v1['label_mar'] == 1))
            NB_COL_sameError += sum((df_v1['COL'] == 1) & (df_v1['VIR'] == 1) & (df_v1['label_ori'] == 0) & (df_v1['label_mar'] == 0) &(df_v1['nucleotide_martin'] == df_v1['nucleotide_origin']))
            NB_COL_same += sum((df_v1['COL'] == 1) & (df_v1['VIR'] == 0) & (df_v1['label_ori'] == 0) & (df_v1['label_mar'] == 0) &(df_v1['nucleotide_martin'] == df_v1['nucleotide_origin']))
            NB_COL_diffError += sum((df_v1['COL'] == 1) & (df_v1['VIR'] == 1) & (df_v1['label_ori'] == 0) & (df_v1['label_mar'] == 0) &(df_v1['nucleotide_martin'] != df_v1['nucleotide_origin']))
            NB_COL_diff += sum((df_v1['COL'] == 1) & (df_v1['VIR'] == 0) & (df_v1['label_ori'] == 0) & (df_v1['label_mar'] == 0) &(df_v1['nucleotide_martin'] != df_v1['nucleotide_origin']))
            

            NB_VIR_masked += sum((df_v1['VIR'] == 1) & (df_v1['label_ori'] == 1))
            NB_VIR_sameError += sum((df_v1['VIR'] == 1) & (df_v1['COL'] == 1) & (df_v1['label_ori'] == 0) & (df_v1['label_mar'] == 0) &(df_v1['nucleotide_martin'] == df_v1['nucleotide_origin']))
            NB_VIR_same += sum((df_v1['VIR'] == 1) & (df_v1['COL'] == 0) & (df_v1['label_ori'] == 0) & (df_v1['label_mar'] == 0) &(df_v1['nucleotide_martin'] == df_v1['nucleotide_origin']))
            NB_VIR_diffError += sum((df_v1['VIR'] == 1) & (df_v1['COL'] == 1) & (df_v1['label_ori'] == 0) & (df_v1['label_mar'] == 0) &(df_v1['nucleotide_martin'] != df_v1['nucleotide_origin']))
            NB_VIR_diff += sum((df_v1['VIR'] == 1) & (df_v1['COL'] == 0) & (df_v1['label_ori'] == 0) & (df_v1['label_mar'] == 0) &(df_v1['nucleotide_martin'] != df_v1['nucleotide_origin']))
            
        else:
            not_found_ids.append(row["ID"])

    # IDs not in existing files
    not_found_ids.extend(df_filled.loc[~ids_in_existing_files, 'ID'].tolist())

    # Check if parent folder of not_found_ids_file exists and create if it does not
    if not os.path.exists(os.path.dirname(not_found_ids_file)):
        os.makedirs(os.path.dirname(not_found_ids_file))

    # Save not found IDs to a file
    with open(not_found_ids_file, 'w') as f:
        for item in not_found_ids:
            f.write("%s\n" % item)

    # Print the location of not_found_ids_file
    print(f"The not found IDs file has been saved to: {not_found_ids_file}")

    # Print the number of not found IDs
    print(f"The number of not found IDs: {len(not_found_ids)}")

    # Print the statistics
    print('====================== Info ======================')
    print('Total masked positions in Virdian assembly: ', num_viridian_masked)
    print('Total positions in Colman assembly: ', num_colman_masked)
    
    print('====================== Info ======================')
    print('Total unmasked positions in Virdian assembly, without errors '
          'identified by MAPLE: ', num_viridian_unmasked_no_error)
    print('Total unmasked positions in Colman assembly, without errors '
          'identified by MAPLE: ', num_colman_unmasked_no_error)
    
    print('====================== Info ======================')
    print('Total positions in Virdian assembly identified as errors by MAPLE '
          '(Virdian\'s errors): ', num_viridian_error)
    print('Total positions in Colman assembly identified as errors by MAPLE '
          '(Colman\'s errors): ', num_colman_error)
    
    print('====================== For VIR error ======================')
    print('Colman’s assemblies are masked: ',NB_VIR_masked)
    print('Same nucleotide, Colman’s assembly error: ',NB_VIR_sameError)
    print('Same nucleotide, Colman’s assembly not error: ',NB_VIR_same)
    print('Diff nucleotide, Colman’s assembly error: ',NB_VIR_diffError)
    print('Diff nucleotide, Colman’s assembly not error: ',NB_VIR_diff)
    print('====================== For COL error ======================')
    print('Viridian’s assemblies are masked: ',NB_COL_masked)
    print('Same nucleotide, Viridian\'s assembly error: ',NB_COL_sameError)
    print('Same nucleotide, Viridian\'s assembly not error: ',NB_COL_same)
    print('Diff nucleotide, Viridian\'s assembly error: ',NB_COL_diffError)
    print('Diff nucleotide, Viridian\'s assembly not error: ',NB_COL_diff)

    # print(f"Time taken for the entire function: {time.time() - start_time:.2f} seconds")

folder_col = '/nfs/research/goldman/zihao/Datas/p2_compViridian_P3/Folder_mapleOutput/COL_output_modified.txt'
folder_vir = '/nfs/research/goldman/zihao/Datas/p2_compViridian_P3/Folder_mapleOutput/VIR_output_modified.txt'
folder_data = '/nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_2_combination/folderData_combination'
not_found_ids_file = '/nfs/research/goldman/zihao/Datas/p2_compViridian_P3/notFound_idsError.txt'

combine_assemblies(folder_col, folder_vir, folder_data, not_found_ids_file)

