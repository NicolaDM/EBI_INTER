import os
import pandas as pd
from multiprocessing import Pool, cpu_count, Manager
# ==================Requires modification==================
# folder_path：input folder
# ==================Requires modification==================
folder_path = "/nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_2_combination/folderData_addInfo"

# Get all file names in the folder
file_names = os.listdir(folder_path)

threshold_AF = 0.001
threshold_SB = 0
threshold_COV = 0.1

def count_statistics(df, columns, label, flag_name, count_dict):
    df_label = df[df[columns] == label]
    count_dict[flag_name + '_count'] += len(df_label)
    
    count_dict['Flag_SB_PASSED'] += df_label[(df_label['Flag_SB'] == 1) & (df_label['Flag_AF'] == 0) & (df_label['Flag_COV'] == 0)].shape[0]
    count_dict['Flag_AF_PASSED'] += df_label[(df_label['Flag_SB'] == 0) & (df_label['Flag_AF'] == 1) & (df_label['Flag_COV'] == 0)].shape[0]
    count_dict['Flag_COV_PASSED'] += df_label[(df_label['Flag_SB'] == 0) & (df_label['Flag_AF'] == 0) & (df_label['Flag_COV'] == 1)].shape[0]

    count_dict['both_PASSED'] += df_label[(df_label['Flag_SB'] == 1) & (df_label['Flag_AF'] == 1) & (df_label['Flag_COV'] == 1)].shape[0]
    count_dict['both_UNPASSED'] += df_label[(df_label['Flag_SB'] == 0) & (df_label['Flag_AF'] == 0) & (df_label['Flag_COV'] == 0)].shape[0]

    count_dict['Flag_AF_SB_PASSED'] += df_label[(df_label['Flag_SB'] == 1) & (df_label['Flag_AF'] == 1) & (df_label['Flag_COV'] == 0)].shape[0]
    count_dict['Flag_AF_COV_PASSED'] += df_label[(df_label['Flag_SB'] == 0) & (df_label['Flag_AF'] == 1) & (df_label['Flag_COV'] == 1)].shape[0]
    count_dict['Flag_SB_COV_PASSED'] += df_label[(df_label['Flag_SB'] == 1) & (df_label['Flag_AF'] == 0) & (df_label['Flag_COV'] == 1)].shape[0]

def process_file(file_name):
    local_count_dict = {
        'same_count': 0,
        'Flag_SB_PASSED': 0,
        'Flag_AF_PASSED': 0,
        'Flag_COV_PASSED': 0,
        'both_PASSED': 0,
        'both_UNPASSED': 0,
        'Flag_AF_SB_PASSED': 0,
        'Flag_SB_COV_PASSED': 0,
        'Flag_AF_COV_PASSED': 0,
    }
    
    df = pd.read_csv(os.path.join(folder_path, file_name), sep = '\t')

    df['Flag_SB'] = (df['SB'].astype(float) > threshold_SB).astype(int)
    df['Flag_AF'] = (df['AF'].astype(float) > threshold_AF).astype(int)
    df['Flag_COV'] = (df['RATIO'].astype(float) < threshold_COV).astype(int)

    count_statistics(df, 'label_same', 1, 'same', local_count_dict)  # 'Same nucleotide'

    return local_count_dict

def main():
    with Pool(cpu_count()) as pool:
        results = pool.map(process_file, file_names)

    # Merge results
    merged_dict = {
        'same_count': 0,
        'Flag_SB_PASSED': 0,
        'Flag_AF_PASSED': 0,
        'Flag_COV_PASSED': 0,
        'both_PASSED': 0,
        'both_UNPASSED': 0,
        'Flag_AF_SB_PASSED': 0,
        'Flag_SB_COV_PASSED': 0,
        'Flag_AF_COV_PASSED': 0,
    }
    for result in results:
        for key in merged_dict:
            merged_dict[key] += result[key]

    # Print the results
    print("========================= Information =========================")
    for key, value in merged_dict.items():
        print(f'{key}: {value}')

if __name__ == "__main__":
    main()

    
