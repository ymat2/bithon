from Bio import SeqIO
import argparse
import time

def main():
  psr = argparse.ArgumentParser()
  psr.add_argument("--fasta")
  args = psr.parse_args()

  start = time.time()
  seq_dict = fasta2dict_with(args.fasta)
  print(len(seq_dict))
  print('Time elapsed: {:,}'.format(time.time() - start))


def fasta2dict_with(path):
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


# slowest
def fasta2dict_bio(path):
  id2seq = dict()
  desc2seq = dict()
  for record in SeqIO.parse(path, "fasta"):
    _id, _desc, _seq = record.id, record.description, record.seq
    id2seq[_id] = str(_seq)
    desc2seq[_desc] = str(_seq)
  return desc2seq


# fastest
def fasta2dict_kfuku(path):
  with open(path, mode='r') as f:
    txt = f.read()
  seqs = [ t for t in txt.split('>') if not t=='' ]
  seqs = [ s.split('\n', 1) for s in seqs ]
  seqs = [ s.replace('\n','') for seq in seqs for s in seq ]
  seq_dict = dict()
  for i in range(int(len(seqs)/2)):
    seq_dict[seqs[i*2]] = seqs[i*2+1]
  return seq_dict


if __name__ == "__main__":
  main()
