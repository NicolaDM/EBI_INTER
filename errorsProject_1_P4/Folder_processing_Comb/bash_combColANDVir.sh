#!/bin/bash

# Command 1.1_forViridianAssembly 
bsub -M 2000 -e /nfs/research/goldman/zihao/N_errorsProject_1_P4/Folder_processing_Comb/Folder_Checking/errPos_errorChecking_forVir.txt -o /nfs/research/goldman/zihao/N_errorsProject_1_P4/Folder_processing_Comb/Folder_Checking/errPos_outputChecking_forVir.txt 'python3 /nfs/research/goldman/zihao/N_errorsProject_1_P4/Folder_processing_Comb/pg_errPos_combVir.py'

# Command 1.2_forColmanAssembly 
bsub -M 2000 -e /nfs/research/goldman/zihao/N_errorsProject_1_P4/Folder_processing_Comb/Folder_Checking/errPos_errorChecking_forCol.txt -o /nfs/research/goldman/zihao/N_errorsProject_1_P4/Folder_processing_Comb/Folder_Checking/errPos_outputChecking_forCol.txt 'python3 /nfs/research/goldman/zihao/N_errorsProject_1_P4/Folder_processing_Comb/pg_errPos_combCol.py'

# Command 2.1_forViridianAssembly
bsub -M 20000 -e /nfs/research/goldman/zihao/N_errorsProject_1_P4/Folder_processing_Comb/Folder_Checking/allPos_errorChecking_forVir.txt -o /nfs/research/goldman/zihao/N_errorsProject_1_P4/Folder_processing_Comb/Folder_Checking/allPos_outputChecking_forVir.txt 'python3 /nfs/research/goldman/zihao/N_errorsProject_1_P4/Folder_processing_Comb/pg_allPos_combVir.py'

# Command 2.2_forColmanAssembly 
bsub -M 20000 -e /nfs/research/goldman/zihao/N_errorsProject_1_P4/Folder_processing_Comb/Folder_Checking/allPos_errorChecking_forCol.txt -o /nfs/research/goldman/zihao/N_errorsProject_1_P4/Folder_processing_Comb/Folder_Checking/allPos_outputChecking_forCol.txt 'python3 /nfs/research/goldman/zihao/N_errorsProject_1_P4/Folder_processing_Comb/pg_allPos_combCol.py'