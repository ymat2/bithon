import argparse
import time
import os

def command_gls(args):
  print("bithon::get_longest_seq starts.")
  start = time.time()
  from bithon.get_longest_seq import get_longest_seq
  params = get_params(args)
  get_longest_seq(params)
  print("Time elapsed: {:,} sec.".format(int(time.time() - start)))
  print("bithon::get_longest_seq ends.")


def command_prank(args):
  print("bithon::codon_alignment starts.")
  start = time.time()
  from bithon.codon_alignment import codon_alignment
  params = {
    'nuc': args.infile,
    'prank_exe': args.prank_exe
  }
  codon_alignment(params)
  print("Time elapsed: {:,} sec.".format(int(time.time() - start)))
  print("bithon::codon_alignment ends.")


def get_params(args):
  gtf = args.indir+"/genomic.gtf"
  cds = args.indir+"/cds_from_genomic.fna"
  pep = args.indir+"/protein.faa"

  params = dict()
  params['indir'] = args.indir
  params['outdir'] = args.outdir
  if os.path.exists(gtf):
    params['gtf'] = gtf
  if os.path.exists(cds):
    params['cds'] = cds
  if os.path.exists(pep):
    params['pep'] = pep

  return params


def main():
  parser = argparse.ArgumentParser()
  subparsers = parser.add_subparsers()

  # get_longest_seq
  parser_gls = subparsers.add_parser("gls")
  parser_gls.add_argument("-i", "--indir")
  parser_gls.add_argument("-o", "--outdir")
  parser_gls.set_defaults(handler=command_gls)

  # codon_alignment
  parser_prank = subparsers.add_parser("prank")
  parser_prank.add_argument("-i", "--infile")
  parser_prank.add_argument("--prank_exe", default="prank")
  parser_prank.set_defaults(handler=command_prank)

  args = parser.parse_args()
  if hasattr(args, "handler"):
    args.handler(args)
  else:
    parser.print_help()


if __name__ == "__main__":
  main()
