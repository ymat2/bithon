# Bithon

Personal pyhton package for bioinformatics.


## Installation

```sh
python3 -m pip install git+https://github.com/ymat2/bithon
```


## Basic usage

### get longest seq from NCBI

```sh
bithon ngls -i indir -o outdir
```

- `-i` / `--indir`: Directory contains cds, pep, and gtf
- `-o` / `--outdir`: *outdir*.pep.fa and *outdir*.cds.fa are generated

### get longest seq from ENSEMBL

```sh
bithon egls -i infile -o outfile --header str
```

- `-i` / `--infile`: input fasta file name
- `-o` / `--outfile`: output fasta file name
- `--header`: one of "transcript", "id", or "symbol". Chosen one is written as header of fasta.

### prank alignment

```sh
bithon prank -i file_path -o file_name --prank_exe prank_path
```

- `-i` / `--infile`: Fasta file to align
- `-o` / `--outfile`: Path and file name. *file_name*.best.fas are genarated.
- `--prank_exe`: Path for `prank` executable file. Defaut is `prank`.
