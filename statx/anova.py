#!/usr/bin/env python
'''
  basic t test
'''

import argparse
import logging
import sys

import scipy.stats

import statx.t_test

def anova(num1, num2, num3=None, num4=None, num5=None, num6=None, num7=None, out_fh=None):
  logging.debug('starting: %i num vs %i...', len(num1), len(num2))

  if len(num1) == 0 or len(num2) == 0:
    logging.warn('at least one empty group')
    return {'pvalue': 1, 'statistic': 0}

  result = {}
  result['t_test_num1_num2'] = statx.t_test.t_test(num1, num2)['p-value']

  if num3 is None:
    anova_result = scipy.stats.f_oneway(num1, num2)
  else:
    result['t_test_num1_num3'] = statx.t_test.t_test(num1, num3)['p-value']
    result['t_test_num2_num3'] = statx.t_test.t_test(num2, num3)['p-value']
    if num4 is None:
      anova_result = scipy.stats.f_oneway(num1, num2, num3)
    else: 
      result['t_test_num1_num4'] = statx.t_test.t_test(num1, num4)['p-value']
      result['t_test_num2_num4'] = statx.t_test.t_test(num2, num4)['p-value']
      result['t_test_num3_num4'] = statx.t_test.t_test(num3, num4)['p-value']
      if num5 is None:
        anova_result = scipy.stats.f_oneway(num1, num2, num3, num4)
      else:
        result['t_test_num1_num5'] = statx.t_test.t_test(num1, num5)['p-value']
        result['t_test_num2_num5'] = statx.t_test.t_test(num2, num5)['p-value']
        result['t_test_num3_num5'] = statx.t_test.t_test(num3, num5)['p-value']
        result['t_test_num4_num5'] = statx.t_test.t_test(num4, num5)['p-value']
        if num6 is None:
          anova_result = scipy.stats.f_oneway(num1, num2, num3, num4, num5)
        else:
          result['t_test_num1_num6'] = statx.t_test.t_test(num1, num6)['p-value']
          result['t_test_num2_num6'] = statx.t_test.t_test(num2, num6)['p-value']
          result['t_test_num3_num6'] = statx.t_test.t_test(num3, num6)['p-value']
          result['t_test_num4_num6'] = statx.t_test.t_test(num4, num6)['p-value']
          result['t_test_num5_num6'] = statx.t_test.t_test(num5, num6)['p-value']
          if num7 is None:
            anova_result = scipy.stats.f_oneway(num1, num2, num3, num4, num5, num6)
          else:
            result['t_test_num1_num7'] = statx.t_test.t_test(num1, num7)['p-value']
            result['t_test_num2_num7'] = statx.t_test.t_test(num2, num7)['p-value']
            result['t_test_num3_num7'] = statx.t_test.t_test(num3, num7)['p-value']
            result['t_test_num4_num7'] = statx.t_test.t_test(num4, num7)['p-value']
            result['t_test_num5_num7'] = statx.t_test.t_test(num5, num7)['p-value']
            result['t_test_num6_num7'] = statx.t_test.t_test(num6, num7)['p-value']
            anova_result = scipy.stats.f_oneway(num1, num2, num3, num4, num5, num6, num7)

  if out_fh is not None:
    out_fh.write('statistic\tp-value\n')

  #if all([num1[0] == x for x in num1 + num2]):
  #  logging.info('all values equal')
  #  if out_fh is not None:
  #    out_fh.write('0\t1\n')
  #  return {'pvalue': 1, 'statistic': 0}

  result['statistic'] = anova_result.statistic
  result['pvalue'] = anova_result.pvalue

  if out_fh is not None:
    out_fh.write('{}\t{}\n'.format(result['statistic'], result['pvalue']))

  logging.debug('done')
  return result

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Perform an ANOVA test')
  parser.add_argument('--values1', required=True, nargs='+', type=float, help='group 1')
  parser.add_argument('--values2', required=True, nargs='+', type=float, help='group 2')
  parser.add_argument('--values3', required=False, nargs='+', type=float, help='group 3')
  parser.add_argument('--values4', required=False, nargs='+', type=float, help='group 4')
  parser.add_argument('--values5', required=False, nargs='+', type=float, help='group 5')
  parser.add_argument('--values6', required=False, nargs='+', type=float, help='group 6')
  parser.add_argument('--values7', required=False, nargs='+', type=float, help='group 7')
  parser.add_argument('--verbose', action='store_true', help='more logging')
  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

  anova(args.values1, args.values2, args.values3, args.values4, args.values5, args.values6, args.values7, out_fh=sys.stdout)

