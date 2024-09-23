#!/usr/bin/env python
'''
  basic t test
'''

import argparse
import logging
import sys

import statsmodels.stats.weightstats

# base on https://stats.stackexchange.com/questions/124096/two-samples-z-test-in-python
def proportion(values1, values2):
  logging.info('starting: %i values vs %i...', len(values1), len(values2))

  if len(values1) == 0 or len(values2) == 0:
    logging.fatal('at least one empty group')
    return

  result = statsmodels.stats.weightstats.ztest(values1, values2)

  sys.stdout.write('statistic\tp-value\n')

  if all([values1[0] == x for x in values1 + values2]):
    logging.info('all values equal')
    sys.stdout.write('0\t1\n')
    return

  sys.stdout.write('{}\t{}\n'.format(result[0], result[1]))

  return {'pvalue': result[0], 'statistic': result[1]}

  logging.info('done')

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Perform a 2-sample proportion test')
  parser.add_argument('--values1', required=True, nargs='+', type=float, help='group 1')
  parser.add_argument('--values2', required=True, nargs='+', type=float, help='group 2')
  parser.add_argument('--verbose', action='store_true', help='more logging')
  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

  proportion(args.values1, args.values2)

