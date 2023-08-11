import os

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
file_path = "/nfs/research/goldman/zihao/compViridian_2_P2/MAPLE_Part/For_vir/MAPLE0.3.2_rateVar_errors_realData_checkingErrors_vir_estimatedErrors.txt"
output_folder = "/nfs/research/goldman/zihao/Datas/p2_compViridian_P3/Folder_mapleOutput/"
output_file_name = "VIR_output_modified.txt"

process_file(file_path, output_folder, output_file_name)

# For colman
file_path = "/nfs/research/goldman/zihao/compViridian_2_P2/MAPLE_Part/For_col/MAPLE0.3.2_rateVar_checkingErrors_col_estimatedErrors.txt"
output_file_name = "COL_output_modified.txt"

process_file(file_path, output_folder, output_file_name)
