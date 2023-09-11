#!/bin/bash
# ==================Requires modification==================
# input_file_base
# input_file_suffix
# output_file
# ==================Requires modification==================

# Define the input and output file paths、
input_file_base="/nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_1_dataPrep/Folder_alignment/output_"
input_file_suffix="_aligned.fasta"
output_file="/nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_1_dataPrep/Folder_alignment/folderData_alignedSplit"

for i in {1..10}

do
  # Construct the full input file path for the current iteration
  input_file="${input_file_base}${i}${input_file_suffix}"

  # Call the script with bsub command using the defined variables
  bsub -M 2000 python3 /nfs/research/goldman/zihao/N_compViridian_2_P2/Folder_2sequenceAlignment/Folder_1sequenceAlignment/pg_splitAligned.py -i "$input_file" -o "$output_file"
done
