#!/usr/bin/env python
'''
  apply test to each row
'''

import argparse
import collections
import csv
import logging
import sys

import statx.t_test

def main(fh, out, key, val, delimiter, one_sided=False, paired=False):
  logging.info('reading stdin...')
  fhr = csv.DictReader(fh, delimiter=delimiter)
  vs = collections.defaultdict(list)
  for i, row in enumerate(fhr):
    # def t_test(num1, num2, one_sided=one_sided, paired=paired, output=None):
    vs[row[key]].append(float(row[val]))

  ls = [vs[x] for x in vs]
  if len(ls) == 2:
    result = statx.t_test.t_test(ls[0], ls[1], one_sided=one_sided, paired=paired)
  else:
    logging.warn('more than 2 groups not implemented')
    return None # anova not implemented

  out.write('Name\tValue\n')
  out.write(''.join(['key_{}\t{}\n'.format(i + 1, x) for i, x in enumerate(vs)]))
  out.write('{}'.format('\n'.join(['{}\t{}'.format(k, result[k]) for k in result])))

  logging.info('done')

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Run t_test on each row')
  parser.add_argument('--key', required=True, help='column for group')
  parser.add_argument('--val', required=True, help='column for value')
  parser.add_argument('--delimiter', default=',', help='csv input delimiter')
  parser.add_argument('--verbose', action='store_true', help='more logging')
  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

  main(sys.stdin, sys.stdout, args.key, args.val, args.delimiter)
