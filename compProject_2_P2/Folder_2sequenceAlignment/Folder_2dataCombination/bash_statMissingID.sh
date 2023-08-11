#!/bin/bash

cat /nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_2_combination/folderData_MissingID/*.txt | sort | uniq > /nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_2_combination/folderData_MissingID/MissingID.txt && echo -n "The number of unique missing IDs is: " && wc -l /nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_2_combination/folderData_MissingID/MissingID.txt
