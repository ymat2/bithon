from bithon import fs

def ensembl_gls(infile, outfile, header):
  header2seq = fs.fasta2dict(infile)
  longest_header = dict()
  for hdr, seq in header2seq.items():
    gene_id = [i for i in hdr.split(" ") if i.startswith("gene:")][0]
    gene_id = gene_id.split(":")[1]
    if gene_id not in longest_header:
      longest_header[gene_id] = hdr
    elif len(seq) > len(header2seq[longest_header[gene_id]]):
      longest_header[gene_id] = hdr

  with open(outfile, "w") as f:
    for gn, hdr in longest_header.items():
      if header == "transcript":
        hwr = hdr.split(" ")[0]
      elif header == "id":
        hwr = gn
      elif header == "symbol":
        try:
          hwr = [i for i in hdr.split(" ") if i.startswith("gene_symbol:")][0]
          hwr = hwr.split(":")[1]
        except:
          hwr = gn
      f.write(">"+hwr+"\n")
      f.write(header2seq[hdr]+"\n")
