#!/usr/bin/env python
'''
  distance calculation
'''

import argparse
import csv
import logging
import sys

import numpy as np
import scipy.stats

def cosine_similarity(v1, v2):
  similarity = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
  return similarity

def similarity_matrix(name, cols):
  logging.info('reading from stdin')
  names = {}
  for row in csv.DictReader(sys.stdin, delimiter='\t'):
    if cols is None:
      names[row[name]] = [float(row[x]) for x in sorted(row) if x != name]
    else:
      names[row[name]] = [float(row[x]) for x in sorted(row) if x in cols]

  logging.info('generating distances')
  sys.stdout.write('{}\t{}\n'.format(name, '\t'.join(sorted(names))))
  for x in sorted(names):
    vals = []
    for y in sorted(names):
      similarity = cosine_similarity(names[x], names[y])
      vals.append(similarity)
    sys.stdout.write('{}\t{}\n'.format(x, '\t'.join([str('{:.3f}'.format(x)) for x in vals])))

  logging.info('done')

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Distance of tabular data')
  parser.add_argument('--name', help='column for row name')
  parser.add_argument('--cols', nargs='+', required=False, help='columns to assess')
  parser.add_argument('--verbose', action='store_true', help='more logging')
  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

  similarity_matrix(args.name, args.cols)
