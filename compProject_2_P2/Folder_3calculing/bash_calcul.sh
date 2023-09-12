#!/bin/bash

# Command 1_For Venn diff
bsub -M 5000 -e /nfs/research/goldman/zihao/Code/compProject_2_P2/Folder_3calculing/Folder_Checking/vennDiff_allPos_errorChecking.txt -o /nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_3_calculForPLOT/allPos/allPos_vennDiff.txt 'python3 /nfs/research/goldman/zihao/Code/compProject_2_P2/Folder_3calculing/allPOS_diff.py'

# Command 2_For Venn masked
bsub -M 5000 -e /nfs/research/goldman/zihao/Code/compProject_2_P2/Folder_3calculing/Folder_Checking/vennMasked_allPos_errorChecking.txt -o /nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_3_calculForPLOT/allPos/allPos_vennMasked.txt 'python3 /nfs/research/goldman/zihao/Code/compProject_2_P2/Folder_3calculing/allPOS_masked.py'

# Command 3_For Venn same
bsub -M 5000 -e /nfs/research/goldman/zihao/Code/compProject_2_P2/Folder_3calculing/Folder_Checking/vennSame_allPos_errorChecking.txt -o /nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_3_calculForPLOT/allPos/allPos_vennSame.txt 'python3 /nfs/research/goldman/zihao/Code/compProject_2_P2/Folder_3calculing/allPOS_same.py'

# Command 4_For Pie
bsub -M 5000 -e /nfs/research/goldman/zihao/Code/compProject_2_P2/Folder_3calculing/Folder_Checking/pieAllpos_errorChecking.txt -o /nfs/research/goldman/zihao/Datas/p2_compViridian_P2/Folder_3_calculForPLOT/allPos/allPos_pie.txt 'python3 /nfs/research/goldman/zihao/Code/compProject_2_P2/Folder_3calculing/allPOS_pie.py'

# Command For errPos
bsub -M 2000 -e /nfs/research/goldman/zihao/Code/compProject_2_P2/Folder_3calculing/Folder_Checking/errPos_errorChecking.txt -o /nfs/research/goldman/zihao/Code/compProject_2_P2/Folder_3calculing/Folder_Checking/errPos_outputChecking.txt 'python3 /nfs/research/goldman/zihao/Code/compProject_2_P2/Folder_3calculing/errPos.py'