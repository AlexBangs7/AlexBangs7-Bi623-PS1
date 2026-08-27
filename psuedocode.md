## Problem:

0. Sort blastp results by best e-value for each protein query

1. First, the script should filter blastp results and only retain the best hit(s) for each protein query based on e-value. **Note: you can write a bash command to sort the data**

2. Next, the script should determine which best hits share a 1:1 (species1:species2) reciprocal best hit. **Note: In your pseudocode, please note all cases where protein hits should be discarded.**

- Protein hits should be discarded if two separate subject sequence IDs (i.e. two unique copies of the gene in the reference genome) have the same e-value. **Except when you have two identical subject sequence IDs (i.e. two reads of the same one gene in the reference genome) with the same e-value, they should be kept.**

3. Finally, the script should output a tab separated table of all proteins with reciprocal best hits. **Formatting note: Species 1 Gene ID, Species 1 Protein ID, Species 1 Gene Name, Species 2 Gene ID, Species 2 Protein ID, Species 2 Gene Name Note: Your output file should have a HEADER line to explain each column**

- If the gene does not have gene name available, write out an empty string for the gene name **Example: ENSDARG500, ENSDARP500, shha, ENSEEG919, ENSEEP919,**

First, think your blastp output. Write out all cases where we want to keep a blast hit. Then, write down all cases where we want to remove a blast hit. Finally, write or draw pseudo-code for how to approach the reciprocal best hit script.

## Output:

Tab separated file containing all reciprocal best hits in following format:

| Species 1 Gene ID | Species 1 Protein ID | Species 1 Gene Name | Species 2 Gene ID | Species 2 Protein ID | Species 2 Gene Name |
| ----------- | ----------- | ----------- | ----------- | ----------- | ----------- |


## Psuedocode:
```
# 1. Filter blastp results and retain the best hit(s) for each protein query based on e-value
# a. Sort blastp results by qseqid (column 1) and e-value (column 11) and move to tsv file (bash)

sort by query sequence ID then by e-value | cut down to just the query sequence ID, the subject sequence ID, and e-value column > write to new txt file

# b. Take sorted txt file and add best e-value entry to new best e-value file

Create dictionary with following format: {key = query ID: value = [subject ID, e-value, identical e-value flag]}

for line in sorted file:
    split strip each line
    queryID = line[0]
    subjectID = line[1]
    evalue = line[2]
    if queryID already in dictionary:
        if evalue the same as dictionary's evalue AND if subjectID not the same as dictionary's subjectID: 
            mark identical flag as TRUE # if subject ID is the same as dictionary's subjectID, then should not mark as duplicate
    else:
        add to dictionary {query: [subjectID, evalue, FALSE duplicate flag]}

Remove all dictionary entries with identical flag == TRUE:

# 2. Next, the script should determine which best hits share a 1:1 (species1:species2) reciprocal best hit. This is a smaller list/dictionary of only the proteins that are the best hit for both blast runs

For each species, make dictionary of Ensembl biomart data for gene ID, gene name, and protein ID (ENS_Human_genes_116.txt, or ENS_Zfish_genes_116.txt).

for species1_hit, species2_hit in species1 dictionary:
    if species2_hit is a key in species2 dictionary and the corresponding species2 dictionary value is species1_hit:
        write the gene id, protein id, and gene name for species1_hit and species2_hit to output file

# 3. Finally, the script should output a tab separated table of all proteins with reciprocal best hits. Formatting note: Species 1 Gene ID, Species 1 Protein ID, Species 1 Gene Name, Species 2 Gene ID, Species 2 Protein ID, Species 2 Gene Name Note: Your output file should have a HEADER line to explain each column

If the gene does not have gene name available, write out an empty string for the gene name Example: ENSDARG500, ENSDARP500, shha, ENSEEG919, ENSEEP919, 

```