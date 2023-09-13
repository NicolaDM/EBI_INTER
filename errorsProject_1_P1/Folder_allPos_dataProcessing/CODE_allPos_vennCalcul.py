import os
import pandas as pd
from multiprocessing import Pool, cpu_count, Manager

def merge_and_process(args):
    filename, folder1_path, folder2_path, not_found_ids = args

    if filename.endswith("_coverage.txt"):
        file_id = filename.replace("_coverage.txt", "")
        filepath1 = os.path.join(folder1_path, filename)

        # Confirm if corresponding file exists in Folder2
        filepath2 = os.path.join(folder2_path, f"{file_id}_annot.txt")
        if not os.path.exists(filepath2):
            not_found_ids.append(file_id)
            return

        # Load the two files into dataframes
        df1 = pd.read_csv(filepath1, sep="\t")
        df2 = pd.read_csv(filepath2, sep="\t")

        # Merge based on the 'Position' column from df1 and 'POS' column from df2
        df_merged = pd.merge(df1, df2, left_on="Position", right_on="POS", how="inner")[['Position','RATIO','AF','SB']]
        
        # Process the merged dataframe
        return process_dataframe(df_merged)
    return None

def process_dataframe(df_v0):
    df_v0["Label_COV"] = (df_v0["RATIO"] < 0.1).astype(int)
    df_v0["Label_AF"] = (df_v0["AF"] > 0.001).astype(int)
    df_v0["Label_SB"] = (df_v0["SB"] > 0).astype(int)
    
    stats = {
        'nb_count': len(df_v0),
        'nb_SB_PASSED': sum((df_v0['Label_COV'] == 0)&(df_v0['Label_AF'] == 0)&(df_v0['Label_SB'] == 1)),
        'nb_AF_PASSED': sum((df_v0['Label_COV'] == 0)&(df_v0['Label_AF'] == 1)&(df_v0['Label_SB'] == 0)),
        'nb_COV_PASSED': sum((df_v0['Label_COV'] == 1)&(df_v0['Label_AF'] == 0)&(df_v0['Label_SB'] == 0)),
        'both_PASSED': sum((df_v0['Label_COV'] == 1)&(df_v0['Label_AF'] == 1)&(df_v0['Label_SB'] == 1)),
        'both_UNPASSED': sum((df_v0['Label_COV'] == 0)&(df_v0['Label_AF'] == 0)&(df_v0['Label_SB'] == 0)),
        'nb_AF_SB_PASSED': sum((df_v0['Label_COV'] == 0)&(df_v0['Label_AF'] == 1)&(df_v0['Label_SB'] == 1)),
        'nb_SB_COV_PASSED': sum((df_v0['Label_COV'] == 1)&(df_v0['Label_AF'] == 0)&(df_v0['Label_SB'] == 1)),
        'nb_AF_COV_PASSED': sum((df_v0['Label_COV'] == 1)&(df_v0['Label_AF'] == 1)&(df_v0['Label_SB'] == 0))
    }

    return stats

def main():
    folder1_path = "/nfs/research/goldman/zihao/Datas/p1_errorsProject_NEW/Folder_dataProcessing/folderData_MAPLE_allPos"
    folder2_path = "/nfs/research/goldman/zihao/Datas/p1/File_5_annot/New_Decompress"
    output_folderMissing_path = "/nfs/research/goldman/zihao/Datas/p1_errorsProject_NEW/Folder2_calculPercentage/Folder_missingID" 

    # Check if output_folderMissing_path exists, if not, create it
    if not os.path.exists(output_folderMissing_path):
        os.makedirs(output_folderMissing_path, exist_ok=True)

    with Manager() as manager:
        not_found_ids = manager.list()
        with Pool(cpu_count()) as pool:
            results = pool.map(merge_and_process, [(filename, folder1_path, folder2_path, not_found_ids) for filename in os.listdir(folder1_path)])

        # Aggregate results
        aggregated_stats = {}
        for stats in results:
            if stats:
                for key, value in stats.items():
                    if key in aggregated_stats:
                        aggregated_stats[key] += value
                    else:
                        aggregated_stats[key] = value

        # Print aggregated results
        for key, value in aggregated_stats.items():
            print(f"{key}: {value}")

        # Output IDs not found
        not_found_ids_file = os.path.join(output_folderMissing_path, "not_found_ids.txt")
        with open(not_found_ids_file, "w") as f:
            for id_ in not_found_ids:
                f.write(f"{id_}\n")

        # Print the number of missing IDs
        print(f"The number of missing IDs: {len(not_found_ids)}")
        # Print the path of the folder storing missing IDs
        print(f"The path of the folder storing missing IDs: {output_folderMissing_path}")

if __name__ == "__main__":
    main()


