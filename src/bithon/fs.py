def fasta2dict(fasta: str) -> dict:
  f2d = dict()
  with open(fasta) as f:
    _tmp_header = ""
    for line in f:
      if line[0] == ">":
        _tmp_header = line.rstrip("\n")[1:]
        f2d[_tmp_header] = ""
      else:
        _seq = line.rstrip("\n")
        f2d[_tmp_header] = "".join([f2d[_tmp_header], _seq])
  return f2d


def write_fasta(d: dict, outfile: str) -> None:
  with open(outfile, "w") as f:
    for k, v in d.items():
      f.write(">"+k+"\n"+v+"\n")
