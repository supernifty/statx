#!/usr/bin/env python
'''
  correlation matrix of provided cols
'''

import argparse
import collections
import csv
import logging
import sys

import numpy as np

import scipy.stats

def main(ifh, ofh, cols, delimiter='\t'):
  logging.info('reading...')
  data = collections.defaultdict(list)
  # want sig: [vals]
  count = 0
  for row in csv.DictReader(ifh, delimiter=delimiter):
    for c in cols:
      try:
        data[c].append(float(row[c]))
      except:
        logging.warning('column %s contains non-numeric value: %s, row: %s', c, row[c], row)
        raise
    count += 1

  logging.info('calculating from %i...', count)
  correlations = []

  odw = csv.DictWriter(ofh, delimiter='\t', fieldnames=['x', 'y', 'correlation', 'pvalue'])
  odw.writeheader()
  for x in cols:
    for y in cols:
      if x == y:
        continue
      result = scipy.stats.pearsonr(data[x], data[y])
      odw.writerow({'x': x, 'y': y, 'correlation': '{:.3f}'.format(result[0]), 'pvalue': result[1]})
      correlations.append(result[0])

  logging.info('correlation mean: %.6f sd: %.6f', np.mean(correlations), np.std(correlations, ddof=1))
  logging.info('done')

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='matrix')
  parser.add_argument('--cols', required=True, nargs='+', help='tumour vcf')
  parser.add_argument('--verbose', action='store_true', help='more logging')
  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

  main(sys.stdin, sys.stdout, args.cols)
