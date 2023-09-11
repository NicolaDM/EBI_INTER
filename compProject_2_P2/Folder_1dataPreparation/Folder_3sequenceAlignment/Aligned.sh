#!/bin/bash

for i in {1..10}
do
  bsub sh /nfs/research/goldman/zihao/N_compViridian_2_P2/Folder_2sequenceAlignment/Mafft.sh ${i}
done

