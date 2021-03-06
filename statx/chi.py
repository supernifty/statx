#!/usr/bin/env python
'''
'''

import argparse
import logging
import sys

import numpy as np
import scipy.stats

def fisher(v):
  oddsratio, pvalue = scipy.stats.fisher_exact([[v[0], v[1]], [v[2], v[3]]])
  return {'oddsratio': oddsratio, 'pvalue': pvalue}

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Assess MSI')
  parser.add_argument('--values', required=True, type=int, nargs='+', help='2x2 set of values')
  parser.add_argument('--verbose', action='store_true', help='more logging')
  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

  result = fisher(args.values)
  sys.stdout.write('oddsratio\tp-value\n')
  sys.stdout.write('{}\t{}\n'.format(result['oddsratio'], result['pvalue']))
