import argparse
import time


def protid2geneid(path):
	p2g = {}
	with open(path) as f:
		ln = [ line.rstrip().split("\t")[-1] for line in f ]
	for l in ln:
		attribute = l.split("; ")
		att = {dsc.split(" ")[0]: dsc.split(" ")[-1].strip("\"") for dsc in attribute}
		gene_id = att.get("gene", "NA")
		prot_id = att.get("protein_id", "NA")
		if prot_id not in p2g:
			p2g[prot_id] = gene_id
	return p2g
