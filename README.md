# Bithon

Personal python package for bioinformatics.


## Installation

```sh
python3 -m pip install git+https://github.com/ymat2/bithon
bithon --help  ## show help
```


## Basic usage

### get longest seq from NCBI

See detail:
[日本語版](https://github.com/ymat2/bithon/blob/main/docs/bithon_gls_manual.ja.md),
[English ver.](https://github.com/ymat2/bithon/blob/main/docs/bithon_gls_manual.en.md)

```sh
usage: bithon gls [-h] [-i INDIR] [-o OUTDIR] [-p PREFIX] [--keep_identity] [--header {original,gene}] [--report REPORT]

options:
  -h, --help            show this help message and exit
  -i INDIR, --indir INDIR
                        PATH to directory that contains `cds_from_genomic.fna` and `protein.faa`.
  -o OUTDIR, --outdir OUTDIR
                        PATH to output directory.
  -p PREFIX, --prefix PREFIX
                        default=longest: Prefix of files. `longest.cds.fa` and `longest.pep.fa` will be generated by default.
  --keep_identity       Whether keep only seqs that has no mismatches between Protein and translated CDS.
  --header {original,gene}
                        'original' or 'gene'. Type of fasta header. Original sequence ID will be used by default (`original`).
                        Gene_symbol+species_name will be used when `gene`.
  --report REPORT       Path to report file (.tsv). Ungenerated by default.
```

### get longest seq from ENSEMBL

```sh
bithon ensgls -i infile -o outfile --header str
```

- `-i` / `--infile`: input fasta file name
- `-o` / `--outfile`: output fasta file name
- `--header`: one of "transcript", "id", or "symbol". Chosen one is written as header of fasta.

### prank alignment

Help function to use [`prank`](https://ariloytynoja.github.io/prank-msa/)

```sh
bithon prank -i file_path -o file_name --prank_exe prank_path
```

- `-i` / `--infile`: Fasta file to align
- `-o` / `--outfile`: Path and file name. *file_name*.best.fas are genarated.
- `--prank_exe`: Path for `prank` executable file. Defaut is `prank`.
