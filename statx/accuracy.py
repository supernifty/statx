#!/usr/bin/env python
'''
Measure AUC of two groups
'''

import argparse
import logging
import sys

import numpy as np
import sklearn.metrics

def accuracy(a, b):
  truth = [1] * len(a) + [0] * len(b)
  values = a + b
  auc = sklearn.metrics.roc_auc_score(truth, values)
  return {'auc': auc}

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Measure AUC of two groups')
  parser.add_argument('--group1', required=True, type=float, nargs='+', help='cases')
  parser.add_argument('--group2', required=True, type=float, nargs='+', help='controls')
  parser.add_argument('--verbose', action='store_true', help='more logging')
  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

  a = accuracy(args.group1, args.group2)
  sys.stdout.write('auc\t{}\n'.format(a))
