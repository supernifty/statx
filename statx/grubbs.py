#!/usr/bin/env python
'''
  grubbs outlier test
'''

import argparse
import logging
import sys

import numpy as np
import scipy.stats

def grubbs(value, values):
  logging.info('starting: %i values', len(values))

  if len(values) <= 1:
    logging.fatal('not enough values')
    return

  nums = [float(x) for x in values]

  sys.stdout.write('sd\tp-value\n')

  if all([nums[0] == x for x in nums]):
    logging.info('all values equal')
    sys.stdout.write('0\t1\n')
    return

  num = float(value)
  z = (num - np.mean(nums)) / np.std(nums)
  p = scipy.stats.norm.sf(abs(z))*2
  

  sys.stdout.write('{}\t{}\n'.format(z, p))

  logging.info('done')

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Grubbs test')
  parser.add_argument('--value', required=True, type=float, help='outlier')
  parser.add_argument('--values', required=True, nargs='+', help='distribution')
  parser.add_argument('--verbose', action='store_true', help='more logging')
  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

  grubbs(args.value, args.values)
