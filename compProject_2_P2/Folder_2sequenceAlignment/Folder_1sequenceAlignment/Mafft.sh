#!/bin/bash

i=$1
mafft --6merpair --keeplength --addfragments "/nfs/research/goldman/zihao/Datas/p2_comp_viridian/1_extract_sequence/split_files/output_${i}.fasta" "/nfs/research/goldman/zihao/errorsProject_1/Consensuses/ref_MN908947.3.fasta" > "/nfs/research/goldman/zihao/Datas/p2_comp_viridian/2_alignment/output_${i}_aligned.fasta"

