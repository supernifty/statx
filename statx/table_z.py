#!/usr/bin/env python
'''
  add z and p-value to a table based on a given mean and sd
'''

import argparse
import collections
import csv
import logging
import sys

import numpy as np

import scipy.stats

def main(ifh, ofh, col, mean, sd, delimiter='\t'):
  logging.info('reading...')
  idr = csv.DictReader(ifh, delimiter=delimiter)
  odw = csv.DictWriter(ofh, delimiter=delimiter, fieldnames=idr.fieldnames + ['z', 'p'])
  odw.writeheader()
  for row in idr:
    z = (float(row[col]) - mean) / sd
    row['p'] = scipy.stats.norm.sf(abs(z)) * 2
    row['z'] = '{:.6f}'.format(z)
    odw.writerow(row)
  logging.info('done')

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='matrix')
  parser.add_argument('--col', required=True, help='col of interest')
  parser.add_argument('--mean', required=True, type=float, help='mean of dist')
  parser.add_argument('--sd', required=True, type=float, help='sd of dist')
  parser.add_argument('--verbose', action='store_true', help='more logging')
  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

  main(sys.stdin, sys.stdout, args.col, args.mean, args.sd)
