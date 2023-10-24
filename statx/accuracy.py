#!/usr/bin/env python
'''
Measure AUC of two groups
'''

import argparse
import csv
import logging
import sys

import numpy as np
import sklearn.metrics

def accuracy(colval, colgroup, a, b, ifh):
  if colval is not None:
    a = []
    b = []
    cat1 = None
    for r in csv.DictReader(ifh, delimiter='\t'):
      if cat1 is None:
        cat1 = r[colgroup]
      if r[colgroup] == cat1:
        a.append(float(r[colval]))
      else:
        b.append(float(r[colval]))

  truth = [1] * len(a) + [0] * len(b)
  values = a + b
  auc = sklearn.metrics.roc_auc_score(truth, values)
  return {'auc': auc}

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Measure AUC of two groups')
  parser.add_argument('--group1', required=False, type=float, nargs='+', help='cases')
  parser.add_argument('--group2', required=False, type=float, nargs='+', help='controls')
  parser.add_argument('--colval', required=False, help='')
  parser.add_argument('--colgroup', required=False, help='')
  parser.add_argument('--verbose', action='store_true', help='more logging')
  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

  a = accuracy(args.colval, args.colgroup, args.group1, args.group2, sys.stdin)
  sys.stdout.write('{:.6f}'.format(a['auc']))
