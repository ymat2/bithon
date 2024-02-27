from bithon import fs
import os

def gls_main(args):
  faa = args.indir+"/protein.faa"
  fna = args.indir+"/cds_from_genomic.fna"

  fna2dict = fs.fasta2dict(fna)
  fna2dict = parse_fna(fna2dict)

  faa2dict = fs.fasta2dict(faa)
  faa2dict = parse_faa(faa2dict)

  df_report = dict()
  for k, v in fna2dict.items():
    prot_id = k
    [cds_id, gene_id, cds_seq] = v
    [sp_name, prot_seq] = faa2dict.get(prot_id, ["NaN", ""])
    idnty = str(is_identical(cds_seq, prot_seq))
    df_report[prot_id] = [gene_id, prot_id, str(len(prot_seq)), cds_id, str(len(cds_seq)), idnty, sp_name]

  if args.report:
    with open(args.report, "w") as f:
      _header = ["gene_id", "protein_id", "protein_length_aa", "cds_id", "cds_length_bp", "identity", "species"]
      f.write("\t".join(_header)+"\n")
      for v in df_report.values():
        f.write("\t".join(v)+"\n")

  fna2dict = {v[0]: v[2] for v in fna2dict.values()}
  faa2dict = {k: v[1] for k, v in faa2dict.items()}

  df_longest = gls(df_report, keep = args.keep_identity)

  if args.header == "gene":
    fna2dict = {v[0]+"_"+v[-1]: fna2dict[v[3]] for v in df_longest.values() if v[3] in fna2dict}
    faa2dict = {v[0]+"_"+v[-1]: faa2dict[v[1]] for v in df_longest.values() if v[1] in faa2dict}
  else:
    fna2dict = {v[3]: fna2dict[v[3]] for v in df_longest.values() if v[3] in fna2dict}
    faa2dict = {v[1]: faa2dict[v[1]] for v in df_longest.values() if v[1] in faa2dict}

  if not os.path.exists(args.outdir):
    print(f"\t{args.outdir}/ does not exitst. It will be newly created.")
    os.makedirs(args.outdir)
  fs.write_fasta(fna2dict, args.outdir+"/"+args.prefix+".cds.fa")
  print(f"\tWrite out CDS: {len(fna2dict)} sequences.")
  fs.write_fasta(faa2dict, args.outdir+"/"+args.prefix+".pep.fa")
  print(f"\tWrite out Protein: {len(faa2dict)} sequences.")

def parse_fna(d: dict) -> dict:
  ids = dict()
  for k, v in d.items():
    cds_id = k.rstrip("\n").split(" ")[0].split("|")[1]
    desc = k.rstrip("\n").split(" ")[1:]
    desc = [i.strip("[]") for i in desc]
    desc = {i.split("=")[0]: i.split("=")[1] for i in desc if "=" in i}
    prot_id = desc.get("protein_id", "NA")
    gene_id = desc.get("gene", "NA")
    ids[prot_id] = [cds_id, gene_id, v]
  return ids


def parse_faa(d: dict) -> dict:
  ids = dict()
  for k, v in d.items():
    prot_id = k.rstrip("\n").split(" ")[0]
    desc = k.rstrip("\n").split(" ")[1:]
    sp_name = " ".join(desc)
    sp_name = sp_name.rstrip("]").split("[")[-1]
    sp_name = sp_name.replace(" ", "_")
    ids[prot_id] = [sp_name, v]
  return ids


def is_identical(cds: str, pep: str) -> bool:
  from Bio.Seq import Seq
  if len(cds)%3 == 1:
    cds = cds + "NN"
  elif len(cds)%3 == 2:
    cds = cds + "N"
  cds = Seq(cds)
  cds = cds.translate(table="Standard", stop_symbol="*", to_stop=False, cds=False, gap=None)
  cds = cds.rstrip("*")
  return str(cds) == pep


def gls(ids: dict, keep: bool) -> dict:
  longest = dict()
  for v in ids.values():
    gene_id = v[0]
    len_cds = int(v[4])
    identity = v[5]
    if keep and not (identity == "True"):
      continue
    if gene_id not in longest:
      longest[gene_id] = v
    elif len_cds > int(longest[gene_id][4]):
      longest[gene_id] = v
  return longest


if __name__ == "__main__":
  gls_main()
