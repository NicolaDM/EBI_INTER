import csv
import gzip
import glob
import os

class VCFProcessor:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

    @staticmethod
    def parse_info_field(info_str):
        """Parse the INFO field of a VCF file and return a dictionary."""
        info_dict = {}
        for field in info_str.split(';'):
            if '=' in field:
                key, value = field.split('=')
                info_dict[key] = value
        return info_dict

    def process_vcf_file(self, file_path):
        """Process a single VCF file and return the processed data."""
        try:
            data = {}
            new_data = []

            with gzip.open(file_path, 'rt') as file:
                reader = csv.reader(file, delimiter='\t')

                for row in reader:
                    if not row or row[0].startswith('#'):
                        continue

                    chrom, pos, id_, ref, alt, qual, filter_, info = row
                    pos = int(pos)
                    info_dict = self.parse_info_field(info)

                    if 'INDEL' in info_dict and info_dict['INDEL'] == True:
                        continue
                        
                    # Skip the current loop if 'REF' or 'ALT' have more than one character
                    if len(ref) > 1 or len(alt) > 1:
                        continue

                    ref = ref if ref else '0'
                    alt = alt if alt else '0'
                    af = info_dict.get('AF', '0')
                    sb = info_dict.get('SB', '0')
                    
                    af = float(af)
                    """
                    if af > 0.5:
                        af = 1 - af
                    """

                    if pos not in data:
                        data[pos] = [pos, ref, alt, af, sb]

            for idx in range(1, length_of_sample):
                if idx in data:
                    new_data.append(data[idx])
                else:
                    new_data.append([idx, 'NA', 'NA', '0', '0'])

            return new_data

        except Exception as e:
            print(f"Unknown error processing {file_path}: {e}")

    def process_files(self):
        """Process all VCF files in the input directory and write the results to the output directory."""
        
        file_paths = glob.glob(os.path.join(self.input_dir, '*.annot.vcf.gz'))

        for i, file_path in enumerate(file_paths):

            output_file = os.path.join(self.output_dir, os.path.basename(file_path).replace('.annot.vcf.gz', '_annot.txt'))

            if os.path.exists(output_file):
                print(f"{output_file} already exists. Skipping file {file_path}.")
                continue

            result = self.process_vcf_file(file_path)
            if result is None:
                continue

            with open(output_file, 'w', newline='') as f:
                writer = csv.writer(f, delimiter='\t')
                writer.writerow(['POS', 'REF', 'ALT', 'AF', 'SB'])
                writer.writerows(result)

if __name__ == '__main__':
    length_of_sample = 29904 # the true number +1 (eg: 29903 should be 29904)
    input_dir = '/nfs/research/goldman/zihao/Datas/p1/File_5_annot/Downloads/'
    output_dir = '/nfs/research/goldman/zihao/Datas/p1/File_5_annot/Folder_Decompress_forP4/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    processor = VCFProcessor(input_dir, output_dir)
    processor.process_files()


