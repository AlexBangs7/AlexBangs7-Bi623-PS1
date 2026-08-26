#!/usr/bin/env python

import argparse

def get_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("-s1", help="species1", required=True)
    parser.add_argument("-s2", help="species2", required=True)

    return parser.parse_args()
args = get_args()

species1_BLAST = args.s1 + "_sorted.txt"
species1 = args.s1
species2_BLAST = args.s2 + "_sorted.txt"
species2 = args.s2


eval_dict_1 = {} # key = query sequence ID, value = [subject sequence ID, e-value, duplicate-flag]
eval_dict_2 = {} # key = query sequence ID, value = [subject sequence ID, e-value, duplicate-flag]

with open(species1_BLAST, "r") as file:
    for line in file:
        line = line.strip("\n").split()
        queryID = line[0]
        subjectID = line[1]
        evalue = float(line[2])
        if queryID in eval_dict_1:
            if evalue == eval_dict_1[queryID][1] and subjectID != eval_dict_1[queryID][0]:
                eval_dict_1[queryID][2] = True
                #mark identical flag as TRUE # if subject ID is the same as dictionary's subjectID, then should not mark as duplicate
        else:
            eval_dict_1[queryID] = [subjectID, evalue, False] #add to dictionary {query: [subjectID, evalue, FALSE duplicate flag]}


with open(species2_BLAST, "r") as file:
    for line in file:
        line = line.strip("\n").split()
        queryID = line[0]
        subjectID = line[1]
        evalue = float(line[2])
        if queryID in eval_dict_2:
            if evalue == eval_dict_2[queryID][1] and subjectID != eval_dict_2[queryID][0]:
                eval_dict_2[queryID][2] = True
                #mark identical flag as TRUE # if subject ID is the same as dictionary's subjectID, then should not mark as duplicate
        else:
            eval_dict_2[queryID] = [subjectID, evalue, False] #add to dictionary {query: [subjectID, evalue, FALSE duplicate flag]}


species1_dict = {}
for key, value in eval_dict_1.items():
    if value[2] == False:
        species1_dict[key] = value[0]

species2_dict = {}
for key, value in eval_dict_2.items():
    if value[2] == False:
        species2_dict[key] = value[0]

# print(species1_dict)
# print(species2_dict)

with open(f'{species1}_{species2}.txt',"w") as output:
    for species1_hit, species2_hit in species1_dict.items():
        # print(species1_hit, species2_hit)
        if species2_hit in species2_dict and species2_dict[species2_hit] == species1_hit:
            output.write(f'{species2_hit}\t{species1_hit}\n')