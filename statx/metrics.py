#!/usr/bin/env python
'''
Measure confidence intervals
'''

import argparse
import logging
import math
import sys

import numpy as np
import scipy
import scipy.stats


def ci(x, n, alpha=0.05):
  ci_low = scipy.stats.beta.ppf(alpha/2, x, n - x + 1)
  ci_upp = scipy.stats.beta.isf(alpha/2, x + 1, n - x)
  return {'lower': 0 if math.isnan(ci_low) else ci_low, 'upper': 1 if math.isnan(ci_upp) else ci_upp}

  #if np.ndim(ci_low) > 0:
  #  ci_low[q_ == 0] = 0
  #  ci_upp[q_ == 1] = 1
  #else:
  #  ci_low = ci_low if (q_ != 0) else 0
  #  ci_upp = ci_upp if (q_ != 1) else 1

def metrics(tp, tn, fp, fn):
  accuracy = (tp + tn) / (tp + tn + fp + fn)
  accuracy_ci = ci(tp + tn, tp + fn + tn + fp)
  sensitivity = tp / (tp + fn)
  sensitivity_ci = ci(tp, tp + fn)
  specificity = tn / (tn + fp)
  specificity_ci = ci(tn, tn + fp)
  # confidence intervals
  return {'accuracy_pe': accuracy, 'accuracy_lower': accuracy_ci['lower'], 'accuracy_upper': accuracy_ci['upper'], 'sensitivity_pe': sensitivity, 'sensitivity_lower': sensitivity_ci['lower'], 'sensitivity_upper': sensitivity_ci['upper'], 'specificity_pe': specificity, 'specificity_lower': specificity_ci['lower'], 'specificity_upper': specificity_ci['upper']}

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Measure AUC of two groups')
  parser.add_argument('--tp', required=True, type=int, help='true positives')
  parser.add_argument('--tn', required=True, type=int, help='true negative')
  parser.add_argument('--fp', required=True, type=int, help='false positives')
  parser.add_argument('--fn', required=True, type=int, help='false negatives')
  parser.add_argument('--verbose', action='store_true', help='more logging')
  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

  a = metrics(args.tp, args.tn, args.fp, args.fn)
  sys.stdout.write('Metric\tPoint\tLowerCI\tUpperCI\n')
  sys.stdout.write('accuracy\t{:.3f}\t{:.3f}\t{:.3f}\n'.format(a['accuracy_pe'] * 100, a['accuracy_lower'] * 100, a['accuracy_upper'] * 100))
  sys.stdout.write('sensitivity\t{:.3f}\t{:.3f}\t{:.3f}\n'.format(a['sensitivity_pe'] * 100, a['sensitivity_lower'] * 100, a['sensitivity_upper'] * 100))
  sys.stdout.write('specificity\t{:.3f}\t{:.3f}\t{:.3f}\n'.format(a['specificity_pe'] * 100, a['specificity_lower'] * 100, a['specificity_upper'] * 100))
