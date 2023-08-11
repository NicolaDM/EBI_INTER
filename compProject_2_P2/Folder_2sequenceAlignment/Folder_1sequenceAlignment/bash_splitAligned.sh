#!/bin/bash

for i in {1..10}
do
  # Call the script with bsub command
  bsub -M 2000 python3 /nfs/research/goldman/zihao/N_compViridian_2_P2/Folder_2sequenceAlignment/Folder_1sequenceAlignment/pg_splitAligned.py -i "/nfs/research/goldman/zihao/Datas/p2_comp_viridian/2_alignment/output_${i}_aligned.fasta" -o "/nfs/research/goldman/zihao/Datas/p2_comp_viridian/2_alignment/Aligned_split"
done
