import os
import pandas as pd

def read_file(file_path, delimiter='\t'):
    """Reads a file into a pandas DataFrame."""
    return pd.read_csv(file_path, delimiter=delimiter)

def fetch_file_path(folder_path, file_id, extension='.txt'):
    """Builds the file path from the folder path and file id."""
    return os.path.join(folder_path, f'{file_id}{extension}')

def match_row(df, column, value):
    """Finds rows in a DataFrame that match a specific value in a specific column."""
    return df[df[column] == value]

def append_columns(df_source, df_target, index, columns):
    """Appends columns from a source DataFrame to a target DataFrame."""
    df_target.loc[index, columns] = df_source[columns].values.tolist()[0]

def save_file(df, file_path, columns, delimiter='\t', index=False):
    """Saves a DataFrame to a file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df[columns].to_csv(file_path, sep=delimiter, index=index)

# Specify paths and column names
a_file_path = '/nfs/research/goldman/zihao/Datas/p2_compViridian_P3/Folder_mapleOutput/COL_output_modified.txt'
# a_file_path = '/nfs/research/goldman/zihao/errorsProject_1/MAPLE/new_version_MAY/output_modified.txt'

b_folder_path = "/nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_3_mergeINFO/folderData_mergeFile"
b_column_names = ['position', 'nucleotide_martin', 'nucleotide_origin', 'label_masked', 'label_mar', 'label_ori', 'label_same', 'RATIO', 'AF', 'SB']
output_file_path = '/nfs/research/goldman/zihao/Datas/p2_comp_viridian/Folder_3_mergeINFO/errpos_outputData.txt'
missing_b_file_path = '/nfs/research/goldman/zihao/Datas/p2_comp_viridian/Folder_3_mergeINFO/Folder_missingData/errPos_missingFiles.txt'
missing_rows_file_path = '/nfs/research/goldman/zihao/Datas/p2_comp_viridian/Folder_3_mergeINFO/Folder_missingData/errPos_missingPos.txt'

# Load the data from the 'A' file
a_data = read_file(a_file_path)

# Open missing files loggers
os.makedirs(os.path.dirname(missing_b_file_path), exist_ok=True)
os.makedirs(os.path.dirname(missing_rows_file_path), exist_ok=True)

missing_b_files_count = 0
missing_rows_count = 0

with open(missing_b_file_path, 'w') as missing_b_file, open(missing_rows_file_path, 'w') as missing_rows_file:

    # Iterate through each row of the 'A' data
    for index, row in a_data.iterrows():
        # Fetch the path of the corresponding 'B' file
        b_file_path = fetch_file_path(b_folder_path, row['ID'])
    
        # Continue to the next iteration if the 'B' file doesn't exist
        if not os.path.isfile(b_file_path):
            missing_b_file.write(f'{row["ID"]}\n')
            missing_b_files_count += 1
            continue

        # Load the data from the 'B' file
        b_data = read_file(b_file_path)

        # Find the matching row in the 'B' data
        matched_row = match_row(b_data, 'position', row['Position'])

        # Continue to the next iteration if no matching row was found
        if matched_row.empty:
            missing_rows_file.write(f'{row["ID"]}\t{row["Position"]}\n')
            missing_rows_count += 1
            continue

        # Append the necessary columns to the 'A' data
        append_columns(matched_row, a_data, index, b_column_names)

# Save the modified 'A' data
save_file(a_data, output_file_path, ['ID', 'Position'] + b_column_names)

print(f"Data saved to {output_file_path}")
print(f"{missing_b_files_count} ID of the file with the missing merge information (SB, AF) is saved to {missing_b_file_path}")
print(f"Missing row IDs and Positions saved to {missing_rows_file_path}")
