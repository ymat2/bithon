import subprocess
import os
from bithon import fs

def codon_alignment(params):

  _in = params['nuc']
  _prank = params['prank_exe']
  file_name = '.'.join(_in.split('.')[:-2])

  fas = fs.fasta2dict(_in)
  fas = as_multiple3(fas)
  fs.write_fasta(fas, file_name+'.m3.fa')

  print("\tSatrt prank alignment.")
  subprocess.run(
    _prank
    +' -d='+file_name+'.m3.fa'
    +' -o='+file_name
    +' -codon -quiet',
    shell=True
  )
  print("\tFinish prank alignment.")

  os.remove(file_name+'.m3.fa')


def as_multiple3(seq_dict):
  m3_dict = dict()
  for id, nuc in seq_dict.items():
    if len(nuc)%3 == 0:
      nuc = nuc
    elif len(nuc)%3 == 1:
      nuc = nuc + 'NN'
    else:
      nuc = nuc + 'N'
    m3_dict[id] = nuc
  return m3_dict
