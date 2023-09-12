import os
import pandas as pd

class DataMerger:
    def __init__(self, a_file_path, b_folder_path, output_file_path, missing_b_file_path, missing_rows_file_path):
        self.a_file_path = a_file_path
        self.b_folder_path = b_folder_path
        self.output_file_path = output_file_path
        self.missing_b_file_path = missing_b_file_path
        self.missing_rows_file_path = missing_rows_file_path
        self.missing_b_files_count = 0
        self.missing_rows_count = 0
        self.b_column_names = ['position', 'nucleotide_martin', 'nucleotide_origin', 'label_masked', 'label_mar', 'label_ori', 'label_same', 'RATIO', 'AF', 'SB']

    def read_file(self, file_path, delimiter='\t'):
        """Reads a file into a pandas DataFrame."""
        return pd.read_csv(file_path, delimiter=delimiter)

    def fetch_file_path(self, folder_path, file_id, extension='.txt'):
        """Builds the file path from the folder path and file id."""
        return os.path.join(folder_path, f'{file_id}{extension}')

    def match_row(self, df, column, value):
        """Finds rows in a DataFrame that match a specific value in a specific column."""
        return df[df[column] == value]

    def append_columns(self, df_source, df_target, index):
        """Appends columns from a source DataFrame to a target DataFrame."""
        df_target.loc[index, self.b_column_names] = df_source[self.b_column_names].values.tolist()[0]

    def save_file(self, df, file_path, columns, delimiter='\t', index=False):
        """Saves a DataFrame to a file."""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df[columns].to_csv(file_path, sep=delimiter, index=index)

    def merge_data(self):
        a_data = self.read_file(self.a_file_path)

        with open(self.missing_b_file_path, 'w') as missing_b_file, open(self.missing_rows_file_path, 'w') as missing_rows_file:

            for index, row in a_data.iterrows():
                b_file_path = self.fetch_file_path(self.b_folder_path, row['ID'])

                if not os.path.isfile(b_file_path):
                    missing_b_file.write(f'{row["ID"]}\n')
                    self.missing_b_files_count += 1
                    continue

                b_data = self.read_file(b_file_path)
                matched_row = self.match_row(b_data, 'position', row['Position'])

                if matched_row.empty:
                    missing_rows_file.write(f'{row["ID"]}\t{row["Position"]}\n')
                    self.missing_rows_count += 1
                    continue

                self.append_columns(matched_row, a_data, index)

        self.save_file(a_data, self.output_file_path, ['ID', 'Position'] + self.b_column_names)

    def report(self):
        print(f"Data saved to {self.output_file_path}")
        print(f"{self.missing_b_files_count} ID of the file with the missing merge information (SB, AF) is saved to {self.missing_b_file_path}")
        print(f"Missing row IDs and Positions saved to {self.missing_rows_file_path}")

if __name__ == '__main__':
    a_file_path = '/nfs/research/goldman/zihao/Datas/p2_compViridian_P3/Folder_mapleOutput/COL_output_modified.txt'
    b_folder_path = "/nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_2_combination/folderData_addInfo"
    output_file_path = '/nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_3_calculForPLOT/errPos/errpos_outputData.txt'
    missing_b_file_path = '/nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_3_calculForPLOT/errPos/errPos_missingFiles.txt'
    missing_rows_file_path = '/nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_3_calculForPLOT/errPos/errPos_missingPos.txt'
    
    merger = DataMerger(a_file_path, b_folder_path, output_file_path, missing_b_file_path, missing_rows_file_path)
    merger.merge_data()
    merger.report()