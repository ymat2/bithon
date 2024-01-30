from bithon import fs, parsegtf

def ncbi_gls(params):
  if params['gtf']:
    gtf = params['gtf']
    prot2gene = parsegtf.prot2gene(gtf)
    print("\tFinish parsing GTF file.")
  else:
    raise FileNotFoundError("GTF file not found.")

  if params['pep'] and params['cds']:
    pep = params['pep']
    pep = fs.fasta2dict(pep)
    cds = params['cds']
    cds = fs.fasta2dict(cds)
    cds = {fs.get_prot_id(k): v for k,v in cds.items()}
    longest = dict()

    for k in pep.keys():
      protid = k.split(" ")[0]
      geneid = prot2gene[protid]
      species_name = fs.get_species_name(k)
      geneid = geneid+"_"+species_name
      if geneid not in longest:
        longest[geneid] = [pep[k], cds[protid]]
      elif len(pep[k]) > len(longest[geneid][0]):
        longest[geneid] = [pep[k], cds[protid]]

    longest_pep, longest_cds = dict(), dict()
    for gn in longest:
      longest_pep[gn] = longest[gn][0]
      longest_cds[gn] = longest[gn][1]
    fs.write_fasta(longest_pep, params['outdir']+".pep.fa")
    fs.write_fasta(longest_cds, params['outdir']+".cds.fa")
    print("\tSelected sequences: {} genes.".format(len(longest)))

  if params['pep'] and not params['cds']:
    pep = params['pep']
    pep = fs.fasta2dict(pep)
    longest = dict()

    for k, v in pep.items():
      protid = k.split(" ")[0]
      geneid = prot2gene[protid]
      species_name = fs.get_species_name(k)
      geneid = geneid+"_"+species_name
      if geneid not in longest:
        longest[geneid] = v
      elif len(v) > len(longest[geneid][1]):
        longest[geneid] = v

    fs.write_fasta(longest, params['outdir']+".pep.fa")
    print("\tSelected sequences: {} genes.".format(len(longest)))
