#!/usr/bin/env python
'''
  grubbs outlier test
  2 sided
  divide by two for 1 sided
'''

import argparse
import logging
import sys

import numpy as np
import scipy.stats

def grubbs(value, values, one_sided):
  logging.info('starting: %i values', len(values))

  if len(values) <= 1:
    logging.fatal('not enough values')
    return

  nums = [float(x) for x in values]

  sys.stdout.write('z\tp-value\tv\tvu\tsd\tvmin\tvmax\tn\n')

  if all([nums[0] == x for x in nums]):
    logging.info('all values equal')
    sys.stdout.write('0\t1\t{}\t{}\t{}\t{}\t{}\n', value, num[0], 0, num[0], num[0], len(nums))
    return

  num = float(value)
  z = (num - np.mean(nums)) / np.std(nums, ddof=1)
  p = scipy.stats.norm.sf(abs(z)) * 2

  if one_sided:
    p /= 2

  sys.stdout.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(z, p, value, np.mean(nums), np.std(nums, ddof=1), min(nums), max(nums), len(nums)))

  logging.info('done')

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Grubbs test')
  parser.add_argument('--value', required=True, type=float, help='outlier')
  parser.add_argument('--values', required=True, nargs='+', help='distribution')
  parser.add_argument('--one_sided', action='store_true', help='one sided test')
  parser.add_argument('--verbose', action='store_true', help='more logging')
  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

  grubbs(args.value, args.values, args.one_sided)
