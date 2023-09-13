import pandas as pd
import os
import numpy as np
from multiprocessing import Pool, cpu_count, Manager, Lock

def process_chunk(args):
    chunk, folder_data, not_found_ids, stats = args
    not_found_ids_local = set()  # using set to collect not_found_ids[avoid duplicate]
    num_viridian_masked = 0
    num_colman_masked = 0
    num_viridian_unmasked_no_error = 0
    num_colman_unmasked_no_error = 0
    num_viridian_error = 0
    num_colman_error = 0
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

    chunk_ids_set = set(chunk['ID'].values)

    existing_files = {os.path.splitext(f)[0] for f in os.listdir(folder_data)}

    for file_id in existing_files:
        file_path = f'{folder_data}/{file_id}.txt'
        df = pd.read_csv(file_path, sep='\t')[['position', 'nucleotide_martin', 'nucleotide_origin', 'label_mar', 'label_ori']]

        if file_id in chunk_ids_set:
            row = chunk[chunk['ID'] == file_id].iloc[0]
            if row['Position'] in df['position'].values:
                df.loc[df['position'] == row['Position'], 'VIR'] = row['VIR']
                df.loc[df['position'] == row['Position'], 'COL'] = row['COL']
            else:
                not_found_ids.add(file_id)
        else:
            df['COL'] = np.nan  # Add 'COL' column with NaN
            df['VIR'] = np.nan  # Add 'VIR' column with NaN

        df_v1 = df.fillna(0)
        df_v1["VIR"] = df_v1["VIR"].astype(int)
        df_v1["COL"] = df_v1["COL"].astype(int)
        num_viridian_masked += sum(df_v1['label_mar'] == 1)
        num_colman_masked += sum(df_v1['label_ori'] == 1)
        num_viridian_unmasked_no_error += sum((df_v1['label_mar'] == 0) & (df_v1['VIR'] == 0))
        num_colman_unmasked_no_error += sum((df_v1['label_ori'] == 0) & (df_v1['COL'] == 0))
        num_viridian_error += sum(df_v1['VIR'] == 1)
        num_colman_error += sum(df_v1['COL'] == 1)
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

    # Update shared data structures
    with lock:
        not_found_ids.extend(list(not_found_ids_local))
        for i in range(17):
            stats[i] += local_stats[i]

    return None

def combine_assemblies(folder_col, folder_vir, folder_data, not_found_ids_file):
    df_col = pd.read_csv(folder_col, sep='\t')
    df_vir = pd.read_csv(folder_vir, sep='\t')
    df_vir['VIR'] = 1
    df_col['COL'] = 1
    merged_df = pd.merge(df_vir, df_col, on=['ID','Position'], how='outer')
    df_filled = merged_df.fillna(0)
    df_filled['COL'] = df_filled['COL'].astype(int)
    df_filled['VIR'] = df_filled['VIR'].astype(int)

    global lock
    lock = Lock()

    # Use set to ensure that each file appears only once in a block
    existing_files = list(set({os.path.splitext(f)[0] for f in os.listdir(folder_data)}))

    # Split the existing_files into chunks
    chunk_size = len(existing_files) // cpu_count()
    chunks = [existing_files[i:i + chunk_size] for i in range(0, len(existing_files), chunk_size)]

    # Create shared data structures using Manager
    manager = Manager()
    all_not_found_ids = manager.list()
    stats = manager.list([0] * 17)  # Initialize a list of zeros for 17 statistics

    # Process the chunks in parallel
    with Pool(cpu_count()) as pool:
        pool.map(process_chunk, [(df_filled[df_filled['ID'].isin(c)], folder_data, all_not_found_ids, stats) for c in chunks])

    # Convert shared data structures back to regular Python lists for further processing
    all_not_found_ids = list(all_not_found_ids)
    stats = list(stats)

    # Extract statistics from the stats list
    num_viridian_masked, num_colman_masked, num_viridian_unmasked_no_error, num_colman_unmasked_no_error, num_viridian_error, num_colman_error, NB_VIR_masked, NB_VIR_sameError, NB_VIR_same, NB_VIR_diffError, NB_VIR_diff, NB_COL_masked, NB_COL_sameError, NB_COL_same, NB_COL_diffError, NB_COL_diff = stats[1:]
    
    # Check if parent folder of not_found_ids_file exists and create if it does not
    if not os.path.exists(os.path.dirname(not_found_ids_file)):
        os.makedirs(os.path.dirname(not_found_ids_file))

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

folder_col = '/nfs/research/goldman/zihao/Datas/p2_compViridian_P3/Folder_mapleOutput/COL_output_modified.txt'
folder_vir = '/nfs/research/goldman/zihao/Datas/p2_compViridian_P3/Folder_mapleOutput/VIR_output_modified.txt'

folder_data = '/nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_2_combination/folderData_addInfo'
not_found_ids_file = '/nfs/research/goldman/zihao/Datas/p2_compViridian_P3/notFound_idsError.txt'

combine_assemblies(folder_col, folder_vir, folder_data, not_found_ids_file)

