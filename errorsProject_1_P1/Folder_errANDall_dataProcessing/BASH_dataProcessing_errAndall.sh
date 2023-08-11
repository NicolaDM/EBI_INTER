#!/bin/bash

# Submit job 1
echo "Submitting job for OUTPUT"
bsub -M 2000 -e /nfs/research/goldman/zihao/Code/errorsProject_1_P1/Folder_errANDall_dataProcessing/Folder_Checking/errorChecking_errPos_dataProcessing_forOutput.txt -o /nfs/research/goldman/zihao/Code/errorsProject_1_P1/Folder_errANDall_dataProcessing/Folder_Checking/outputChecking_errPos_dataProcessing_forOutput.txt 'python3 /nfs/research/goldman/zihao/Code/errorsProject_1_P1/Folder_errPos_dataProcessing/CODE_errPos_dataProcessing_forOutput.py'
echo "Job for output has been submitted"

# Submit job 2
echo "Submitting job for ANNOT"
bsub -M 2000 -e /nfs/research/goldman/zihao/Code/errorsProject_1_P1/Folder_errANDall_dataProcessing/Folder_Checking/errorChecking_errPos_dataProcessing_forAnnot.txt -o /nfs/research/goldman/zihao/Code/errorsProject_1_P1/Folder_errANDall_dataProcessing/Folder_Checking/outputChecking_errPos_dataProcessing_forAnnot.txt 'python3 /nfs/research/goldman/zihao/Code/errorsProject_1_P1/Folder_errPos_dataProcessing/CODE_errPos_dataProcessing_forAnnot.py'
echo "Job for ANNOT has been submitted"

# Submit job 3
echo "Submitting job for COV"
bsub -M 2000 -e /nfs/research/goldman/zihao/Code/errorsProject_1_P1/Folder_errANDall_dataProcessing/Folder_Checking/errorChecking_errPos_dataProcessing_forCov.txt -o /nfs/research/goldman/zihao/Code/errorsProject_1_P1/Folder_errANDall_dataProcessing/Folder_Checking/outputChecking_errPos_dataProcessing_forCov.txt 'python3 /nfs/research/goldman/zihao/Code/errorsProject_1_P1/Folder_errPos_dataProcessing/CODE_errPos_dataProcessing_forCov.py'
echo "Job for COV has been submitted"

# Submit job 4
echo "Submitting job for all Positions"
bsub -M 20000 -e /nfs/research/goldman/zihao/Code/errorsProject_1_P1/Folder_errANDall_dataProcessing/Folder_Checking/errorChecking_allPos_dataProcessing.txt -o /nfs/research/goldman/zihao/Code/errorsProject_1_P1/Folder_errANDall_dataProcessing/Folder_Checking/outputChecking_allPos_dataProcessing.txt 'python3 /nfs/research/goldman/zihao/Code/errorsProject_1_P1/Folder_allPos_dataProcessing/CODE_allPos_dataProcessing.py'
echo "Job for all Positions has been submitted"

