import os
import glob
import pandas as pd

# ==================Requires modification==================
# checkid_file：MAPLE's input is used to detect IDs without corresponding information（AF）
# missingID_dir：Location to save missing IDs
# output_dir：Location to save processed files
# ==================Requires modification==================
checkid_file = "/nfs/research/goldman/zihao/Datas/p2_comp_viridian/2_alignment/Col_MAPLE_format_consensuses.txt"
id_set = set()
is_first_line = True

with open(checkid_file, 'r') as f:
    for line in f:
        line = line.strip()
        if line.startswith('>'):
            if is_first_line:
                is_first_line = False
            else:
                id_set.add(line[1:])
print('=========================== information =========================== ')
print("Number of samples for MAPLE input: ", len(id_set))

folder1_files = glob.glob('/nfs/research/goldman/zihao/Datas/p1/File_5_annot/Folder_Decompress_forP4/*.txt')
folder2_files = glob.glob('/nfs/research/goldman/zihao/Datas/p2_comp_viridian/3_combination/*.txt')

folder1_files_dict = {os.path.basename(path).split('_')[0]: path for path in folder1_files}
folder2_files_dict = {os.path.basename(path).split('.')[0]: path for path in folder2_files}

missingID_dir = '/nfs/research/goldman/zihao/Datas/p1_errorsProject_P4/Folder_treatedAF/Folder_missingID'
if not os.path.exists(missingID_dir):
    os.mkdir(missingID_dir)

missing_id_file_path = f"{missingID_dir}/missing_file1_ids.txt"
missing_file2_id_file_path = f"{missingID_dir}/missing_file2_ids.txt"

missing_id_file = open(missing_id_file_path, "w")
missing_file2_id_file = open(missing_file2_id_file_path, "w")

print("Path for the missing_file1_ids.txt:", missing_id_file_path)
print("Path for the missing_file2_ids.txt:", missing_file2_id_file_path)

output_dir = '/nfs/research/goldman/zihao/Datas/p1_errorsProject_P4/Folder_treatedAF/folderData_treatedFile'
if not os.path.exists(output_dir):
    os.mkdir(output_dir)

for id in id_set:
    if id not in folder1_files_dict:
        missing_id_file.write(id + '\t')
        continue
    if id in folder1_files_dict and id not in folder2_files_dict:
        missing_file2_id_file.write(id + '\t')
        continue

    file1 = folder1_files_dict[id]
    file2 = folder2_files_dict[id]

    df1 = pd.read_csv(file1, delimiter='\t')
    df2 = pd.read_csv(file2, delimiter='\t')
    df1 = df1[df1['AF'] > 0].drop('SB', axis=1)
    df1['AF2'] = 1 - df1['AF']
    df = pd.merge(df1, df2, left_on='POS', right_on='position', how='inner')
    df = df[['POS', 'REF', 'ALT', 'AF', 'AF2', 'nucleotide_martin', 'nucleotide_origin']]
    df[['nucleotide_martin', 'nucleotide_origin']] = df[['nucleotide_martin', 'nucleotide_origin']].applymap(lambda x: x.upper() if isinstance(x, str) else x)
    
    df.to_csv(f'{output_dir}/merged_{id}.txt', sep='\t', index=False)



##############################################
## Number of missing statistics
##############################################

def count_ids_in_file(filepath):
    # Initialize the counter
    count = 0

    # Open the file and count the ids
    with open(filepath, 'r') as file:
        for line in file:
            ids_in_line = line.strip().split('\t')
            count += len(ids_in_line)

    # Return the count
    return count

missing_id_file.close()
missing_file2_id_file.close()

# Example usage
print("The number of missing files when merging Annot files:", count_ids_in_file(missing_id_file_path))
print("The number of missing files when merging Coverage files:", count_ids_in_file(missing_file2_id_file_path))



