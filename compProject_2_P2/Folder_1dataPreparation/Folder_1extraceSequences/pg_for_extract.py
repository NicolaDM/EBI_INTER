import os
import argparse
import gzip

file_path = "/nfs/research/goldman/zihao/errorsProject_1/MAPLE/new_version_MAY/MAPLE0.3.2_rateVar_errors_realData_checkingErrors_new_all_estimatedErrors.txt"
data_set = set()

with open(file_path, 'r') as file:
    for line in file:
        if line.startswith(">"):
            data_set.add(line.strip())
            
def process_file(input_filename, output_dir):
    with gzip.open(input_filename, 'rt') as file:
        current_name = None
        current_content = []
        for line in file:
            if line.startswith(">"):
                if current_name is not None and current_name.split(".")[0] in data_set:
                    output_path = os.path.join(output_dir, current_name.split(".")[0][1:] + ".txt")
                    with open(output_path, "w") as out_file:
                        out_file.write(current_name + "\n" + "".join(current_content))
                
                current_name = line.strip()
                current_content = []
            else:
                current_content.append(line)

        if current_name is not None and current_name.split(".")[0] in data_set:
            output_path = os.path.join(output_dir, current_name.split(".")[0][1:] + ".txt")
            with open(output_path, "w") as out_file:
                out_file.write(current_name + "\n" + "".join(current_content))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some files.")
    parser.add_argument("-i", "--input_file", required=True, help="The input file to be processed")
    parser.add_argument("-o", "--output_dir", required=True, help="The output directory to store processed files")

    args = parser.parse_args()

    process_file(args.input_file, args.output_dir)

