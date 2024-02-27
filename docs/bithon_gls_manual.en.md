# Get the longest isoform from NCBI genome data


## What is longest isoforms

mRNA transcribed from a single protein-coding gene generates multiple transcripts (splicing variants) by alternative splicing.
([Modrek and Lee 2002](https://doi.org/10.1038/ng0102-13),
[Kelemen et al. 2013](https://doi.org/10.1016/j.gene.2012.07.083),
*etc.*)

`protein.faa` and `cds_from_genomic.fna` on NCBI contains these variants,
thus the number of sequences in FASTA files are more than that of coding genes.

Since various analyses without removing splicing variants can lead to overestimation of gene copy number and other problems,
we often use a single transcript for a single gene (representative sequence).

`bithon gls` supplies one of this method, which is to select the longest splicing variant as representative sequence of each gene.


## Download genome data from NCBI by accession

[`datasets`](https://www.ncbi.nlm.nih.gov/datasets/docs/v2/download-and-install/)
and `curl` get `protein.faa` and `cds_from_genomic.fna` by accession.
(Of course we can get `genomic.fna`, `gff`, `gtf`, *etc*.)

```sh
## datasets
datasets download genome accession GCF_016699485.2 --include cds,protein

## curl
curl -OJ https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/GCF_016699485.2/download?include_annotation_type=CDS_FASTA,PROT_FASTA
```

Unzipping `ncbi_dataset.zip` will inflat each data in `ncbi_dataset/data/_accession_/`.


## Get the longest isoforms using `bithon gls`

See `bithon gls --help`, [`README.md`](https://github.com/ymat2/bithon/blob/main/README.md)

The basic usage of `bithon gls`:

```sh
bithon gls -i ncbi_dataset/data/_accession_ -o output_directory
```

This will generate `longest.pep.fa` and `longest.cds.fa` in `output_directory/`
from `protein.faa` and `cds_from_genomic.fna` in `ncbi_dataset/data/_accession_`.


## Usage for each options

`-p`/`--prefix`
: Specify the prefix instead of `longest`.

`--keep_identity`
: Due to partial sequences and differences in protein sequence prediction models,
  there are often mismatches between sequences translated from `cds_from_genomic.fna` and `protein.faa`.
  `--keep_identity` translates CDS according to the
  [Standard codon table](https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi)
  and keeps only sequences that matches with `protein.faa`.
  If the longest sequence has a mismatch, the longest sequence among those without a mismatch is selected.
  Therefore, dozens to hundreds of genes, including mitochondria-encoded genes, will be lost.
  So this method is not recommended for analyses where the number of genes is important.


`--header`
: `original` or `gene`. By default (`original`), use the ID of the original transcript as the header.
  (ex: `>XP_040503661.1`, `>NC_052532.1_cds_XP_040503661.1_1`)
  `gene` will use "gene.symbol_species.name" as the header.
  (ex: `>CARMIL3_Gallus_gallus`)

`--report`
: Output information about each transcripts. As:

| gene_id | protein_id | protein_length_aa | cds_id | cds_length_bp | identity | species |
| :--- | :--- | ---: | :--- | ---: | :--- | :--- |
| CARMIL3 | XP_040503661.1 | 1135 | NC_052532.1_cds_XP_040503661.1_1 | 3408 | True | Gallus_gallus |
| CARMIL3 | XP_040503669.1 | 1093 | NC_052532.1_cds_XP_040503669.1_2 | 3282 | True | Gallus_gallus |
| CARMIL3 | XP_040503651.1 | 1140 | NC_052532.1_cds_XP_040503651.1_3 | 3423 | True | Gallus_gallus |
| CARMIL3 | XP_040503649.1 | 1148 | NC_052532.1_cds_XP_040503649.1_4 | 3447 | True | Gallus_gallus |
| CARMIL3 | XP_040503637.1 | 1166 | NC_052532.1_cds_XP_040503637.1_5 | 3501 | True | Gallus_gallus |
| CARMIL3 | XP_040503664.1 | 1098 | NC_052532.1_cds_XP_040503664.1_6 | 3297 | True | Gallus_gallus |
| CARMIL3 | XP_040503643.1 | 1153 | NC_052532.1_cds_XP_040503643.1_7 | 3462 | True | Gallus_gallus |
| CARMIL3 | XP_040503634.1 | 1171 | NC_052532.1_cds_XP_040503634.1_8 | 3516 | True | Gallus_gallus |
| DHRS4 | NP_001264054.1 | 273 | NC_052532.1_cds_NP_001264054.1_9  | 822 | True | Gallus_gallus |
| DHRS4 | XP_046798619.1 | 228 | NC_052532.1_cds_XP_046798619.1_10 | 687 | True | Gallus_gallus |
| DHRS4 | XP_046798618.1 | 239 | NC_052532.1_cds_XP_046798618.1_11 | 720 | True | Gallus_gallus |
| LOC121106805 | XP_040503678.1 | 615 | NC_052532.1_cds_XP_040503678.1_12 | 1848 | True | Gallus_gallus |
| LOC121107380 | XP_040507277.1 | 615 | NC_052532.1_cds_XP_040507277.1_13 | 1848 | True | Gallus_gallus |
| LOC121107381 | XP_040507283.1 | 615 | NC_052532.1_cds_XP_040507283.1_14 | 1848 | True | Gallus_gallus |
| LOC121107383 | XP_040507286.1 | 615 | NC_052532.1_cds_XP_040507286.1_15 | 1848 | True | Gallus_gallus |
| ⋮ | | | | | | |

`identity` shows whether protein and translated cds is identical (no mismatch).
