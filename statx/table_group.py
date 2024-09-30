#!/usr/bin/env python
'''
  apply test to columns
'''

import argparse
import collections
import csv
import logging
import math
import sys

import scipy.stats

import statx.anova
import statx.t_test

def t_test(fh, out, group, col, delimiter, one_sided=False, paired=False):
  '''
    group: variable to separate groups on
    col: value
  '''
  logging.info('reading stdin...')
  fhr = csv.DictReader(fh, delimiter=delimiter)
  vals = collections.defaultdict(list)
  for i, row in enumerate(fhr):
    # def t_test(num1, num2, one_sided=one_sided, paired=paired, output=None):
    logging.debug('processing row %i...', i)
    vals[row[group]].append(row[col])

  groups = sorted([x for x in list(vals.keys()) if x != ''])
  if len(groups) == 2:
    logging.info('comparing %s to %s using column %s', groups[0], groups[1], col)
    result = statx.t_test.t_test([float(x) for x in vals[groups[0]] if x != ''], [float(x) for x in vals[groups[1]] if x != ''], one_sided=one_sided, paired=paired, output=out)
  elif len(groups) == 3: 
    logging.info('comparing 3 groups using column %s with anova', col)
    logging.debug('groups are %s', groups)
    result = statx.anova.anova([float(x) for x in vals[groups[0]] if x != ''], [float(x) for x in vals[groups[1]] if x != ''], [float(x) for x in vals[groups[2]] if x != ''], None, None)
  elif len(groups) == 4:
    logging.info('comparing 4 groups using column %s with anova', col)
    result = statx.anova.anova([float(x) for x in vals[groups[0]] if x != ''], [float(x) for x in vals[groups[1]] if x != ''], [float(x) for x in vals[groups[2]] if x != ''], [float(x) for x in vals[groups[3]] if x != ''], None)
  elif len(groups) == 5:
    logging.info('comparing 5 groups using column %s with anova', col)
    result = statx.anova.anova([float(x) for x in vals[groups[0]] if x != ''], [float(x) for x in vals[groups[1]] if x != ''], [float(x) for x in vals[groups[2]] if x != ''], [float(x) for x in vals[groups[3]] if x != ''], [float(x) for x in vals[groups[4]] if x != ''])
  else:
    logging.warning('unsupported group size: %i', len(groups))

  odw = csv.DictWriter(out, delimiter=delimiter, fieldnames=['key', 'value'])
  odw.writeheader()
  for x in sorted(result):
    odw.writerow({'key': x, 'value': result[x]})

  logging.info('done')

def chi(fh, out, group, col, delimiter, ybase=None, keys=None):
  '''
    reads a table and writes chi-square summary
    group: variable to separate groups on
    col: value
  '''
  result = {}
  xy = collections.defaultdict(int) # table of counts
  x = collections.defaultdict(int) 
  y = collections.defaultdict(int) 
  total = 0
  if keys is None:
    logging.info('reading stdin...')
    fhr = csv.DictReader(fh, delimiter=delimiter)
    for i, row in enumerate(fhr):
      # def t_test(num1, num2, one_sided=one_sided, paired=paired, output=None):
      #logging.debug('processing row %i...', i)
      if row[group] == '' or row[col] == '':
        continue
      key = (row[group], row[col])
      xy[key] += 1
      x[row[group]] += 1
      y[row[col]] += 1
      total += 1
  else:
    group = 0
    col = 1
    logging.info('%i keys...', len(keys))
    for i, row in enumerate(keys):
      if row[group] == '' or row[col] == '':
        continue
      key = (row[group], row[col])
      xy[key] += 1
      x[row[group]] += 1
      y[row[col]] += 1
      total += 1
 
  # observed counts
  out.write('OBSERVED\n')
  ofh = csv.DictWriter(out, delimiter='\t', fieldnames=[col] + sorted(x.keys()) + ['Total'])
  ofh.writeheader()
  for yn in sorted(y.keys()):
    row = {col: yn, 'Total': y[yn]}
    for xn in x.keys():
      row[xn] = '{} ({:.6f})'.format(xy[(xn, yn)], xy[(xn, yn)] / x[xn])
      result['observed_{}_{}'.format(xn, yn)] = xy[(xn, yn)]
      result['observed-pct_{}_{}'.format(xn, yn)] = xy[(xn, yn)] / x[xn]
      result['observed-pct-y_{}_{}'.format(xn, yn)] = xy[(xn, yn)] / y[yn]
    ofh.writerow(row)

  # observed totals
  row = {col: 'Total'}
  row.update(x)
  ofh.writerow(row)

  out.write('\nEXPECTED\n')
  ofh = csv.DictWriter(out, delimiter='\t', fieldnames=[col] + sorted(x.keys()))
  ofh.writeheader()
  for yn in sorted(y.keys()):
    row = {col: yn}
    for xn in x.keys():
      row[xn] = x[xn] * y[yn] / total
    ofh.writerow(row)

  # significance
  out.write('\nSIGNIFICANCE\n')
  if total > 0:
    f_obs = []
    for yn in sorted(y.keys()):
      f_obs.append([xy[(xn, yn)] for xn in sorted(x.keys())])
    f_exp = []
    for yn in sorted(y.keys()):
      f_exp.append([x[xn] * y[yn] / total for xn in sorted(x.keys())])
    out.write('f_obs = {}\n'.format(f_obs))
    out.write('f_exp = {}\n'.format(f_exp))
    chisquare_result = scipy.stats.chisquare(f_obs, f_exp, axis=1, ddof=0)
    # overall 
    out.write('chisq\tp_value\n')
    #chisquare = sum(result[0])
    #p_value = scipy.stats.chisquare(f_obs=chisquare, ddof=0)[1]]
    #out.write('{}\t{}\n'.format(chisquare, result[1]))
    out.write('{}\t{}\n'.format(chisquare_result[0], chisquare_result[1]))
    #out.write('yn is {}'.format(y.keys()))
    for v, pv in zip(sorted(y.keys()), chisquare_result[1]):
      result['{}_pvalue'.format(v)] = pv
    chisquare = sum(chisquare_result[0])
    pvalue = 1 - scipy.stats.chi2.cdf(chisquare, (len(x.keys()) - 1) * (len(y.keys()) - 1))
    out.write('{}\t{}\n'.format(chisquare, pvalue))
    result['pvalue'] = pvalue

    # odds ratio for each x
  xs = list(sorted(x.keys()))
  if len(xs) == 2:
    out.write('\nODDS RATIOS\n')
    out.write('category\todds ratio\tCI\n')

    for yn in sorted(y.keys()): # each key
      positives = xy[(xs[1], yn)] 
      negatives = xy[(xs[0], yn)]
      if ybase is None:
        base_positives = sum([xy[(xs[1], ys)] for ys in y.keys() if ys != yn])
        base_negatives = sum([xy[(xs[0], ys)] for ys in y.keys() if ys != yn])
      else:
        base_positives = xy[(xs[1], ybase)]
        base_negatives = xy[(xs[0], ybase)]
      logging.debug('with yn=%s bp=%i bn=%i', yn, base_positives, base_negatives)
      # or is (p / n) / (op / on)

      logging.debug('%s: pos %i neg %i vs %s: pos %i neg %i', yn, positives, negatives, ybase, base_positives, base_negatives)
      
      smoothing = False
      if any([x == 0 for x in (negatives, base_positives, base_negatives, positives)]):
        negatives += 1
        base_positives += 1
        base_negatives += 1
        positives += 1
        smoothing = True
        logging.info('smoothing applied to yn')
      result['smoothing'] = smoothing

      odds = positives * base_negatives / negatives / base_positives
      ci_high = math.exp(math.log(odds) + 1.96 * math.sqrt(1/positives + 1/negatives + 1/base_positives + 1/base_negatives))
      ci_low = math.exp(math.log(odds) - 1.96 * math.sqrt(1/positives + 1/negatives + 1/base_positives + 1/base_negatives))
      out.write('{}\t{:.3f}\t{:.3f}-{:.3f}{}\n'.format(yn, odds, ci_low, ci_high, ' smoothed' if smoothing else ''))
      result['oddsratio-point_{}'.format(yn)] = odds
      result['oddsratio-low_{}'.format(yn)] = ci_low
      result['oddsratio-high_{}'.format(yn)] = ci_high
      # convert to p-value
      oddsratio, pvalue = scipy.stats.fisher_exact([[positives, base_positives], [negatives, base_negatives]])
      result['oddsratio-fisher-point_{}'.format(yn)] = oddsratio
      result['oddsratio-fisher-pvalue_{}'.format(yn)] = pvalue
      
  # return results
  return result
    

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Run t_test on each row')
  parser.add_argument('--test', required=True, help='t_test')
  parser.add_argument('--col', required=True, help='independent variables')
  parser.add_argument('--group', required=True, help='dependent variable') # for odds ratio
  parser.add_argument('--base', required=False, help='base value for odds ratios') # for odds ratio
  parser.add_argument('--delimiter', default=',', help='csv input delimiter')
  parser.add_argument('--verbose', action='store_true', help='more logging')
  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

  if args.test == 't_test':
    t_test(sys.stdin, sys.stdout, args.group, args.col, args.delimiter)
  elif args.test == 'chi':
    chi(sys.stdin, sys.stdout, args.group, args.col, args.delimiter, args.base)
  else:
    logging.fatal('unrecognized test')
