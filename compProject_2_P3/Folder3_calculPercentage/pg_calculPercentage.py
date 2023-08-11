import os
import pandas as pd

# ==================Requires modification==================
# folder_path: The folder where the file with the error positions information was added.
# ==================Requires modification==================
def process_files(folder_path):
      
    num_viridian_masked = 0
    num_colman_masked = 0
    
    num_viridian_unmasked_no_error = 0
    num_colman_unmasked_no_error = 0
    
    num_viridian_error = 0
    num_colman_error = 0
    
    #======================
    NB_VIR_masked = 0
    NB_VIR_sameError = 0
    NB_VIR_same = 0
    NB_VIR_diffError = 0
    NB_VIR_diff = 0
    
    NB_COL_masked = 0
    NB_COL_sameError = 0
    NB_COL_same = 0
    NB_COL_diffError = 0
    NB_COL_diff = 0  
    
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            df_v0 = pd.read_csv(os.path.join(folder_path, file_name), sep='\t')
            df_v1 = df_v0.fillna(0)

            df_v1["VIR"] = df_v1["VIR"].astype(int)
            df_v1["COL"] = df_v1["COL"].astype(int)
            num_viridian_masked += sum(df_v1['label_mar'] == 1)
            num_colman_masked += sum(df_v1['label_ori'] == 1)
            
            num_viridian_unmasked_no_error += sum((df_v1['label_mar'] == 0)&(df_v1['VIR'] == 0))
            num_colman_unmasked_no_error += sum((df_v1['label_ori'] == 0)&(df_v1['COL'] == 0))
            
            num_viridian_error += sum(df_v1['VIR'] == 1)
            num_colman_error += sum(df_v1['COL'] == 1)
            
            #======================

            NB_COL_masked += sum((df_v1['COL'] == 1) & (df_v1['label_mar'] == 1))
            NB_COL_sameError += sum((df_v1['COL'] == 1) & (df_v1['VIR'] == 1) & (df_v1['label_ori'] == 0) & (df_v1['label_mar'] == 0) &(df_v1['nucleotide_martin'] == df_v1['nucleotide_origin']))
            NB_COL_same += sum((df_v1['COL'] == 1) & (df_v1['VIR'] == 0) & (df_v1['label_ori'] == 0) & (df_v1['label_mar'] == 0) &(df_v1['nucleotide_martin'] == df_v1['nucleotide_origin']))
            NB_COL_diffError += sum((df_v1['COL'] == 1) & (df_v1['VIR'] == 1) & (df_v1['label_ori'] == 0) & (df_v1['label_mar'] == 0) &(df_v1['nucleotide_martin'] != df_v1['nucleotide_origin']))
            NB_COL_diff += sum((df_v1['COL'] == 1) & (df_v1['VIR'] == 0) & (df_v1['label_ori'] == 0) & (df_v1['label_mar'] == 0) &(df_v1['nucleotide_martin'] != df_v1['nucleotide_origin']))
            

            NB_VIR_masked += sum((df_v1['VIR'] == 1) & (df_v1['label_ori'] == 1))
            NB_VIR_sameError += sum((df_v1['VIR'] == 1) & (df_v1['COL'] == 1) & (df_v1['label_ori'] == 0) & (df_v1['label_mar'] == 0) &(df_v1['nucleotide_martin'] == df_v1['nucleotide_origin']))
            NB_VIR_same += sum((df_v1['VIR'] == 1) & (df_v1['COL'] == 0) & (df_v1['label_ori'] == 0) & (df_v1['label_mar'] == 0) &(df_v1['nucleotide_martin'] == df_v1['nucleotide_origin']))
            NB_VIR_diffError += sum((df_v1['VIR'] == 1) & (df_v1['COL'] == 1) & (df_v1['label_ori'] == 0) & (df_v1['label_mar'] == 0) &(df_v1['nucleotide_martin'] != df_v1['nucleotide_origin']))
            NB_VIR_diff += sum((df_v1['VIR'] == 1) & (df_v1['COL'] == 0) & (df_v1['label_ori'] == 0) & (df_v1['label_mar'] == 0) &(df_v1['nucleotide_martin'] != df_v1['nucleotide_origin']))
            
    print('====================== Info ======================')
    print('Total masked positions in Virdian assembly: ', num_viridian_masked)
    print('Total positions in Colman assembly: ', num_colman_masked)
    
    print('====================== Info ======================')
    print('Total unmasked positions in Virdian assembly, without errors '
          'identified by MAPLE: ', num_viridian_unmasked_no_error)
    print('Total unmasked positions in Colman assembly, without errors '
          'identified by MAPLE: ', num_colman_unmasked_no_error)
    
    print('====================== Info ======================')
    print('Total positions in Virdian assembly identified as errors by MAPLE '
          '(Virdian\'s errors): ', num_viridian_error)
    print('Total positions in Colman assembly identified as errors by MAPLE '
          '(Colman\'s errors): ', num_colman_error)
    
    print('====================== For VIR error ======================')
    print('Colman’s assemblies are masked: ',NB_VIR_masked)
    print('Same nucleotide, Colman’s assembly error: ',NB_VIR_sameError)
    print('Same nucleotide, Colman’s assembly not error: ',NB_VIR_same)
    print('Diff nucleotide, Colman’s assembly error: ',NB_VIR_diffError)
    print('Diff nucleotide, Colman’s assembly not error: ',NB_VIR_diff)
    print('====================== For COL error ======================')
    print('Viridian’s assemblies are masked: ',NB_COL_masked)
    print('Same nucleotide, Viridian\'s assembly error: ',NB_COL_sameError)
    print('Same nucleotide, Viridian\'s assembly not error: ',NB_COL_same)
    print('Diff nucleotide, Viridian\'s assembly error: ',NB_COL_diffError)
    print('Diff nucleotide, Viridian\'s assembly not error: ',NB_COL_diff)

folder_path = "/nfs/research/goldman/zihao/Datas/p2_compViridian_P3/folderData_addError"
process_files(folder_path)