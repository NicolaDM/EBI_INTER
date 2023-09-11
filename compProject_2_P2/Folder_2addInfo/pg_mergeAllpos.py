import os
import pandas as pd
import numpy as np
import argparse
from multiprocessing import Pool, cpu_count, Manager
import glob

def read_sequence(file_path):
    '''This function reads a FASTA file and returns a pandas DataFrame where
    each row corresponds to the base and its position in the sequence'''
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    sequence = ''.join(lines[1:]).replace('\n', '')
    sequence_list = [{'position': i+1, 'nucleotide': base} for i, base in enumerate(sequence)]

    return pd.DataFrame(sequence_list)

def process_file(file_name, folder_path_1, folder_path_2, output_folder, batch_index, missing_cov_ids, missing_ann_ids):
    try:
        file_path_1 = os.path.join(folder_path_1, file_name)
        df1 = read_sequence(file_path_1)
        df1.rename(columns={'nucleotide': 'nucleotide_martin'}, inplace=True)

        file_path_2 = os.path.join(folder_path_2, file_name)
        if not os.path.exists(file_path_2):
            missing_id = file_name.split('.')[0]
            with open(os.path.join(missing_folder_1, f'missing_ids_{batch_index}.txt'), 'a') as missing_file:
                missing_file.write(f"{missing_id}\n")
            return

        df2 = read_sequence(file_path_2)
        df2.rename(columns={'nucleotide': 'nucleotide_origin'}, inplace=True)

        merged_df = pd.merge(df1, df2, on='position')

        merged_df['label_masked'] = np.where((merged_df['nucleotide_martin'].isin(['-', 'n', 'm', 'r', 'w', 's', 'y', 'k', 'v', 'h', 'd', 'b'])) & (merged_df['nucleotide_origin'].isin(['-', 'n'])), 1, 0)
        merged_df['label_mar'] = np.where(merged_df['nucleotide_martin'].isin(['-', 'n', 'm', 'r', 'w', 's', 'y', 'k', 'v', 'h', 'd', 'b']), 1, 0)
        merged_df['label_ori'] = np.where(merged_df['nucleotide_origin'].isin(['-', 'n']), 1, 0)
        merged_df['label_same'] = np.where((merged_df['nucleotide_martin'] == merged_df['nucleotide_origin']),
                                           np.where(merged_df['nucleotide_martin'].isin(['-', 'n', 'm', 'r', 'w', 's', 'y', 'k', 'v', 'h', 'd', 'b']), 2, 1),
                                           np.where((merged_df['label_masked'] == 1) | (merged_df['label_mar'] == 1) | (merged_df['label_ori'] == 1), 2, 0))

        process_merged_df(file_name, merged_df, output_folder, missing_cov_ids, missing_ann_ids)

    except Exception as e:
        print(f"Error processing {file_name}. Error: {e}")

def process_merged_df(file_name, merged_df, output_folder, missing_cov_ids, missing_ann_ids):
    try:
        basename = os.path.basename(file_name)
        id = basename[:-4]

        df_cov_path = f"/nfs/research/goldman/zihao/Datas/p1/File_5_coverage/Decompress/{id}_coverage.txt"
        if not os.path.exists(df_cov_path):
            missing_cov_ids.append(id)
            return
        df_cov = pd.read_csv(df_cov_path, sep='\t')

        df_ann_path = f"/nfs/research/goldman/zihao/Datas/p1/File_5_annot/New_Decompress/{id}_annot.txt"
        if not os.path.exists(df_ann_path):
            missing_ann_ids.append(id)
            return
        df_ann = pd.read_csv(df_ann_path, sep='\t')

        df_merge = pd.concat([merged_df, df_cov['RATIO'], df_ann['AF'], df_ann['SB']], axis=1)

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        df_merge.to_csv(os.path.join(output_folder, file_name), index=False, sep='\t')

    except Exception as e:
        print(f"An error occurred while processing {file_name}: {e}")

def process_batch(file_names, folder_path_1, folder_path_2, output_folder, batch_index, missing_cov_ids, missing_ann_ids):
    if not os.path.exists(missing_folder_1):
        os.makedirs(missing_folder_1, exist_ok=True)
    if not os.path.exists(missing_folder_2):
        os.makedirs(missing_folder_2, exist_ok=True)
    with open(os.path.join(missing_folder_1, f'missing_ids_{batch_index}.txt'), 'a') as f:
        pass
    with Pool(cpu_count()) as pool:
        pool.starmap(process_file, [(file_name, folder_path_1, folder_path_2, output_folder, batch_index, missing_cov_ids, missing_ann_ids) for file_name in file_names])

def main(folder_path_1, folder_path_2, output_folder, batch_index, batch_size):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder, exist_ok=True)
    
    file_names = sorted(os.listdir(folder_path_1))
    
    start_index = (batch_index - 1) * batch_size
    end_index = start_index + batch_size
    current_batch_files = file_names[start_index:end_index]
    
    with Manager() as manager:
        missing_cov_ids = manager.list()
        missing_ann_ids = manager.list()
        
        process_batch(current_batch_files, folder_path_1, folder_path_2, output_folder, batch_index, missing_cov_ids, missing_ann_ids)

        # Convert shared lists back to normal lists
        missing_cov_ids = list(missing_cov_ids)
        missing_ann_ids = list(missing_ann_ids)
        
    # Save missing ids to files
    with open(os.path.join(missing_folder_2, f'missing_cov_ids_{batch_index}.txt'), 'w') as f:
        for id in missing_cov_ids:
            f.write(f"{id}\n")

    with open(os.path.join(missing_folder_2, f'missing_ann_ids_{batch_index}.txt'), 'w') as f:
        for id in missing_ann_ids:
            f.write(f"{id}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a batch of FASTA files.')
    parser.add_argument('folder_path_1', type=str, help='Path to the Viridian Assembly\'s FASTA files.')
    parser.add_argument('folder_path_2', type=str, help='Path to the Colman Assembly\'s FASTA files.')
    parser.add_argument('output_folder', type=str, help='The output folder.')
    parser.add_argument('batch_index', type=int, help='The batch index to process.')
    parser.add_argument('batch_size', type=int, help='The size of each batch.')

    args = parser.parse_args()
    missing_folder_1 = '/nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_2_combination/folderData_MissingID'
    missing_folder_2 = '/nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_2_combination/folderData_missingID—COVAF'

    main(args.folder_path_1, args.folder_path_2, args.output_folder, args.batch_index, args.batch_size)

