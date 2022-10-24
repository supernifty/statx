#!/usr/bin/env python
'''
  apply test to each row
'''

import argparse
import collections
import csv
import logging
import sys

import statsmodels.stats.multitest

def main(fh, out, pvalue, target, adjust, delimiter, threshold=0.05):
  logging.info('reading stdin...')
  rows = []
  pvalues = []
  pvalues_sig = 0
  idr = csv.DictReader(fh, delimiter=delimiter)
  for r in idr:
    rows.append(r)
    pvalues.append(float(r[pvalue]))
    if pvalues[-1] < threshold:
      pvalues_sig += 1

  # apply adjustment
  logging.info('%i pvalues %i significant', len(pvalues), pvalues_sig)
  adjusted = statsmodels.stats.multitest.fdrcorrection(pvalues)

  # write with new column
  ofh = csv.DictWriter(out, delimiter=delimiter, fieldnames=idr.fieldnames + [adjust])
  ofh.writeheader()
  adjusted_sig = 0
  for adj, row in zip(adjusted[1], rows):
    row[adjust] = adj
    ofh.writerow(row)
    if adj < threshold:
      adjusted_sig += 1

  logging.info('done. %i adjusted pvalues significant', adjusted_sig)

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Apply multiple testing correction')
  parser.add_argument('--pvalue', required=True, help='column for pvalue')
  parser.add_argument('--target', required=True, help='column for corrected value')
  parser.add_argument('--adjust', default='bh', help='adjustment to apply')
  parser.add_argument('--delimiter', default=',', help='csv input delimiter')
  parser.add_argument('--verbose', action='store_true', help='more logging')
  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

  main(sys.stdin, sys.stdout, args.pvalue, args.target, args.adjust, args.delimiter)
