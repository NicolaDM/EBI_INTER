import os
import time

# ==================Requires modification==================
# output_folder：output folder
# ==================Requires modification==================
class AnnotDataProcessor:
    def __init__(self, data1_file, dir_to_search_Annot, output_file):
        self.data1_file = data1_file
        self.dir_to_search_Annot = dir_to_search_Annot
        self.output_file = output_file

    def _read_data1(self):
        data1 = []
        with open(self.data1_file) as f:
            header = f.readline().strip() + "\tAF\tSB\n"
            for line in f:
                line = line.strip().split()
                data1.append(line)
        return header, data1

    def _process_data(self, output_folder):
        header, data1 = self._read_data1()
        
        missing_ids = set()

        for row in data1:
            id = row[0]
            filename = os.path.join(self.dir_to_search_Annot, f"{id}_annot.txt")
            if os.path.exists(filename):
                with open(filename) as f:
                    for line in f:
                        line = line.strip().split()
                        if line[0] == row[1]:
                            row.append(line[3])
                            row.append(line[4])
                            break
                    else:
                        row.append("")
                        row.append("")
            else:
                missing_ids.add(id)

        print(f'There are {len(missing_ids)} missing IDs.')

        missing_id_file = os.path.join(output_folder, 'errPOS_missing_files_AF.txt')
        with open(missing_id_file, 'w') as f:
            for id in missing_ids:
                f.write(f'{id}\n')

        print(f'Missing IDs have been saved to: {missing_id_file}')

        return header, data1

    def process(self, output_folder):
        header, data1 = self._process_data(output_folder)
        with open(self.output_file, "w") as f:
            f.write(header)
            for row in data1:
                f.write("\t".join(row) + "\n")

if __name__ == '__main__':
    output_folder = "/nfs/research/goldman/zihao/Datas/p1_errorsProject_NEW/Folder_dataProcessing/"
    output_file = os.path.join(output_folder, "output_modified.txt")

    while not os.path.exists(output_file):
        time.sleep(5)
    print("Output file found. Proceeding with the process...")
    
    data1_file = output_file
    dir_to_search_Annot = "/nfs/research/goldman/zihao/Datas/p1/File_5_annot/New_Decompress/"

    file_name_annot = "ANNOT_dataProcessing_errorPos.txt"
    output_file_annot = output_folder + file_name_annot
    
    annotProcessor = AnnotDataProcessor(data1_file, dir_to_search_Annot, output_file_annot)
    annotProcessor.process(output_folder)

with open(output_file_annot, 'r') as file:
    line_count = sum(1 for line in file)
print('=========================== information =========================== ')
print(f"The number of MAPLE-marked error positions (After finishing the ANNOT information merge operation) is: {line_count-1}")

print('=========================== information =========================== ')
print("output_file_annot saved to: ", output_file_annot)

