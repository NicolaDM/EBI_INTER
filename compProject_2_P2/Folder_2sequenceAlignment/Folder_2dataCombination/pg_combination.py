import os
import pandas as pd
import numpy as np
import argparse

def read_sequence(file_path):
    '''This function reads a FASTA file and returns a pandas DataFrame where
    each row corresponds to the base and its position in the sequence'''
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    sequence = ''.join(lines[1:]).replace('\n', '')
    sequence_list = [{'position': i+1, 'nucleotide': base} for i, base in enumerate(sequence)]

    return pd.DataFrame(sequence_list)

def process_batch(file_names, folder_path_1, folder_path_2, output_folder, batch_index):
    missing_folder = '/nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_2_combination/folderData_MissingID'
    if not os.path.exists(missing_folder):
        os.makedirs(missing_folder)
    missing_file_path = os.path.join(missing_folder, f"{batch_index}.txt")

    for file_name in file_names:
        try:
            file_path_1 = os.path.join(folder_path_1, file_name)
            df1 = read_sequence(file_path_1)
            df1.rename(columns={'nucleotide': 'nucleotide_martin'}, inplace=True)

            file_path_2 = os.path.join(folder_path_2, file_name)
            if not os.path.exists(file_path_2):
                with open(missing_file_path, 'a') as missing_file:
                    missing_id = file_name.split('.')[0]  # Assuming IDs are the name of the file before the extension
                    missing_file.write(f"{missing_id}\n")
                del df1
                continue

            df2 = read_sequence(file_path_2)
            df2.rename(columns={'nucleotide': 'nucleotide_origin'}, inplace=True)

            merged_df = pd.merge(df1, df2, on='position')

            merged_df['label_masked']=np.where((merged_df['nucleotide_martin'].isin(['-','n','m','r','w','s','y','k','v','h','d','b']))&(merged_df['nucleotide_origin'].isin(['-','n'])),1,0)
            merged_df['label_mar']=np.where(merged_df['nucleotide_martin'].isin(['-','n','m','r','w','s','y','k','v','h','d','b']),1,0)
            merged_df['label_ori']=np.where(merged_df['nucleotide_origin'].isin(['-','n']),1,0)
            merged_df['label_same']=np.where((merged_df['nucleotide_martin']==merged_df['nucleotide_origin']),
                                            np.where(merged_df['nucleotide_martin'].isin(['-','n','m','r','w','s','y','k','v','h','d','b']),2,1),
                                            np.where((merged_df['label_masked']==1)|(merged_df['label_mar']==1)|(merged_df['label_ori']==1),2,0))

            if os.path.exists(os.path.join(output_folder, file_name)):
                del df1
                del df2
                del merged_df
                continue

            merged_df.to_csv(os.path.join(output_folder, file_name), sep='\t', index=False)

            del df1
            del df2
            del merged_df

        except Exception as e:
            print(f"Error processing {file_name}. Error: {e}")

def main(folder_path_1, folder_path_2, output_folder, batch_index, batch_size):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    file_names = sorted(os.listdir(folder_path_1))
    
    start_index = (batch_index - 1) * batch_size
    end_index = start_index + batch_size
    current_batch_files = file_names[start_index:end_index]
    
    process_batch(current_batch_files, folder_path_1, folder_path_2, output_folder, batch_index)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a batch of FASTA files.')
    parser.add_argument('folder_path_1', type=str, help='Path to the Viridian Assembly\'s FASTA files.')
    parser.add_argument('folder_path_2', type=str, help='Path to the Colman Assembly\'s FASTA files.')
    parser.add_argument('output_folder', type=str, help='The output folder.')
    parser.add_argument('batch_index', type=int, help='The batch index to process.')
    parser.add_argument('batch_size', type=int, help='The size of each batch.')

    args = parser.parse_args()
    main(args.folder_path_1, args.folder_path_2, args.output_folder, args.batch_index, args.batch_size)
