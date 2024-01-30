import argparse
import time
import os

def command_ngls(args):
  print("bithon::ncbi_gls starts.")
  start = time.time()
  from bithon.ncbi_gls import ncbi_gls
  params = get_params(args)
  ncbi_gls(params)
  print("Time elapsed: {:,} sec.".format(int(time.time() - start)))
  print("bithon::ncbi_gls ends.")


def command_egls(args):
  print("bithon::ensembl_gls starts.")
  start = time.time()
  from bithon.ensembl_gls import ensembl_gls
  ensembl_gls(args.infile, args.outfile, args.header)
  print("Time elapsed: {:,} sec.".format(int(time.time() - start)))
  print("bithon::ensembl_gls ends.")


def command_prank(args):
  print("bithon::codon_alignment starts.")
  start = time.time()
  from bithon.codon_alignment import codon_alignment
  params = {
    'nuc': args.infile,
    'out': args.outfile,
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

  # ncbi_gls
  parser_gls = subparsers.add_parser("ngls")
  parser_gls.add_argument("-i", "--indir")
  parser_gls.add_argument("-o", "--outdir")
  parser_gls.set_defaults(handler=command_ngls)

  # ensembl_gls
  parser_egls = subparsers.add_parser("egls")
  parser_egls.add_argument("-i", "--infile")
  parser_egls.add_argument("-o", "--outfile")
  parser_egls.add_argument("--header", choices=["transcript", "id", "symbol"])
  parser_egls.set_defaults(handler=command_egls)

  # codon_alignment
  parser_prank = subparsers.add_parser("prank")
  parser_prank.add_argument("-i", "--infile")
  parser_prank.add_argument("-o", "--outfile")
  parser_prank.add_argument("--prank_exe", default="prank")
  parser_prank.set_defaults(handler=command_prank)

  args = parser.parse_args()
  if hasattr(args, "handler"):
    args.handler(args)
  else:
    parser.print_help()


if __name__ == "__main__":
  main()
