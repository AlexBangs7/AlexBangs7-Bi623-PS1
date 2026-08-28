#!/usr/bin/env python

import argparse
from pathlib import Path

def get_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("-s1","--species1", help="First species", required=True, choices=['Hsa','Dre','Eel','Pka'])
    parser.add_argument("-s2","--species2", help="Second species", required=True, choices=['Hsa','Dre','Eel','Pka'])
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--test", help="running on test files", required=False)
    group.add_argument("--swapPeer", help="running on peer test files. Provide initials of peer, and make sure file names match requirements", required=False)
    return parser.parse_args()
args = get_args()

species1 = args.species1
species2 = args.species2
swapPeer = args.swapPeer

def best_hit(species1=str, species2=str):
    if args.swapPeer:
            BLASTp_file = open(f"/projects/bgmp/abangs/bioinfo/Bi623/PS/AlexBangs7-Bi623-PS1/test-files/peer-swap/{swapPeer}_{species1}_{species2}.txt", "r")
    elif args.test:
        BLASTp_file = open(f"/projects/bgmp/abangs/bioinfo/Bi623/PS/AlexBangs7-Bi623-PS1/test-files/{species1}_{species2}_test.txt", "r")
    else:
        BLASTp_file = open(f"/projects/bgmp/shared/Bi623/PS1/blasthits/{species1}_query_{species2}_db.txt", "r")

    # Iterate over sorted BLASTp results for species and make dictionary of best hits
    eval_dict = {} # key = query sequence ID, value = [subject sequence ID, e-value, toss-flag]
    for line in BLASTp_file:
        if line.startswith("#"):
           continue # skip explanation lines in test files
        line = line.strip("\n").split()
        queryID = line[0]
        subjectID = line[1]
        evalue = float(line[10])
        if queryID in eval_dict:
            if evalue < eval_dict[queryID][1]:
                eval_dict[queryID][0:2] = [subjectID, evalue]
            if evalue == eval_dict[queryID][1] and subjectID != eval_dict[queryID][0]:
                eval_dict[queryID][2] = True 
            else:
                continue
                # 1. if e-vals are different and subjectIDs are different, you already have best hit for different subjectID; 
                # 2. if e-vals are different and subjectIDs are same, you already have best hit for same subjectID; 
                # 3. if e-vals are same and subjectIDs are same, you already have hit for subjectID (and keep it)
        else: # add queryID and best hit to eval_dict
            eval_dict[queryID] = [subjectID, evalue, False]
    BLASTp_file.close()

    # Condense eval_dict by removing best hits that had identical flags for different subject sequence IDs
    best_hit_dict = {} # key = query sequence ID, value = subject sequence ID (no need for e-value anymore)
    for key, value in eval_dict.items():
        if value[2] == False:
            best_hit_dict[key] = value[0]

    # dictionary for identifying all protein IDs and their corresponding gene IDs
    gene_dict = {} # key = protein stable ID, value = [gene stable ID, gene name]
    #if args.swapPeer:
    #    gene_table_file = open(f"/projects/bgmp/abangs/bioinfo/Bi623/PS/AlexBangs7-Bi623-PS1/test-files/peer-swap/{species1}_gene_table.txt", "r")
    #else:
    gene_table_file = open(f"/projects/bgmp/shared/Bi623/PS1/biomart/{species1}_biomart_v116.txt", "r")
    for index, line in enumerate(gene_table_file):
        if index == 0:
            continue
        gene_info = line.strip('\n').split('\t')
        protein_id = gene_info[0]
        gene_id = gene_info[1]
        gene_name = gene_info[2]
        if protein_id not in gene_dict:
            gene_dict[protein_id] = [gene_id,gene_name]
    return best_hit_dict, gene_dict

# Run best_hit for both species
species1_dict, species1_genes = best_hit(species1, species2)
species2_dict, species2_genes = best_hit(species2, species1)

# 3. Take results of best_hit and print reciprocal best hits to output tsv file
# 4. Count number of RBH for each species combination

RBH_count = 0

print(species1_dict)
print(species2_dict)

if args.swapPeer:
    RBH_output = open(f"/projects/bgmp/abangs/bioinfo/Bi623/PS/AlexBangs7-Bi623-PS1/test-files/peer-swap/{swapPeer}_output.tsv", "w")
    count_file = f"/projects/bgmp/abangs/bioinfo/Bi623/PS/AlexBangs7-Bi623-PS1/test-files/peer-swap/{swapPeer}_RBH_count.tsv"

elif args.test:
    RBH_output = open(f"/projects/bgmp/abangs/bioinfo/Bi623/PS/AlexBangs7-Bi623-PS1/test-files/{species1}_{species2}_RBH.tsv", "w")
    count_file = f"/projects/bgmp/abangs/bioinfo/Bi623/PS/AlexBangs7-Bi623-PS1/test-files/RBH_count.tsv"

else:
    RBH_output = open(f'/projects/bgmp/abangs/bioinfo/Bi623/PS/AlexBangs7-Bi623-PS1/output-files/{species1}_{species2}_RBH.tsv',"w")
    count_file = f'/projects/bgmp/abangs/bioinfo/Bi623/PS/AlexBangs7-Bi623-PS1/output-files/RBH_count.tsv'
RBH_output.write(f'{species1} Gene ID\t{species1} Protein ID\t{species1} Gene Name\t{species2} Gene ID\t{species2} Protein ID\t{species2} Gene Name\n')

for species1_hit, species2_hit in species1_dict.items():
    if species2_hit in species2_dict and species2_dict[species2_hit] == species1_hit:
        gene1_id, gene1_name = species1_genes[species1_hit][0:2]
        gene2_id, gene2_name = species2_genes[species2_hit][0:2]
        RBH_count += 1 

        RBH_output.write(f'{gene1_id}\t{species1_hit}\t{gene1_name}\t{gene2_id}\t{species2_hit}\t{gene2_name}\n')
RBH_output.close()

if not args.swapPeer:
    if Path(count_file).exists(): # check if count_output file is empty, and if so write header
        count_output = open(count_file,"a")
        count_output.write(f"\n{species1}\t{species2}\t{RBH_count}")
    else:
        count_output = open(count_file,"a")
        count_output.write(f"Species 1\tSpecies 2\tRBH count")
        count_output.write(f"\n{species1}\t{species2}\t{RBH_count}")
