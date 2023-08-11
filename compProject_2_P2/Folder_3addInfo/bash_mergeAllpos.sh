#!/bin/bash

# ==================Requires modification==================
# batch_size: Number of documents processed per batch.
# input_folder: Path to the DataFrame merged in the previous step
# merge_dir: The output folder.
# ==================Requires modification==================

# Define paths
batch_size=100
input_folder="/nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_2_combination/folderData_combination"
merge_dir="/nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_3_mergeINFO/folderData_mergeFile"

# Get the number of files
files=$(ls $input_folder)
total_files=$(echo $files | wc -w)
batch_num=$((total_files / batch_size))
last_batch_files=$((total_files % batch_size))

# Process each batch
for i in $(seq 1 $batch_num)
do
  bsub -M 2000 python3 /nfs/research/goldman/zihao/N_compViridian_2_P2/Folder_3addInfo/pg_mergeAllpos.py --input_folder "$input_folder" --merge_dir "$merge_dir" --output $i
done

# Process the last batch
if [ $last_batch_files -gt 0 ]
then
  bsub -M 2000 -o "/nfs/research/goldman/zihao/N_compViridian_2_P2/Folder_3addInfo/Folder_Checking/mergeAllpos_outputChecking.txt" python3 /nfs/research/goldman/zihao/N_compViridian_2_P2/Folder_3addInfo/pg_mergeAllpos.py --input_folder "$input_folder" --merge_dir "$merge_dir" --output $((batch_num + 1))
fi


