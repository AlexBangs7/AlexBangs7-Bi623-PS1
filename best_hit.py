#!/usr/bin/env python

import argparse

def get_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("-s1", help="species1", required=True, choices=['Hsa','Dre','Eel','Pka'])
    parser.add_argument("-s2", help="species2", required=True, choices=['Hsa','Dre','Eel','Pka'])
    parser.add_argument("-t", help="running on test files", required=False)
    return parser.parse_args()
args = get_args()

species1 = args.s1
species2 = args.s2

def best_hit(species1=str, species2=str):
    if args.t:
        BLASTp_file = open(f"/projects/bgmp/abangs/bioinfo/Bi623/PS/AlexBangs7-Bi623-PS1/test-files/{species1}_{species2}_test.txt", "r")
    else:
        BLASTp_file = open(f"/projects/bgmp/shared/Bi623/PS1/blasthits/{species1}_query_{species2}_db.txt", "r")

    # Iterate over sorted BLASTp results for species and make dictionary of best hits
    eval_dict = {} # key = query sequence ID, value = [subject sequence ID, e-value, duplicate-flag]
    for line in BLASTp_file:
        if line.startswith("#"):
           continue # skip explanation lines in test files
        line = line.strip("\n").split()
        queryID = line[0]
        subjectID = line[1]
        evalue = float(line[10])
        if queryID in eval_dict:
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
    with open(f"/projects/bgmp/shared/Bi623/PS1/biomart/{species1}_biomart_v116.txt", "r") as tbl:
        for index, line in enumerate(tbl):
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

# Take results of best_hit and print reciprocal best hits to output tsv file
if args.t:
    output_file = open(f"/projects/bgmp/abangs/bioinfo/Bi623/PS/AlexBangs7-Bi623-PS1/test-files/{species1}_{species2}_output_RBH.tsv", "w")
else:
    output_file = open(f'/projects/bgmp/abangs/bioinfo/Bi623/PS/AlexBangs7-Bi623-PS1/output-files/{species1}_{species2}_RBH.tsv',"w")

output_file.write(f'{species1} Gene ID\t{species1} Protein ID\t{species1} Gene Name\t{species2} Gene ID\t{species2} Protein ID\t{species2} Gene Name\n')

for species1_hit, species2_hit in species1_dict.items():
    if species2_hit in species2_dict and species2_dict[species2_hit] == species1_hit:
        gene1_id, gene1_name = species1_genes[species1_hit][0:2]
        #gene1_name = species1_genes[species1_hit][1]
        gene2_id, gene2_name = species2_genes[species2_hit][0:2]
        #gene2_name = species2_genes[species2_hit][1]

        output_file.write(f'{gene1_id}\t{species1_hit}\t{gene1_name}\t{gene2_id}\t{species2_hit}\t{gene2_name}\n')
output_file.close()