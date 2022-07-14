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

def t_test(num1, num2, one_sided=False, paired=False, output=None):
  logging.info('starting: %i values vs %i values', len(num1), len(num2))
  logging.debug('group 1: %s; group 2: %s', ' '.join([str(x) for x in num1]), ' '.join([str(x) for x in num2]))

  if len(num1) == 0 or len(num2) == 0:
    logging.warn('empty groups')
    return {'p-value': 1, 't-value': 0, 'v1n': len(num1), 'v2n': len(num2)}

  if paired and len(num1) != len(num2):
    logging.fatal('paired groups must have same length')
    return

  if output is not None:
    output.write('t-value\tp-value\tv1u\tv1median\tv1sd\tv1min\tv1max\tv1n\tv2u\tv2median\tv2sd\tv2min\tv2max\tv2n\n')

  if all([num1[0] == x for x in num1 + num2]):
    logging.info('all values equal')
    if output is not None:
      output.write('0\t1\t{}\t{}\t0\t{}\t{}\t{}\t{}\t{}\t0\t{}\t{}\t{}\n'.format(num1[0], num1[0], num1[0], num1[0], len(num1), num1[0], num1[0], num1[0], num1[0], len(num2)))
    return (0, 1)

  if paired:
    logging.debug('paired test')
    result = scipy.stats.ttest_rel(num1, num2)
  else:
    logging.debug('independent test')
    result = scipy.stats.ttest_ind(num1, num2)

  if output is not None:
    if one_sided:
      output.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(result[0], result[1] / 2, np.mean(num1), np.median(num1), np.std(num1, ddof=1), min(num1), max(num1), len(num1), np.mean(num2), np.median(num2), np.std(num2, ddof=1), min(num2), max(num2), len(num2)))
    else:
      output.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(result[0], result[1], np.mean(num1), np.median(num1), np.std(num1, ddof=1), min(num1), max(num1), len(num1), np.mean(num2), np.median(num2), np.std(num2, ddof=1), min(num2), max(num2), len(num2)))

  logging.info('done')
  return {'p-value': result[1], 't-value': result[0], 'v1u': np.mean(num1), 'v1median': np.median(num1), 'v1sd': np.std(num1, ddof=1), 'v2u': np.mean(num2), 'v2median': np.median(num2), 'v2sd': np.std(num2, ddof=1), 'v1n': len(num1), 'v2n': len(num2)}

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Perform a t-test')
  parser.add_argument('--values1', required=True, nargs='+', type=float, help='group 1')
  parser.add_argument('--values2', required=True, nargs='+', type=float, help='group 2')
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

  t_test(args.values1, args.values2, args.one_sided, args.paired, sys.stdout)
