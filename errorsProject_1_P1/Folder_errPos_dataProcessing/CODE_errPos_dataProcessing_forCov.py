import os
import time
# ==================Requires modification==================
# output_folder：output folder
# ==================Requires modification==================
class CovDataProcessor:
    def __init__(self, data_file_path, dir_to_search_Cov, output_file_path):
        self.data_file_path = data_file_path
        self.dir_to_search_Cov = dir_to_search_Cov
        self.output_file_path = output_file_path

    @staticmethod
    def _search_position_value_and_get_column_4(file_path, id_position):
        with open(file_path, "r") as f:
            file_header = f.readline().strip().split("\t")
            position_column_index = file_header.index("Position")
            column_4_index = 2
            for line in f:
                line_values = line.strip().split("\t")
                if position_column_index < len(line_values):
                    position_value = int(line_values[position_column_index])
                    if position_value == id_position and column_4_index < len(line_values):
                        return line_values[column_4_index]
        return None

    @staticmethod
    def _calculate_mean_error(data):
        position_error_sum = {}
        position_count = {}
        for line in data:
            position = line[1]
            mean_error = line[-1]
            if mean_error != "None":
                mean_error = float(mean_error)
                if position in position_error_sum:
                    position_error_sum[position] += mean_error
                    position_count[position] += 1
                else:
                    position_error_sum[position] = mean_error
                    position_count[position] = 1
        mean_error_by_position = {}
        for position in position_error_sum:
            mean_error_by_position[position] = position_error_sum[position] / position_count[position]
        return mean_error_by_position

    def process(self):
        data = []
        missing_ids_count = 0  # Counter for missing IDs
        missing_ids_file = "errPOS_missing_files_COV.txt"  # Filename for missing IDs

        with open(self.data_file_path, "r") as f:
            header = f.readline().strip().split("\t")
            header.append("COV_Ratio")
            for line in f:
                data.append(line.strip().split("\t") + [None])

        # Create/Open a txt file to store the IDs of non-existent files
        with open(missing_ids_file, "a") as missing_file:
            for line in data:
                id_now = str(line[0])
                id_position = line[1]
                file_found = False
                if id_position is not None:
                    for filename in os.listdir(self.dir_to_search_Cov):
                        if id_now in filename and filename.endswith(".txt"):
                            file_path = os.path.join(self.dir_to_search_Cov, filename)
                            result = self._search_position_value_and_get_column_4(file_path, int(id_position))
                            if result is not None:
                                line[-1] = result
                                file_found = True
                                break
                if not file_found:
                    # Write the ID into the txt file
                    missing_file.write(str(id_now) + "\t")

                    missing_ids_count += 1  # Increment the counter

        data = [line for line in data if line[-1] is not None and line[-1] != "None"]
        mean_error_by_position = self._calculate_mean_error(data)
        with open(self.output_file_path, "w") as f:
            f.write("ID\tPosition\tCOV_Ratio\n")  # Change column name to 'ID', 'Position', 'COV_Ratio'
            for line in data:
                f.write(f"{line[0]}\t{line[1]}\t{line[-1]}\n")  # Save `id_now` to 'ID', `id_position` to 'Position' and COV_Ratio

        print('=========================== information =========================== ')
        print(f"Number of missing IDs: {missing_ids_count}")
        print(f"Missing IDs saved to: {os.path.abspath(missing_ids_file)}")  # Print the absolute path of the txt file


if __name__ == '__main__':
    output_folder = "/nfs/research/goldman/zihao/Datas/p1_errorsProject_NEW/Folder_dataProcessing/"
    output_file = os.path.join(output_folder, "output_modified.txt")

    
    # Wait until the output_file exists
    while not os.path.exists(output_file):
        time.sleep(5)  # Wait for 5 seconds before checking again
    print("Output file found. Proceeding with the process...")
    
    dir_to_search_Cov = "/nfs/research/goldman/zihao/Datas/p1/File_5_coverage/Decompress/"
    data_file_path = output_file
    
    file_name_cov = "COV_dataProcessing_errorPos.txt"
    output_file_cov = output_folder + file_name_cov

    covProcessor = CovDataProcessor(data_file_path, dir_to_search_Cov, output_file_cov)
    covProcessor.process()

with open(output_file_cov, 'r') as file:
    line_count = sum(1 for line in file)
print('=========================== information =========================== ')
print(f"The number of MAPLE-marked error positions "
      f"(After finishing the COV information merge operation) is: {line_count-1}")

print('=========================== information =========================== ')
print("output_file_cov saved to: ", output_file_cov)
