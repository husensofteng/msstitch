# msstitch -- MS proteomics post-processing utilities

Shotgun proteomics has a number of bioinformatic tools available for identification 
and quantification of peptides, and the subsequent protein inference. A problem which
remains is that to generate a full end-user compatible output table one often has to
resort to a full suite of tools. Suites can be very well made, reliable and accepted
by the field, but they are "large" monoliths.

These scripts are written to scratch an itch felt some years ago when combining 
existing tools, and act as small command-line runnable programs that do small
things such as adding values to a PSM table, manipulating percolator results or grouping
proteins. They are capable of combining multiple different output formats into
complete output.

Small things take short time to update, are easy to parallelize, and tools that 
generate input data for these scripts can usually be upgraded without having to 
wait for a full tool suite update (unless large output format changes apply).
While the tools are not per definition user-friendly in that there is no GUI or
chaining/integration, they are easy to implement in frameworks such as Galaxy
or Taverna.

We currently support the tools we run ourselves, but these could easily be extended
to include more tool output formats.

## Tools

- [mslookup](#mslookup) - Creates SQLite databases from spectra, search and quantification data
- [pycolator](#pycolator) - Splits, merges, filters percolator XML results, and runs qvality
- [mzidtsv](#mzidtsv) - Filters, splits, merges, and proteingroups on PSM tables from MSGF+. Also adds columns with extra data (quant, percolator, genes, etc)
- [peptable](#peptable) - Creates and manipulates peptide tables (merging, quant data additions, etc)
- [prottable](#prottable) - Idem for protein tables, including determining protein FDR


<a name="mslookup"></a>
### mslookup
Generates SQLite database files of various MS data. Can e.g. be used to store statistical
or quant data of multiple experiment sample sets, whereafter these can be merged. But it
also does protein grouping and sequence filtering thanks to the power of the DB engine.

Example: Store a multi-set tab-separated PSM table:

`python3 mslookup.py -c psms -i psmtable.txt --spectracol 2 --fasta ENSEMBL80.fa --map ENS80_biomart.txt`

<a name="pycolator"></a>
### pycolator
Performs various operations on percolator output XML, e.g. splitting into target and decoy,
merging, filtering peptides, runs qvality and reassigns qvality output statistics to 
existing percolator output.

Example: filter unique peptides on best score of a merged percolator file

`python3 pycolator.py filteruni -i percolator.xml`

<a name="mzidtsv"></a>
### mzidtsv
Use this for modifications of tab-separated PSM tables generated by MSGF+ (supported)
or other tools.

Example: add MS2 quant data to PSM table from SQLite lookup (resulting from mslookup)

`python3 mzidtsv.py -c quanttsv -i psmtable.txt --dbfile db.sqlite --isobaric`

Example 2: Split PSM table into multiple tables on column "Biological set"

`python3 mzidtsv.py -c splittsv -i psmtable.txt --bioset`


<a name="peptable"></a>
### peptable
Creates and modifies peptide tables

Example: create a peptide table by filtering best peptides from PSM table and removing isobaric quant data.
Retains MS1 quant data by taking the highest MS1 quant for a given peptide sequence.

`python3 peptable.py -c psm2pep -i psmtable.txt --spectracol 2 --scorecolpattern svm --ms1quantcolpattern area --isobquantcolpattern tmt10plex`

Example: Create column in peptide table with linear modeled q-values

`python3 peptable.py -c modelqvals -i peptides.txt --qcolpattern "^q-value" --scorecolpattern svm`

<a name="prottable"></a>
### prottable
Creates and modifies protein tables, also runs qvality on these for FDR calculation

Example: Add best-scoring peptide to protein table (Q-score by Savitsky et al 2014)

`python3 prottable.py -c bestpeptide -i proteins.txt --peptable peptides.txt --scorecolpattern svm --logscore`

Example: Add FDR from qvality result to protein table using Q-scores as keys to look up
corresponding q-values and PEPs

`python3 prottable.py -c addfdr -i proteins.txt --qvality qvals.txt --scorecolpattern "^Q-score"`
