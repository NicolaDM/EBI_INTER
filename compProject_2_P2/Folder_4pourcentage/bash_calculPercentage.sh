#!/bin/bash

# Command 1_For Venn diff
bsub -M 2000 -e /nfs/research/goldman/zihao/Code/compProject_2_P2/Folder_4pourcentage/Folder_Checking/vennDiff_allPos_errorChecking.txt -o /nfs/research/goldman/zihao/Datas/p2_comp_viridian/Folder_4_percentage/allPos_resultVenn_diff.txt 'python3 /nfs/research/goldman/zihao/Code/compProject_2_P2/Folder_4pourcentage/1.2.1_For_venn_diff.py'

# Command 2_For Venn masked
bsub -M 2000 -e /nfs/research/goldman/zihao/Code/compProject_2_P2/Folder_4pourcentage/Folder_Checking/vennMasked_allPos_errorChecking.txt -o /nfs/research/goldman/zihao/Datas/p2_comp_viridian/Folder_4_percentage/allPos_resultVenn_masked.txt 'python3 /nfs/research/goldman/zihao/Code/compProject_2_P2/Folder_4pourcentage/1.2.2_For_venn_masked.py'

# Command 3_For Venn same
bsub -M 2000 -e /nfs/research/goldman/zihao/Code/compProject_2_P2/Folder_4pourcentage/Folder_Checking/vennSame_allPos_errorChecking.txt -o /nfs/research/goldman/zihao/Datas/p2_comp_viridian/Folder_4_percentage/allPos_resultVenn_same.txt 'python3 /nfs/research/goldman/zihao/Code/compProject_2_P2/Folder_4pourcentage/1.2.3_For_venn_same.py'

# Command 4_For Pie
bsub -M 2000 -e /nfs/research/goldman/zihao/Code/compProject_2_P2/Folder_4pourcentage/Folder_Checking/pieAllpos_errorChecking.txt -o /nfs/research/goldman/zihao/Datas/p2_comp_viridian/Folder_4_percentage/allPos_resultPie.txt 'python3 /nfs/research/goldman/zihao/Code/compProject_2_P2/Folder_4pourcentage/1.1_Calculate_percentage_all_pos.py'