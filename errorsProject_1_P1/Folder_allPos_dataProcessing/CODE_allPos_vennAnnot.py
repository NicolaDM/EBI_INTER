import os
import pandas as pd

def merge_files(folder1_path, folder2_path, output_folder_path, output_folderMissing_path):
    # If output_folder_path doesn't exist, create it
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    not_found_ids = []

    # Iterate through files in Folder1
    for filename in os.listdir(folder1_path):
        if filename.endswith("_coverage.txt"):
            file_id = filename.replace("_coverage.txt", "")
            filepath1 = os.path.join(folder1_path, filename)

            # Confirm if corresponding file exists in Folder2
            filepath2 = os.path.join(folder2_path, f"{file_id}_annot.txt")
            if not os.path.exists(filepath2):
                not_found_ids.append(file_id)
                continue

            # Load the two files into dataframes
            df1 = pd.read_csv(filepath1, sep="\t")
            df2 = pd.read_csv(filepath2, sep="\t")

            # Merge based on the 'Position' column from df1 and 'POS' column from df2
            df_merged = pd.merge(df1, df2, left_on="Position", right_on="POS", how="inner")[['Position','RATIO','AF','SB']]

            # Save the merged data to a new file
            output_filepath = os.path.join(output_folder_path, f"{file_id}_merged.txt")
            df_merged.to_csv(output_filepath, sep="\t", index=False)

    # Output IDs not found
    not_found_ids_file = os.path.join(output_folderMissing_path, "not_found_ids.txt")
    with open(not_found_ids_file, "w") as f:
        for id_ in not_found_ids:
            f.write(f"{id_}\n")
    
    # Print the number of missing IDs
    print(f"The number of missing IDs: {len(not_found_ids)}")
    
    # Print the path of the folder storing missing IDs
    print(f"The path of the folder storing missing IDs: {output_folderMissing_path}")

folder1_path = "/nfs/research/goldman/zihao/Datas/p1_errorsProject_NEW/Folder_dataProcessing/folderData_MAPLE_allPos"
folder2_path = "/nfs/research/goldman/zihao/Datas/p1/File_5_annot/New_Decompress"
output_folderMissing_path = "/nfs/research/goldman/zihao/Datas/p1_errorsProject_NEW/Folder2_calculPercentage/Folder_missingID" 
output_folder_path = "/nfs/research/goldman/zihao/Datas/p1_errorsProject_NEW/Folder2_calculPercentage/folderData_mergeINFO" 

merge_files(folder1_path, folder2_path, output_folder_path, output_folderMissing_path)

def count_files(folder_path):
    if not os.path.isdir(folder_path):
        raise ValueError("Invalid folder path!")

    file_count = 0
    for _, _, files in os.walk(folder_path):
        file_count += len(files)

    return file_count

folder_path = output_folder_path

try:
    num_files = count_files(folder_path)
    print('=========================== information =========================== ')
    print(f"The number of samples is: {num_files}")
except ValueError as e:
    print(str(e))


                
                
                
                
                
                
