import pandas as pd
import os
# ==================Requires modification==================
# File_mapleOutput：Processed MAPLE output file
# output_dir：Location to save processed files
# directory:Location to save missing IDs
# ==================Requires modification==================

File_mapleOutput = '/nfs/research/goldman/zihao/Datas/p2_compViridian_P3/Folder_mapleOutput/VIR_output_modified.txt'
# For colman
df_vir = pd.read_csv(File_mapleOutput, delimiter='\t')
df1 = df_vir

output_dir = '/nfs/research/goldman/zihao/Datas/p1_errorsProject_P4/Folder_combFor_errPos/'
# Check if the directory exists, if not, create it
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    
missing_ids_file = os.path.join(output_dir, 'missing_idsVir.txt')
output_csv_file = os.path.join(output_dir, 'errPos_combForvir.txt')

# Initialize the counter for missing IDs
missing_ids_count = 0

# Find the corresponding file by ID
def find_file(ID):
    global missing_ids_count
    directory = "/nfs/research/goldman/zihao/Datas/p1_errorsProject_P4/Folder_treatedAF/folderData_treatedFile/"
    filename = f"merged_{ID}.txt"
    path = os.path.join(directory, filename)
    if os.path.exists(path):
        return path
    else:
        with open(missing_ids_file, 'a') as f:
            f.write(f"{ID}\t")
            # Increment the counter whenever we encounter a missing ID
            missing_ids_count += 1
        return None

## Based on the Position column, 
## find the row corresponding to the POS column
def find_row(df, position):
    row = df[df['POS'] == position]
    if row.empty:
        return None
    else:
        return row[['REF', 'ALT', 'AF', 'nucleotide_martin']]

# New data boxes
new_rows = []
for index, row in df1.iterrows():
    file_path = find_file(row['ID'])
    if file_path:
        df = pd.read_csv(file_path, delimiter='\t')
        new_row = find_row(df, row['Position'])
        if new_row is not None:
            new_rows.append(new_row.iloc[0].values)
        else:
            new_rows.append([None, None, None, None])
    else:
        new_rows.append([None, None, None, None])

new_df = pd.DataFrame(new_rows, columns=['REF', 'ALT', 'AF', 'nucleotide_martin'])
df1 = pd.concat([df1, new_df], axis=1)
print(f"Writing to: {output_csv_file}")
df1 = df1.dropna()
df1.to_csv(output_csv_file, sep='\t', index=False)

# Print the total count of missing IDs and where they are written
print(f"Total count of missing IDs: {missing_ids_count}")
if missing_ids_count > 0:
    print(f"Missing IDs written to: {missing_ids_file}")