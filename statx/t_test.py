#!/usr/bin/env python
'''
  given tumour and normal vcf pairs, explore msi status
'''

import argparse
import logging
import sys

import scipy.stats

def main(values1, values2):
  logging.info('starting: %i values vs %i values', len(values1), len(values2))
  logging.debug('group 1: %s; group 2: %s', ' '.join(values1), ' '.join(values2))

  result = scipy.stats.ttest_ind([float(x) for x in values1], [float(x) for x in values2])

  sys.stdout.write('t-value: {}\np-value: {}\n'.format(result[0], result[1]))

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

  main(args.values1, args.values2)
