import argparse
import pandas as pd
import glob
import os

def process_files(output_id: int, input_path: str, merge_dir: str):
    files = glob.glob(os.path.join(input_path, '*.txt'))

    missing_cov_ids = []
    missing_ann_ids = []

    output_dir = '/nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_3_mergeINFO/folderData_missingData/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for file in files:
        try:
            basename = os.path.basename(file)
            id = basename[:-4]

            df = pd.read_csv(file, sep='\t')

            df_cov_path = f"/nfs/research/goldman/zihao/Datas/p1/File_5_coverage/Decompress/{id}_coverage.txt"
            if not os.path.exists(df_cov_path):
                missing_cov_ids.append(id)
                continue
            df_cov = pd.read_csv(df_cov_path, sep='\t')

            df_ann_path = f"/nfs/research/goldman/zihao/Datas/p1/File_5_annot/New_Decompress/{id}_annot.txt"
            if not os.path.exists(df_ann_path):
                missing_ann_ids.append(id)
                continue
            df_ann = pd.read_csv(df_ann_path, sep='\t')

            df_merge = pd.concat([df, df_cov['RATIO'], df_ann['AF'], df_ann['SB']], axis=1)
            # merge_output_dir = f"/nfs/research/goldman/zihao/Datas/p2_comp_viridian/Folder_3_mergeINFO/folderData_mergeFile/"

            # Use the provided merge_dir for saving merged data
            if not os.path.exists(merge_dir):
                os.makedirs(merge_dir)
            df_merge.to_csv(os.path.join(merge_dir, os.path.basename(file)), index=False, sep='\t')

        except Exception as e:
            print(f"An error occurred while processing {file}: {e}")

    with open(os.path.join(output_dir, f'missing_cov_ids_{output_id}.txt'), 'w') as f:
        for id in missing_cov_ids:
            f.write(f"{id}\n")

    with open(os.path.join(output_dir, f'missing_ann_ids_{output_id}.txt'), 'w') as f:
        for id in missing_ann_ids:
            f.write(f"{id}\n")

    # print(f"Number of missing cov ids: {len(missing_cov_ids)}")
    # print(f"Number of missing ann ids: {len(missing_ann_ids)}")
    print("Missing IDs are stored in： ", output_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default=1, type=int, help='The output id, e.g. 1 for missing_cov_ids_1.txt')
    parser.add_argument('--input_folder', required=True, type=str, help='The path to the folder containing .txt files to be processed.')
    parser.add_argument('--merge_dir', required=True, type=str, help='The directory to save merged files.')
    args = parser.parse_args()
    process_files(args.output, args.input_folder, args.merge_dir)

    

