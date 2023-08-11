#!/bin/bash

# ==================Requires modification==================
# batch_size: Number of documents processed per batch.
# folder_path_1: Path to the Viridian Assembly\'s FASTA files.
# folder_path_2: Path to the Colman Assembly\'s FASTA files.
# output_folder: The output folder.
# ==================Requires modification==================

# Define input and output paths
batch_size=5000
folder_path_1="/nfs/research/goldman/zihao/Datas/p2_comp_viridian/2_alignment/Aligned_split/"
folder_path_2="/nfs/research/goldman/zihao/Datas/p1/File_5_consensus/Decompress/Aligned_split_July_for_MAPLE"

output_folder="/nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_2_combination/folderData_combination/"

# Get the number of batches
file_names=$(ls $folder_path_1)
total_files=$(echo $file_names | wc -w)
batch_num=$((total_files / batch_size))
last_batch_files=$((total_files % batch_size))

# Process each batch
for i in $(seq 1 $batch_num)
do
  bsub -M 2000 python3 /nfs/research/goldman/zihao/N_compViridian_2_P2/Folder_2sequenceAlignment/Folder_2dataCombination/pg_combination.py $folder_path_1 $folder_path_2 $output_folder $i $batch_size
done

# Process the last batch
if [ $last_batch_files -gt 0 ]
then
  bsub -M 2000 python3 /nfs/research/goldman/zihao/N_compViridian_2_P2/Folder_2sequenceAlignment/Folder_2dataCombination/pg_combination.py $folder_path_1 $folder_path_2 $output_folder $((batch_num + 1)) $batch_size
fi
