import pandas as pd
import os
##########################################
# 0.Adjusting MAPLE output
##########################################
def process_file(file_path, output_folder, output_file_name):
    # Full output file path
    output_file_path = os.path.join(output_folder, output_file_name)
    
    # Open the output file to write the processed data
    with open(output_file_path, "w") as output_file:
        # Write the column headers to the output file
        output_file.write("ID\tPosition\n")
        
        # Initialize the current_id variable to None
        current_id = None
        
        # Iterate over each line in the file and convert it to a list
        with open(file_path, "r") as input_file:
            for line in input_file:
                if line.startswith(">"):
                    # Update current_id if a new ID is encountered
                    current_id = line[1:].strip()
                else:
                    tokens = line.strip().split()
                    position = int(tokens[0])
                    base = tokens[1]
                    percentage = float(tokens[2])

                    # Check if percentage is less than 0.5, and if so, skip adding it to the processed data
                    if percentage < 0.5:
                        continue

                    # Write the processed data to the output file
                    output_file.write(f"{current_id}\t{position}\n")
                    
                    # Delete variables to free up memory
                    del tokens, base, position, percentage
                    
        # Delete the current_id variable after the loop has finished
        del current_id

    print(f"Processing complete and file written to {output_file_path}.")

# For viridian
file_path_VIR = "/nfs/research/goldman/zihao/compViridian_2_P2/MAPLE_Part/For_vir/MAPLE0.3.2_rateVar_errors_realData_checkingErrors_vir_estimatedErrors.txt"
output_folder = "/nfs/research/goldman/zihao/Datas/p2_compViridian_P3/Folder_mapleOutput/"
output_file_name_VIR = "VIR_output_modified.txt"

process_file(file_path_VIR, output_folder, output_file_name_VIR)

# For colman
file_path_COL = "/nfs/research/goldman/zihao/compViridian_2_P2/MAPLE_Part/For_col/MAPLE0.3.2_rateVar_checkingErrors_col_estimatedErrors.txt"
output_file_name_COL = "COL_output_modified.txt"

process_file(file_path_COL, output_folder, output_file_name_COL)

##########################################
# 1.Import and handle with the data
##########################################
Folder_col = os.path.join(output_folder, output_file_name_COL)
Folder_vir = os.path.join(output_folder, output_file_name_VIR)

df_col = pd.read_csv(Folder_col, sep='\t')
df_vir = pd.read_csv(Folder_vir, sep='\t')

df_vir['VIR'] = 1
df_col['COL'] = 1
merged_df = pd.merge(df_vir, df_col, on=['ID','Position'], how='outer')
df_filled = merged_df.fillna(0)

##########################################
# 3.add info_COV_ANNOT
##########################################
# Set to keep track of IDs for which data is not found
missing_ids = set()

# Function to find values based on ID and Position
def find_values(ID, Position, file_path_template, columns, pos_col_name):
    # Generate file path based on ID
    file_path = file_path_template.format(id=ID)
    # Check if file exists
    if not os.path.exists(file_path):
        missing_ids.add(ID)
        return [None for _ in columns], False
    # Read file
    df = pd.read_csv(file_path, delimiter="\t") 
    # Find data based on Position
    df_matched = df[df[pos_col_name] == Position]
    if df_matched.empty:
        missing_ids.add(ID)
        return [None for _ in columns], False
    else:
        return df_matched.iloc[0][columns].tolist(), True

# Iterate over each row in df_filled to find corresponding data in df_cov_path and df_ann_path
for idx, row in df_filled.iterrows():
    ID = row["ID"]
    Position = row["Position"]
    # Find corresponding data in df_cov_path
    df_filled.loc[idx, "RATIO"], _ = find_values(ID, Position, "/nfs/research/goldman/zihao/Datas/p1/File_5_coverage/Decompress/{id}_coverage.txt", ["RATIO"], "Position")
    # Find corresponding data in df_ann_path
    df_filled.loc[idx, ["AF", "SB"]], _ = find_values(ID, Position, "/nfs/research/goldman/zihao/Datas/p1/File_5_annot/New_Decompress/{id}_annot.txt", ["AF", "SB"], "POS")

File_addInfo = "/nfs/research/goldman/zihao/Datas/p2_compViridian_P3/Folder_addInfo/output_addInfo.txt"
df_filled.to_csv(File_addInfo, sep="\t", index=False)
print("The file after adding the information is saved at: ", File_addInfo)

# Print count of missing IDs
print(f"Number of missing IDs: {len(missing_ids)}")

# Save missing IDs to txt file
missing_ids_path = "/nfs/research/goldman/zihao/Datas/p2_compViridian_P3/Folder_addInfo/missing_ids.txt"
with open(missing_ids_path, "w") as f:
    for ID in missing_ids:
        f.write(f"{ID}\n")

# Print path of txt file where missing IDs are saved
print(f"Missing IDs saved at: {os.path.abspath(missing_ids_path)}")