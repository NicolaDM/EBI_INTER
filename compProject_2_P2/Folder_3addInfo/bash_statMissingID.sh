#!/bin/bash

echo "================ Stat for annot ================"

cat /nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_3_mergeINFO/folderData_missingData/missing_ann_ids_*.txt | sort | uniq > /nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_3_mergeINFO/missing_ann_ids.txt && echo -n "The number of missing IDs for Annot is: " && wc -l /nfs/research/goldman/zihao/Datas/p2_comp_viridian/Folder_3_mergeINFO/missing_ann_ids.txt

echo "================ Stat for cov ================"

cat /nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_3_mergeINFO/folderData_missingData/missing_cov_ids_*.txt | sort | uniq > /nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_3_mergeINFO/missing_cov_ids.txt && echo -n "The number of missing IDs for COV is: " && wc -l /nfs/research/goldman/zihao/Datas/p2_comp_viridian/Folder_3_mergeINFO/missing_cov_ids.txt

echo "================ Stat total ================"
echo "The total number of missing IDs is: $(( $(wc -l < /nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_3_mergeINFO/missing_ann_ids.txt) + $(wc -l < /nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_3_mergeINFO/missing_cov_ids.txt) ))"
