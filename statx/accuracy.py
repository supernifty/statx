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

def accuracy(colval, colgroup, a, b, ifh, ci=False):
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
  ci_low = ci_high = None
  if ci and auc < 1 and auc > 0:
    # based on https://www.ncss.com/wp-content/themes/ncss/pdf/Procedures/PASS/Confidence_Intervals_for_the_Area_Under_an_ROC_Curve.pdf
    q1 = auc / (2-auc)
    q2 = 2 * auc * auc / (1 + auc)
    se = math.sqrt((auc * (1-auc) + (len(a) - 1) * (q1 - auc*auc) + (len(b) - 1) * (q2 - auc*auc)) / (len(a) * len(b)))
    z = 1.96
    ci_low = max(0, auc - z * se * auc)
    ci_high = min(1, auc + z * se * auc)
  return {'auc': auc, 'ci_low': ci_low, 'ci_high': ci_high}

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
