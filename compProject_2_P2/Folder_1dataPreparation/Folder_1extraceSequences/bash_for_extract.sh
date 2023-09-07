#!/bin/bash

# Define the input and output file paths
input_file="/nfs/research/zi/mhunt/Viridian_wf_paper/Vdn_all_ena/Dataset.01/Batches.all_reads"
output_file="/nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_1_dataPrep/folderData_extractSequence"

for i in {1..46}
do
  # Call the script with bsub command using the defined variables
  bsub -M 2000 python3 /nfs/research/goldman/zihao/N_compViridian_2_P2/Folder_1dataPreparation/Folder_1extraceSequences/pg_for_extract.py -i "${input_file}/$i.cons.fa.gz" -o "$output_file"
done
