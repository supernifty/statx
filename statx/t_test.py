#!/usr/bin/env python
'''
  basic t test
  2 sided
  divide by 2 for one sided
'''

import argparse
import logging
import sys

import numpy as np
import scipy.stats

def t_test(values1, values2, one_sided, paired):
  logging.info('starting: %i values vs %i values', len(values1), len(values2))
  logging.debug('group 1: %s; group 2: %s', ' '.join(values1), ' '.join(values2))

  if len(values1) == 0 or len(values2) == 0:
    logging.fatal('empty groups')
    return

  if paired and len(values1) != len(values2):
    logging.fatal('paired groups must have same length')
    return

  num1 = [float(x) for x in values1]
  num2 = [float(x) for x in values2]

  sys.stdout.write('t-value\tp-value\tv1u\tv1sd\tv1min\tv1max\tv1n\tv2u\tv2sd\tv2min\tv2max\tv2n\n')

  if all([num1[0] == x for x in num1 + num2]):
    logging.info('all values equal')
    sys.stdout.write('0\t1\t{}\t0\t{}\t{}\t{}\t{}\t0\t{}\t{}\t{}\n'.format(num1[0], num1[0], num1[0], len(num1), num1[0], num1[0], num1[0], len(num2)))
    return

  if paired:
    logging.debug('paired test')
    result = scipy.stats.ttest_rel(num1, num2)
  else:
    logging.debug('independent test')
    result = scipy.stats.ttest_ind(num1, num2)

  if one_sided:
    sys.stdout.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(result[0], result[1] / 2, np.mean(num1), np.std(num1, ddof=1), min(num1), max(num1), len(num1), np.mean(num2), np.std(num2, ddof=1), min(num2), max(num2), len(num2)))
  else:
    sys.stdout.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(result[0], result[1], np.mean(num1), np.std(num1, ddof=1), min(num1), max(num1), len(num1), np.mean(num2), np.std(num2, ddof=1), min(num2), max(num2), len(num2)))

  logging.info('done')

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Perform a t-test')
  parser.add_argument('--values1', required=True, nargs='+', help='group 1')
  parser.add_argument('--values2', required=True, nargs='+', help='group 2')
  parser.add_argument('--one_sided', action='store_true', help='one sided result')
  parser.add_argument('--paired', action='store_true', help='one sided test')
  parser.add_argument('--verbose', action='store_true', help='more logging')
  parser.add_argument('--quiet', action='store_true', help='less logging')
  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  elif args.quiet:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.WARN)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

  t_test(args.values1, args.values2, args.one_sided, args.paired)
