#!/bin/bash

batch_size=5000
folder_path_1="/nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_1_dataPrep/Folder_alignment/folderData_alignedSplit/"
folder_path_2="/nfs/research/goldman/zihao/Datas/p1/File_5_consensus/Decompress/Aligned_split_July_for_MAPLE"
output_folder="/nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_2_combination/folderData_addInfo"

# Get the number of batches
file_names=$(ls $folder_path_1)
total_files=$(echo $file_names | wc -w)
batch_num=$((total_files / batch_size))
last_batch_files=$((total_files % batch_size))

# Process each batch
for i in $(seq 1 $batch_num)
do
  bsub -M 20000 python3 /nfs/research/goldman/zihao/Code/compProject_2_P2/Folder_2addInfo/pg_mergeAllpos.py $folder_path_1 $folder_path_2 $output_folder $i $batch_size
done

# Process the last batch
if [ $last_batch_files -gt 0 ]
then
  bsub -M 20000 python3 /nfs/research/goldman/zihao/Code/compProject_2_P2/Folder_2addInfo/pg_mergeAllpos.py $folder_path_1 $folder_path_2 $output_folder $((batch_num + 1)) $batch_size
fi