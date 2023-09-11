#!/bin/bash
echo "================ Stat for combination ================"
cat /nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_2_combination/folderData_MissingID/*.txt | sort | uniq > /nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_2_combination/missingFile_ids.txt && echo -n "The number of unique missing IDs is: " && wc -l /nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_2_combination/missingFile_ids.txt

echo "================ Stat for annot ================"
cat /nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_2_combination/folderData_missingID—COVAF/missing_ann_ids_*.txt | sort | uniq > /nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_2_combination/missing_annot_ids.txt && echo -n "The number of missing IDs for Annot is: " && wc -l /nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_2_combination/missing_annot_ids.txt

echo "================ Stat for cov ================"
cat /nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_2_combination/folderData_missingID—COVAF/missing_cov_ids_*.txt | sort | uniq > /nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_2_combination/missing_cov_ids.txt && echo -n "The number of missing IDs for COV is: " && wc -l /nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_2_combination/missing_cov_ids.txt

echo "================ Stat total ================"
echo "The total number of missing IDs is: $(( $(wc -l < /nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_2_combination/missing_annot_ids.txt) + $(wc -l < /nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_2_combination/missing_cov_ids.txt) ))"
