def fasta2dict(path):
  seq_dict = dict()
  with open(path) as f:
    tmp_header = ""
    for line in f:
      if line[0] == ">":
        tmp_header = line.rstrip("\n")[1:]
        seq_dict[tmp_header] = ""
      else:
        seq_dict[tmp_header] += line.rstrip("\n")
  return seq_dict


def write_fasta(seq_dict, outfile):
  with open(outfile, 'w') as f:
    for id, seq in seq_dict.items():
      f.write(">"+str(id)+"\n"+str(seq)+"\n")


def get_species_name(string):
  sp_name = string.rstrip("\n")
  sp_name = sp_name.split("[")[-1]
  sp_name = sp_name.rstrip("]")
  sp_name = sp_name.replace(" ", "_")
  return sp_name


def get_prot_id(string):
	if "protein_id" in string:
		protid = string.split("[protein_id=")[1].split("]")[0]
	else:
		protid = "NA"
	return protid
