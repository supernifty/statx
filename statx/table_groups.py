#!/usr/bin/env python
'''
  apply test to each row
'''

import argparse
import collections
import csv
import logging
import sys

import statx.anova
import statx.t_test

def t_test(fh, out, group, cols, delimiter, one_sided=False, paired=False):
  logging.info('reading stdin...')
  fhr = csv.DictReader(fh, delimiter=delimiter)
  data = {}
  for c in cols:
    data[c] = collections.defaultdict(list)

  groups = set()
  for i, r in enumerate(fhr):
    for c in cols:
      data[c][r[group]].append(float(r[c]))
      groups.add(r[group])

  if len(groups) < 2 or len(groups) > 5:
    logging.fatal('only t-tests and anova for now but there are %i groups', len(groups))
    sys.exit(1)
    
  fhout = csv.DictWriter(out, delimiter=delimiter, fieldnames=['col', 'p-value', 't-value', 'v1n', 'v1u', 'v1median', 'v1sd', 'v2n', 'v2u', 'v2median', 'v2sd', 'v1max', 'v2min', 'v1min', 'v2max'])
  fhout.writeheader()
  g = sorted(list(groups))
  for c in cols:
    logging.debug('processing %s...', c)
    if len(groups) == 2:
      result = statx.t_test.t_test(data[c][g[0]], data[c][g[1]], one_sided=one_sided, paired=paired)
    else: # at least 3
      raw = statx.anova.anova(data[c][g[0]], data[c][g[1]], data[c][g[2]], None if len(groups) < 4 else data[c][g[3]], None if len(groups) < 5 else data[c][g[4]]) 
      result = {'t-value': raw['statistic'], 'p-value': raw['pvalue']}
    result['col'] = c
    fhout.writerow(result)

  logging.info('done')

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Run t_test on each row')
  parser.add_argument('--group', required=True, help='col to choose groups')
  parser.add_argument('--cols', required=True, nargs='+', help='cols to test')
  #parser.add_argument('--test', required=False, default='ttest', help='ttest or chi2')
  parser.add_argument('--delimiter', default=',', help='csv input delimiter')
  parser.add_argument('--verbose', action='store_true', help='more logging')
  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

  #if args.test == 'ttest':
  t_test(sys.stdin, sys.stdout, args.group, args.cols, args.delimiter)
