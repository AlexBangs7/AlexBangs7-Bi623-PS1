#!/bin/bash


#SBATCH --account=bgmp                    # REQUIRED: which account to use
#SBATCH --partition=bgmp                  # REQUIRED: which partition to use
#SBATCH --cpus-per-task=8                 # optional: number of cpus, default is 1
#SBATCH --job-name=sort-BLASTp-results
#SBATCH --time=2-0:00:00

# Human and Zebrafish
sort -k1,1 -k11,11g /projects/bgmp/shared/Bi623/PS1/blasthits/Dre_query_Hsa_db.txt > sorted-files/Dre_Hsa_sorted.txt
sort -k1,1 -k11,11g /projects/bgmp/shared/Bi623/PS1/blasthits/Hsa_query_Dre_db.txt > sorted-files/Hsa_Dre_sorted.txt

# Human and Eel
sort -k1,1 -k11,11g /projects/bgmp/shared/Bi623/PS1/blasthits/Eel_query_Hsa_db.txt > sorted-files/Eel_Hsa_sorted.txt
sort -k1,1 -k11,11g /projects/bgmp/shared/Bi623/PS1/blasthits/Hsa_query_Pka_db.txt > sorted-files/Hsa_Pka_sorted.txt

# Human and Baby Whale
sort -k1,1 -k11,11g /projects/bgmp/shared/Bi623/PS1/blasthits/Pka_query_Hsa_db.txt > sorted-files/Pka_Hsa_sorted.txt
sort -k1,1 -k11,11g /projects/bgmp/shared/Bi623/PS1/blasthits/Hsa_query_Pka_db.txt > sorted-files/Hsa_Pka_sorted.txt

# Zebrafish and Eel
sort -k1,1 -k11,11g /projects/bgmp/shared/Bi623/PS1/blasthits/Dre_query_Eel_db.txt > sorted-files/Dre_Eel_sorted.txt
sort -k1,1 -k11,11g /projects/bgmp/shared/Bi623/PS1/blasthits/Eel_query_Dre_db.txt > sorted-files/Eel_Dre_sorted.txt

# Zebrafish and Baby Whale
sort -k1,1 -k11,11g /projects/bgmp/shared/Bi623/PS1/blasthits/Dre_query_Pka_db.txt > sorted-files/Dre_Pka_sorted.txt
sort -k1,1 -k11,11g /projects/bgmp/shared/Bi623/PS1/blasthits/Pka_query_Dre_db.txt > sorted-files/Pka_Dre_sorted.txt

# Eel and Baby Whale
sort -k1,1 -k11,11g /projects/bgmp/shared/Bi623/PS1/blasthits/Eel_query_Pka_db.txt > sorted-files/Eel_Pka_sorted.txt
sort -k1,1 -k11,11g /projects/bgmp/shared/Bi623/PS1/blasthits/Pka_query_Eel_db.txt > sorted-files/Pka_Eel_sorted.txt
