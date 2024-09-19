#!/usr/bin/env python
'''
calculate p-value and confidence interval for binomial
'''

import argparse
import logging
import math
import sys

import scipy.stats
from scipy.stats import binom
import statsmodels.stats.proportion

def binomial(k, n, p, probability_above, alternative):
  logging.debug('alternative: %s', alternative)
  result = scipy.stats.binomtest(k, n, p=p, alternative=alternative)
  ci_low, ci_high = statsmodels.stats.proportion.proportion_confint(count=k, nobs=n, alpha=0.05, method='normal')
  result = {'pvalue': result.pvalue, 'ci_high': ci_high, 'ci_low': ci_low}
  if probability_above is not None:
    # assuming the observed distribution is representative of the population in this context
    result['probability_above'] = 1 - scipy.stats.binom.cdf(probability_above * n, n, k/n)
  return result

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='binomial test')
  parser.add_argument('--k', required=True, type=int, help='successes')
  parser.add_argument('--n', required=True, type=int, help='trials')
  parser.add_argument('--p', required=True, type=float, help='probability of success')
  parser.add_argument('--probability_above', required=False, type=float, help='probability of proportion being greater than this')
  parser.add_argument('--alternative', required=False, default='two-sided', help='two-sided greater less')
  parser.add_argument('--verbose', action='store_true', help='more logging')
  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

  result = binomial(args.k, args.n, args.p, args.probability_above, args.alternative)

  sys.stdout.write('key\tvalue\n')
  for k in result:
    sys.stdout.write('{}\t{}\n'.format(k, result[k]))
