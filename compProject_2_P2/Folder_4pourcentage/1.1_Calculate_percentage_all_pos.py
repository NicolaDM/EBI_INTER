import os
import pandas as pd

folder_path = "/nfs/research/goldman/zihao/Datas/p2_comp_viridian/3_combination"

# Get all file names in the folder
file_names = os.listdir(folder_path)

# Initialize count variables
count_label_2_total = 0
count_label_4_total = 0
count_label_5_total = 0
label_4_5_record_total = 0

# Iterate over each file in the file list
for file_name in file_names:
    file_path = os.path.join(folder_path, file_name)
    df = pd.read_csv(file_path, sep='\t')

    # Calculate label counts for each file
    # count_label_2 = (df['label_mar'] == 1).sum()
    count_label_2 = ((df['label_mar'] == 1) & (df['label_ori'] == 0)).sum()
    count_label_4 = (df['label_same'] == 1).sum()
    count_label_5 = (df['label_same'] == 0).sum()
    label_4_5_record = ((df['label_same'] == 0) | (df['label_same'] == 1)).sum()

    # Accumulate counts to total count variables
    count_label_2_total += count_label_2
    count_label_4_total += count_label_4
    count_label_5_total += count_label_5
    label_4_5_record_total += label_4_5_record

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
