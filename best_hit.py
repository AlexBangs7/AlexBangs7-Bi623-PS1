#!/usr/bin/env python

import argparse

def get_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("-s1", help="species1", required=True, choices=['Hsa','Dre','Eel','Pka'])
    parser.add_argument("-s2", help="species2", required=True, choices=['Hsa','Dre','Eel','Pka'])

    return parser.parse_args()
args = get_args()

species1 = args.s1
species2 = args.s2


def best_hit(species=str):

    # Iterate over sorted BLASTp results for species and make dictionary of best hits
    with open(f"sorted-BLASTp-results/{species}_sorted.txt", "r") as file:
        eval_dict = {} # key = query sequence ID, value = [subject sequence ID, e-value, duplicate-flag]
        for line in file:
            line = line.strip("\n").split()
            queryID = line[0]
            subjectID = line[1]
            evalue = float(line[10])
            if queryID in eval_dict:
                if evalue == eval_dict[queryID][1] and subjectID != eval_dict[queryID][0]:
                    eval_dict[queryID][2] = True
                    #mark identical flag as TRUE # if subject ID is the same as dictionary's subjectID, then should not mark as duplicate
            else:
                eval_dict[queryID] = [subjectID, evalue, False] #add to dictionary {query: [subjectID, evalue, FALSE duplicate flag]}

    # Condense eval_dict by removing best hits that had identical flags for different subject sequence IDs
    best_hit_dict = {} # key = query sequence ID, value = subject sequence ID
    for key, value in eval_dict.items():
        if value[2] == False:
            best_hit_dict[key] = value[0]

    # dictionary for identifying all protein IDs and their corresponding gene IDs
    gene_dict = {} # key = protein stable ID, value = [gene stable ID, gene name]
    with open(f"/projects/bgmp/shared/Bi623/PS1/biomart/{species}_biomart_v116.txt", "r") as tbl:
        for index, line in enumerate(tbl):
            if index == 0:
                continue
            gene_info = line.strip('\n').split('\t')
            gene_id = gene_info[0]
            gene_name = gene_info[1]
            protein_id = gene_info[2]
            if protein_id not in gene_dict:
                gene_dict[protein_id] = [gene_id,gene_name]
    return best_hit_dict, gene_dict


with open(f'{species1}_{species2}.txt',"w") as output:
    for species1_hit, species2_hit in species1_dict.items():
        # print(species1_hit, species2_hit)
        if species2_hit in species2_dict and species2_dict[species2_hit] == species1_hit:
            output.write(f'{species2_hit}\t{species1_hit}\n')