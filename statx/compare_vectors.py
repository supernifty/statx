#!/usr/bin/env python
'''
  apply test to each row
'''

import argparse
import collections
import csv
import logging
import sys

import numpy as np

def cosine_similarity(v1, v2):
  similarity = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
  return similarity

def main(ifh, ofh, x_cols, y_cols, target_col, delimiter):
  logging.info('reading stdin...')
  idr = csv.DictReader(ifh, delimiter=delimiter)
  odw = csv.DictWriter(ofh, delimiter=delimiter, fieldnames=idr.fieldnames + ['cosine_similarity'])
  odw.writeheader()
  for r in idr:
    v1 = [float(r[x]) for x in x_cols]
    v2 = [float(r[x]) for x in y_cols]
    r['cosine_similarity'] = cosine_similarity(v1, v2)
    odw.writerow(r)
  logging.info('done')

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Calculate cosine similarity of two vectors')
  parser.add_argument('--x_cols', required=True, nargs='+', help='cols of vector 1')
  parser.add_argument('--y_cols', required=True, nargs='+', help='cols of vector 2')
  parser.add_argument('--target_col', required=False, default='cosine_similarity', help='col to add')
  parser.add_argument('--delimiter', default=',', help='csv input delimiter')
  parser.add_argument('--verbose', action='store_true', help='more logging')
  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

  main(sys.stdin, sys.stdout, args.x_cols, args.y_cols, args.target_col, args.delimiter)
