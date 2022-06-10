#!/usr/bin/env python
'''
  apply test to each row
'''

import argparse
import csv
import logging
import sys

import statx.t_test

def t_test(fh, out, cols1, cols2, delimiter, one_sided=False, paired=False):
  logging.info('reading stdin...')
  fhr = csv.DictReader(fh, delimiter=delimiter)
  fhout = csv.DictWriter(out, delimiter=delimiter, fieldnames=fhr.fieldnames + ['p-value', 't-value', 'v1u', 'v1sd', 'v2u', 'v2sd'])
  fhout.writeheader()
  for i, row in enumerate(fhr):
    # def t_test(num1, num2, one_sided=one_sided, paired=paired, output=None):
    logging.debug('processing row %i...', i)
    result = statx.t_test.t_test([float(row[x]) for x in cols1], [float(row[x]) for x in cols2], one_sided=one_sided, paired=paired)
    row.update(result)
    logging.debug('row is %s', row)
    fhout.writerow(row)

  logging.info('done')

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Run t_test on each row')
  parser.add_argument('--cols1', required=True, nargs='+', help='colnames')
  parser.add_argument('--cols2', required=True, nargs='+', help='colnames')
  parser.add_argument('--delimiter', default=',', help='csv input delimiter')
  parser.add_argument('--verbose', action='store_true', help='more logging')
  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

  t_test(sys.stdin, sys.stdout, args.cols1, args.cols2, args.delimiter)
