import os

folder_path = '/nfs/research/goldman/zihao/Datas/p2_comp_viridian/1_extract_sequence'
output_folder = '/nfs/research/goldman/zihao/Datas/p2_comp_viridian/1_extract_sequence/split_files'
files_per_txt = 10

# Get the list of txt files in the folder
txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

# Limit the number of output files to a maximum of 10
num_output_files = min(len(txt_files), 10)

# Calculate the number of files per output txt
files_per_output = (len(txt_files) + num_output_files - 1) // num_output_files

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Split and write to txt files
for i in range(num_output_files):
    start_index = i * files_per_output
    end_index = (i + 1) * files_per_output
    output_file_path = os.path.join(output_folder, f'output_{i + 1}.fasta')

    with open(output_file_path, 'w') as output_file:
        for file_name in txt_files[start_index:end_index]:
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as input_file:
                output_file.write(input_file.read())
            output_file.write('\n')

print('File splitting and writing completed.')

