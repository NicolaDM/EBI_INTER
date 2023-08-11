import os
import shutil
import random
# ==================Requires modification==================
# checkid_file: MAPLE output file indicating the positions of the error
# nb_sample: How many samples per position
# ==================Requires modification==================
class CovFileProcessor:
    def __init__(self, folder_path, checkid_file, output_folder, log_folder):
        self.folder_path = folder_path
        self.checkid_file = checkid_file
        self.output_folder = output_folder
        if not os.path.exists(log_folder):  # Check if the log_folder exists
            os.makedirs(log_folder)  # Create log_folder if it does not exist
        self.log_file = os.path.join(log_folder, "missing_ids_cov.txt")

    def run(self):
        id_set = set()
        missing_ids = []
        is_first_line = True

        with open(self.checkid_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('>'):
                    if is_first_line:
                        is_first_line = False
                    else:
                        id_set.add(line[1:])

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        id_set_copy = id_set.copy()

        for filename in os.listdir(self.folder_path):
            for id_str in id_set:
                if id_str in filename:
                    shutil.copy(os.path.join(self.folder_path, filename), os.path.join(self.output_folder, filename))
                    id_set_copy.discard(id_str)  # remove the found id_str from the copy

        # After the loop, id_set_copy contains ids that were not found in any filename
        missing_ids = list(id_set_copy)  # convert to list if necessary

        with open(self.log_file, 'w') as f:
            for id in missing_ids:
                f.write(f"{id}\n")

    def get_log_file_path(self):
        return os.path.abspath(self.log_file)

    def count_missing_ids(self):
        with open(self.log_file, 'r') as f:
            line_count = sum(1 for _ in f)
        return line_count

class ReservoirSampler:
    def __init__(self, output_file_path, k):
        self.output_file_path = output_file_path
        self.k = k

    def generator(self, file_list):
        for file_name in file_list:
            with open(file_name, 'r') as file:
                file_id = os.path.splitext(os.path.basename(file_name))[0]
                file_id = file_id.replace('_coverage', '')
                next(file)
                for line in file:
                    yield [file_id] + line.strip().split('\t')

    def reservoir_sampling(self, stream):
        reservoir = {}
        for item in stream:
            position = int(item[1])
            if position not in reservoir:
                reservoir[position] = [item]
            elif len(reservoir[position]) < self.k:
                reservoir[position].append(item)
            else:
                j = random.randint(0, len(reservoir[position]) + 1)
                if j < self.k:
                    reservoir[position][j] = item
        return reservoir

    def output_samples(self, samples):
        with open(self.output_file_path, 'w') as output_file:
            output_file.write('ID\tPosition\tN\tCov_RATIO\n')
            for position, sample_list in samples.items():
                for sample in sample_list:
                    output_file.write('\t'.join(sample) + '\n')

    def process_files(self, folder_path):
        file_list = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(".txt")]
        stream = self.generator(file_list)
        samples = self.reservoir_sampling(stream)
        self.output_samples(samples)


class AnnotDataProcessor:
    def __init__(self, data1_file, data_folder, output_file, log_folder):
        self.data1_file = data1_file
        self.data_folder = data_folder
        self.output_file = output_file
        if not os.path.exists(log_folder):  # Check if the log_folder exists
            os.makedirs(log_folder)  # Create log_folder if it does not exist
        self.log_file = os.path.join(log_folder, "missing_ids_annot.txt")

    def read_data1(self):
        data1 = []
        with open(self.data1_file) as f:
            header = f.readline().strip() + "\tAF\tSB\n"
            for line in f:
                line = line.strip().split()
                data1.append(line)
        return header, data1

    def process_data(self):
        header, data1 = self.read_data1()
        missing_ids = []

        for row in data1:
            id = row[0]
            filename = os.path.join(self.data_folder, f"{id}_annot.txt")
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
                missing_ids.append(id)

        with open(self.log_file, 'w') as f:
            for id in missing_ids:
                f.write(f"{id}\n")

        return header, data1

    def write_output(self):
        header, data1 = self.process_data()
        with open(self.output_file, 'w') as f:
            f.write(header)
            for row in data1:
                f.write("\t".join(row) + "\n")

    def get_log_file_path(self):
        return os.path.abspath(self.log_file)

    def count_missing_ids(self):
        with open(self.log_file, 'r') as f:
            line_count = sum(1 for _ in f)
        return line_count


if __name__ == '__main__':
    folder_path = "/nfs/research/goldman/zihao/Datas/p1/File_5_coverage/Decompress/"
    checkid_file = "/nfs/research/goldman/zihao/Datas/p2_comp_viridian/2_alignment/Col_MAPLE_format_consensuses.txt"
    output_folder = "/nfs/research/goldman/zihao/Datas/p1_errorsProject_NEW/Folder_dataProcessing/folderData_MAPLE_allPos"
    sampler_output = "/nfs/research/goldman/zihao/Datas/p1_errorsProject_NEW/Folder_dataProcessing/COV_dataProcessing_allPos.txt"
    data_folder = "/nfs/research/goldman/zihao/Datas/p1/File_5_annot/New_Decompress/"
    output_file = "/nfs/research/goldman/zihao/Datas/p1_errorsProject_NEW/Folder_dataProcessing/ANNOT_dataProcessing_allPos.txt"
    nb_sample = 10
    log_folder = "/nfs/research/goldman/zihao/Datas/p1_errorsProject_NEW/Folder_dataProcessing/Folder_Allpos_missingID"

    # Run the CovFileProcessor
    cov_processor = CovFileProcessor(folder_path, checkid_file, output_folder, log_folder)
    cov_processor.run()
    print(f"Missing IDs for CovFileProcessor: {cov_processor.count_missing_ids()} have been logged at {cov_processor.get_log_file_path()}")


    def count_files(folder_path):
        if not os.path.isdir(folder_path):
            raise ValueError("Invalid folder path!")

        file_count = 0
        for _, _, files in os.walk(folder_path):
            file_count += len(files)

        return file_count

    folder_path = output_folder

    try:
        num_files = count_files(folder_path)
        print('=========================== information =========================== ')
        print(f"The number of samples is: {num_files}")
    except ValueError as e:
        print(str(e))

    
    # Run the ReservoirSampler
    sampler = ReservoirSampler(sampler_output, nb_sample)
    sampler.process_files(output_folder)
    
    # Run the AnnotDataProcessor
    processor = AnnotDataProcessor(sampler_output, data_folder, output_file, log_folder)
    processor.write_output()
    print(f"Missing IDs for AnnotDataProcessor: {processor.count_missing_ids()} have been logged at {processor.get_log_file_path()}")
    
    with open(output_file, 'r') as file:
        line_count = sum(1 for line in file)
    print('=========================== information =========================== ')
    print(f"The total number of samples completed for sampling is: {line_count-1}")