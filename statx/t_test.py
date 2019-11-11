#!/usr/bin/env python
'''
  basic t test
'''

import argparse
import logging
import sys

import scipy.stats

def t_test(values1, values2):
  logging.info('starting: %i values vs %i values', len(values1), len(values2))
  logging.debug('group 1: %s; group 2: %s', ' '.join(values1), ' '.join(values2))

  if len(values1) == 0 or len(values2) == 0:
    logging.fatal('empty groups')
    return

  num1 = [float(x) for x in values1]
  num2 = [float(x) for x in values2]

  sys.stdout.write('t-value\tp-value\n')

  if all([num1[0] == x for x in num1 + num2]):
    logging.info('all values equal')
    sys.stdout.write('0\t1\n')
    return

  result = scipy.stats.ttest_ind(num1, num2)

  sys.stdout.write('{}\t{}\n'.format(result[0], result[1]))

  logging.info('done')

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Assess MSI')
  parser.add_argument('--values1', required=True, nargs='+', help='group 1')
  parser.add_argument('--values2', required=True, nargs='+', help='group 2')
  parser.add_argument('--verbose', action='store_true', help='more logging')
  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

  t_test(args.values1, args.values2)
