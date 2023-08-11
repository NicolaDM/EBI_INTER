#!/bin/bash

for i in {1..46}
do
  # Call the script with bsub command
  bsub -M 2000 python3 /nfs/research/goldman/zihao/N_compViridian_2_P2/Folder_1dataPreparation/Folder_1extraceSequences/pg_for_extract.py -i "/nfs/research/zi/mhunt/Viridian_wf_paper/Vdn_all_ena/Dataset.01/Batches.all_reads/$i.cons.fa.gz" -o "/nfs/research/goldman/zihao/Datas/p2_comp_viridian/1_extract_sequence"

done

