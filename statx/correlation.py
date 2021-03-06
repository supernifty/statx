#!/usr/bin/env python
'''
  pearson correlation
'''

import argparse
import logging
import sys

import numpy as np
import scipy.stats

def correlation(values1, values2):
  logging.info('starting: %i values vs %i values', len(values1), len(values2))
  logging.debug('group 1: %s; group 2: %s', ' '.join(values1), ' '.join(values2))

  if len(values1) == 0 or len(values2) == 0:
    logging.fatal('empty groups')
    return

  num1 = [float(x) for x in values1]
  num2 = [float(x) for x in values2]

  sys.stdout.write('pearson\tp-value\tv1u\tv1sd\tv1min\tv1max\tv1n\tv2u\tv2sd\tv2min\tv2max\tv2n\n')

  if all([num1[0] == x for x in num1 + num2]):
    logging.info('all values equal')
    sys.stdout.write('0\t1\t{}\t0\t{}\t{}\t{}\t{}\t0\t{}\t{}\t{}\n'.format(num1[0], num1[0], num1[0], len(num1), num1[0], num1[0], num1[0], len(num2)))
    return

  result = scipy.stats.pearsonr(num1, num2)

  sys.stdout.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(result[0], result[1], np.mean(num1), np.std(num1), min(num1), max(num1), len(num1), np.mean(num2), np.std(num2), min(num2), max(num2), len(num2)))

  logging.info('done')

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Measure correlation')
  parser.add_argument('--values1', required=True, nargs='+', help='group 1')
  parser.add_argument('--values2', required=True, nargs='+', help='group 2')
  parser.add_argument('--verbose', action='store_true', help='more logging')
  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

  correlation(args.values1, args.values2)
