import os
import pandas as pd

# ==================Requires modification==================
# folder_path: The folders for ANNOT information and COV information were merged in the previous step.
# ==================Requires modification==================

def process_files(folder_path):
    nb_count = 0
    nb_SB_PASSED = 0
    nb_AF_PASSED = 0
    nb_COV_PASSED = 0
    both_PASSED = 0
    both_UNPASSED = 0
    nb_AF_SB_PASSED = 0
    nb_SB_COV_PASSED = 0
    nb_AF_COV_PASSED = 0

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            df_v0 = pd.read_csv(os.path.join(folder_path, file_name), sep='\t')
            
            df_v0["Label_COV"] = (df_v0["RATIO"] < 0.1).astype(int)
            df_v0["Label_AF"] = (df_v0["AF"] > 0.001).astype(int)
            df_v0["Label_SB"] = (df_v0["SB"] > 0).astype(int)
            
            nb_count += len(df_v0)
            nb_SB_PASSED += sum((df_v0['Label_COV'] == 0)&(df_v0['Label_AF'] == 0)&(df_v0['Label_SB'] == 1))
            nb_AF_PASSED += sum((df_v0['Label_COV'] == 0)&(df_v0['Label_AF'] == 1)&(df_v0['Label_SB'] == 0))
            nb_COV_PASSED += sum((df_v0['Label_COV'] == 1)&(df_v0['Label_AF'] == 0)&(df_v0['Label_SB'] == 0))
            
            both_PASSED += sum((df_v0['Label_COV'] == 1)&(df_v0['Label_AF'] == 1)&(df_v0['Label_SB'] == 1))
            both_UNPASSED += sum((df_v0['Label_COV'] == 0)&(df_v0['Label_AF'] == 0)&(df_v0['Label_SB'] == 0))
            nb_AF_SB_PASSED += sum((df_v0['Label_COV'] == 0)&(df_v0['Label_AF'] == 1)&(df_v0['Label_SB'] == 1))
            nb_SB_COV_PASSED += sum((df_v0['Label_COV'] == 1)&(df_v0['Label_AF'] == 0)&(df_v0['Label_SB'] == 1))
            nb_AF_COV_PASSED += sum((df_v0['Label_COV'] == 1)&(df_v0['Label_AF'] == 1)&(df_v0['Label_SB'] == 0))

    print('====================== Info ======================')
    print('Total number of positions: ', nb_count)
    print('nb_SB_PASSED: ', nb_SB_PASSED)
    print('nb_AF_PASSED: ', nb_AF_PASSED)
    print('nb_COV_PASSED: ', nb_COV_PASSED)
    print('====================== Info ======================')
    print('both_PASSED: ', both_PASSED)
    print('both_UNPASSED: ', both_UNPASSED)
    print('====================== Info ======================')
    print('nb_AF_SB_PASSED: ', nb_AF_SB_PASSED)
    print('nb_SB_COV_PASSED: ', nb_SB_COV_PASSED)
    print('nb_AF_COV_PASSED: ', nb_AF_COV_PASSED)

folder_path = "/nfs/research/goldman/zihao/Datas/p1_errorsProject_NEW/Folder2_calculPercentage/folderData_mergeINFO"
process_files(folder_path)