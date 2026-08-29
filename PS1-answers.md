## Part 5: Answer the below questions in PS1_answers.txt


1.  How does the number of RBH’s vary across combinations?
    Any ideas why there is variance (biological or technical)?

    S1	S2	RBH count
    Dre	Eel	10185
    Dre Hsa 7961
    Dre	Pka	9341
    Eel Hsa 9022
    Eel	Pka	10662
    Hsa	Pka	9035

    Generally, the magntitude of RBH counts correspond to phylogenetic proximity and convergent evolution. In terms of proximity, zebrafish and electric eels are most closely related, then electric baby whales, then humans. Eel-Pka have the highest, likely because of similarities in electrogenesis-related proteins. Dre-Eel have the next highest, due to the aforementioned relatedness. Dre-Pka have the next, probably since their both teleosts, then lower counts for all Hsa-fish comparisons.

2.  Describe 1 situation where that you could use 1 or more of your reciprocal best hits file(s) either in an analysis or a workflow.

    The best use case for RBH data is identifying potentially orthologous proteins between species. You would could perform RBH as a way to identify proteins of interest for protein structure identification or protein function prediction. An example not using this data would be to look for naturally-occuring orthologs of fluorescent proteins for the purpose of discovering/developing a new FP with a unique wavelength.

    You can also use it as part of a workflow for identifying phylogenetic proximity, as I alluded to in my answer to Q1.

3.  What are some limits to the RBH approach?

    It only provides data on the best matching orthologs, when at times you might want to look at other orthologs and would then have to go digging through the BLASTp results manually. In this current form, it also only works for pairwise species comparison and couldn't tell you which best hit ortholog is the "most" reciprocal across a variety of species.

4.  Why did we use protein sequences instead of gene sequences in this analysis?

    Because multiple codons can code for the same amino acid, there can be variation in the nucleotide sequence that doesn't translate to variation in peptide sequence, i.e. the variations aren't significant when examining protein orthology. You'd have tons of hits that had a higher BLASTn e-value than BLASTp e-value, which would likely result in many reciprocal best hits being excluded.