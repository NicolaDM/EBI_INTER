import os
import pandas as pd
# ==================Requires modification==================
# folder_path：The location where the processed file was saved in the previous step
# output_folder：Location to save processed files
# (probable)total_rows: Number of samples
# ==================Requires modification==================

def sample_rows_from_files(folder_path, output_folder, output_file, total_rows):
    """
    Function to sample rows from multiple files within a folder
    """
    
    # Ensure the output folder exists, if not, create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Save the results to a new txt file in the specified output folder
    output_path = os.path.join(output_folder, output_file)
    first_file = True  # Use this flag to write headers only once

    # Get all files and count them
    files = [f for f in os.listdir(folder_path) if f.endswith(".txt") and f.startswith("merged_")]
    n_files = len(files)

    # Calculate rows per file
    rows_per_file = total_rows // n_files

    # Read all files and store them in a list
    for filename in files:
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path, sep="\t")

        df['ID'] = filename.split("_")[1].split(".")[0]  # Extract ID from the filename

        # Randomly sample the specified number of rows from the large DataFrame
        df_sampled = df.sample(n=rows_per_file, random_state=1)

        # Keep only the needed columns
        df_sampled = df_sampled[['ID', 'POS', 'REF', 'ALT', 'AF', 'nucleotide_martin']]

        # Append the results to the output file, write headers only for the first file
        df_sampled.to_csv(output_path, mode='a', sep="\t", index=False, header=first_file)
        first_file = False  # After first write, headers should not be written

    return output_path

# Set the folder path and number of samples
folder_path = "/nfs/research/goldman/zihao/Datas/p1_errorsProject_P4/Folder_treatedAF/folderData_treatedFile/"
output_folder = "/nfs/research/goldman/zihao/Datas/p1_errorsProject_P4/Folder_combFor_allPos/"  # specify your output folder here
output_file = "allPos_combForvir.txt"
total_rows = 299030  # Total number of rows you wish to sample from all files

# Use the function to sample rows and save the output
output_path = sample_rows_from_files(folder_path, output_folder, output_file, total_rows)

# Print message indicating where the file has been saved
print(f"File has been saved to: {output_path}")




