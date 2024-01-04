#!/usr/bin/env python
'''
'''

import argparse
import logging
import math
import sys

import numpy as np
import scipy.stats

def chisquare(vs):
  xa = []
  xb = []
  for v in range(0, len(vs), 2):
    xa.append(vs[v])
    xb.append(vs[v + 1])

  result = scipy.stats.chi2_contingency([xa, xb])
  return {'oddsratio': 'na', 'pvalue': result.pvalue}

def fisher(v):
  oddsratio, pvalue = scipy.stats.fisher_exact([[v[0], v[1]], [v[2], v[3]]])
  result = {'oddsratio': oddsratio, 'pvalue': pvalue}
  
  # with ci
  # Upper 95% CI = e ^ [ln(OR) + 1.96 sqrt(1/a + 1/b + 1/c + 1/d)] 
  # Lower 95% CI = e ^ [ln(OR) - 1.96 sqrt(1/a + 1/b + 1/c + 1/d)] 
  if all([v[x] > 0 for x in (0,1,2,3)]):
    ci_high = math.exp(math.log(oddsratio) + 1.96 * math.sqrt(1/v[0] + 1/v[1] + 1/v[2] + 1/v[3])) 
    ci_low = math.exp(math.log(oddsratio) - 1.96 * math.sqrt(1/v[0] + 1/v[1] + 1/v[2] + 1/v[3])) 
    result['ci_high'] = ci_high
    result['ci_low'] = ci_low
 
  return result

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='chi square')
  parser.add_argument('--values', required=True, type=int, nargs='+', help='2x2 set of values')
  parser.add_argument('--verbose', action='store_true', help='more logging')
  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

  if len(args.values) == 4:
    result = fisher(args.values)
  else:
    # supports yes/no yes/no ...
    result = chisquare(args.values)
  sys.stdout.write('oddsratio\tp-value\n')
  sys.stdout.write('{}\t{}\n'.format(result['oddsratio'], result['pvalue']))
