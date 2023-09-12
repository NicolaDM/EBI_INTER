import os
import pandas as pd
from multiprocessing import Pool, cpu_count, Manager

# ==================Requires modification==================
# folder_path：input folder
# ==================Requires modification==================
folder_path = "/nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_2_combination/folderData_addInfo"

# Get all file names in the folder
file_names = os.listdir(folder_path)

def process_file(file_name):
    file_path = os.path.join(folder_path, file_name)
    df = pd.read_csv(file_path, sep='\t')

    # Calculate label counts for each file
    count_label_2 = ((df['label_mar'] == 1) & (df['label_ori'] == 0)).sum()
    count_label_4 = (df['label_same'] == 1).sum()
    count_label_5 = (df['label_same'] == 0).sum()
    label_4_5_record = ((df['label_same'] == 0) | (df['label_same'] == 1)).sum()

    return count_label_2, count_label_4, count_label_5, label_4_5_record

def main():
    with Pool(cpu_count()) as pool:
        results = pool.map(process_file, file_names)

    # Aggregate results
    count_label_2_total = sum(result[0] for result in results)
    count_label_4_total = sum(result[1] for result in results)
    count_label_5_total = sum(result[2] for result in results)
    label_4_5_record_total = sum(result[3] for result in results)

    # Print the total counts
    total_files = len(file_names)
    total_records = count_label_2_total + count_label_4_total + count_label_5_total

    print("Martin version masked & Portal unmasked:", count_label_2_total, ', Total number:', (29903 * total_files))
    print("Same nucleotide type:", count_label_4_total, ', Total number:', label_4_5_record_total)
    print("Different nucleotide type:", count_label_5_total, ', Total number:', label_4_5_record_total)
    print('Total records: ', total_records)
    print('================================= percentage =================================')
    print("Martin version masked & Portal unmasked:", round(count_label_2_total / total_records * 100, 3), '%')
    print("Same nucleotide type:", round(count_label_4_total / total_records * 100, 3), '%')
    print("Different nucleotide type:", round(count_label_5_total / total_records * 100, 3), '%')

if __name__ == "__main__":
    main()

