import os

# ==================Requires modification==================
# input_file: MAPLE output file indicating the positions of the error
# output_folder：output folder
# ==================Requires modification==================
class MapleFileProcessor:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file

    def process(self):
        with open(self.output_file, "w") as output_file:
            output_file.write("ID\tPosition\n")
            current_id = None
            with open(self.input_file, "r") as input_file:
                for line in input_file:
                    if line.startswith(">"):
                        current_id = line[1:].strip()
                    else:
                        tokens = line.strip().split()
                        position = int(tokens[0])
                        percentage = float(tokens[2])
                        if percentage < 0.5:
                            continue
                        output_file.write(f"{current_id}\t{position}\n")

if __name__ == '__main__':
    input_file = "/nfs/research/goldman/zihao/compViridian_2_P2/MAPLE_Part/For_col/MAPLE0.3.2_rateVar_checkingErrors_col_estimatedErrors.txt"
    output_folder = "/nfs/research/goldman/zihao/Datas/p1_errorsProject_NEW/Folder_dataProcessing/"
    output_file = os.path.join(output_folder, "output_modified.txt")
    mapleProcessor = MapleFileProcessor(input_file, output_file)
    mapleProcessor.process()

with open(output_file, 'r') as file:
    line_count = sum(1 for line in file)
print('=========================== information =========================== ')
print(f"The number of MAPLE-marked error positions is: {line_count-1}")

print('=========================== information =========================== ')
print("output_file_annot saved to:", output_file)
