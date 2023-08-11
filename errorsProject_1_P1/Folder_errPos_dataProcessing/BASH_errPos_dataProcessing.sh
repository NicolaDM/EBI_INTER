#!/bin/bash

# Submit job 1
echo "Submitting job for OUTPUT"
bsub -M 2000 -e /nfs/research/goldman/zihao/N_errorsProject_1/Folder_errPos_dataProcessing/Folder_Checking/errorChecking_errPos_dataProcessing_forOutput.txt -o /nfs/research/goldman/zihao/N_errorsProject_1/Folder_errPos_dataProcessing/Folder_Checking/outputChecking_errPos_dataProcessing_forOutput.txt 'python3 /nfs/research/goldman/zihao/N_errorsProject_1/Folder_errPos_dataProcessing/CODE_errPos_dataProcessing_forOutput.py'
echo "Job for output has been submitted"

# Submit job 2
echo "Submitting job for ANNOT"
bsub -M 2000 -e /nfs/research/goldman/zihao/N_errorsProject_1/Folder_errPos_dataProcessing/Folder_Checking/errorChecking_errPos_dataProcessing_forAnnot.txt -o /nfs/research/goldman/zihao/N_errorsProject_1/Folder_errPos_dataProcessing/Folder_Checking/outputChecking_errPos_dataProcessing_forAnnot.txt 'python3 /nfs/research/goldman/zihao/N_errorsProject_1/Folder_errPos_dataProcessing/CODE_errPos_dataProcessing_forAnnot.py'
echo "Job for ANNOT has been submitted"

# Submit job 3
echo "Submitting job for COV"
bsub -M 2000 -e /nfs/research/goldman/zihao/N_errorsProject_1/Folder_errPos_dataProcessing/Folder_Checking/errorChecking_errPos_dataProcessing_forCov.txt -o /nfs/research/goldman/zihao/N_errorsProject_1/Folder_errPos_dataProcessing/Folder_Checking/outputChecking_errPos_dataProcessing_forCov.txt 'python3 /nfs/research/goldman/zihao/N_errorsProject_1/Folder_errPos_dataProcessing/CODE_errPos_dataProcessing_forCov.py'
echo "Job for COV has been submitted"

