#!/usr/bin/env python
'''
  apply test to columns
'''

import argparse
import collections
import csv
import logging
import math
import scipy.stats
import sys

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

NEG = {'No', 'Absent', 'Negative', '0', 'Male'}
POS = {'Yes', 'Present', 'Positive', '1', 'Female'}
POS_NEG = POS.union(NEG)

def plot(target, xs, zs, dpi, title, figwidth, figheight, cutoff=None):
    logging.info('generating %s with figure size (%i, %i)', target, figwidth, figheight)
    fig = plt.figure(figsize=(figwidth, figheight), dpi=dpi)
    ax = fig.add_subplot(111)
    #fig, ax = plt.subplots()

    # Show all ticks and label them with the respective list entries
    ax.set_xticks(np.arange(len(xs)))
    ax.set_yticks(np.arange(len(xs)))

    im = ax.imshow(zs)
    for i in range(len(xs)):
      for j in range(len(xs)):
        if cutoff is not None and zs[i][j] < cutoff:
          text = ax.text(j, i, '{:.2f}'.format(zs[i][j]), ha="center", va="center", color="red")
        else:
          text = ax.text(j, i, '{:.2f}'.format(zs[i][j]), ha="center", va="center", color="w")

    #ax.set_xticks(np.arange(len(xs)))
    #ax.set_yticks(np.arange(len(xs)))

    ax.set_xticklabels(xs, rotation=90)
    ax.set_yticklabels(xs)

    ax.set_ylim(len(xs)-0.5, -0.5)

    ax.set_title(title)
    fig.tight_layout()
    plt.savefig(target, dpi=dpi)


def correlation(fh, out, cols, delimiter, plot_pvalue, plot_or, dpi=300, figheight=12, figwidth=10, empty=('N/A', ''), equal_categories=False):
  logging.info('reading stdin...')
  fhr = csv.DictReader(fh, delimiter=delimiter)
  if cols is None:
    cols = fhr.fieldnames
  # pull in the data
  data = collections.defaultdict(list)
  for i, row in enumerate(fhr):
    for col in row:
      if col in cols:
        data[col].append(row[col])

  logging.debug('%i cols included', len(data))
  # process
  xs = []
  cs = []
  ds = []
  ts = []
  ors = []
  bs = []
  zs = []
  for x in sorted(data.keys()):
    logging.info('%s...', x)
    xs.append(x)
    current = []
    current_cs = []
    current_ts = []
    current_or = [] # details
    current_bs = [] # details
    current_ds = [] # details
    for y in sorted(data.keys()): # y is colname
      logging.debug('%s vs %s...', x, y)
      # assume chi-square
      observed = collections.defaultdict(int)
      expected_x = collections.defaultdict(int)
      expected_y = collections.defaultdict(int)
      for idx, _ in enumerate(data[x]): # values from x column
        if data[x][idx] in empty or data[y][idx] in empty:
          continue
        key = (data[x][idx], data[y][idx])
        observed[key] += 1
        expected_x[data[x][idx]] += 1
        expected_y[data[y][idx]] += 1
  
      total_observed = sum([observed[key] for key in observed])
      current_cs.append(total_observed)
      current_ts.append('Chi-square')
      if total_observed > 0:
        dof = (len(expected_x) - 1) * (len(expected_y) - 1) # correct dof
        ddof = len(observed) - 1 - dof
        if equal_categories:
          pvalue = scipy.stats.chisquare(f_obs=[observed[key] for key in sorted(observed.keys())], ddof=ddof)[1]
        else:
          f_obs=[observed[key] for key in sorted(observed.keys())]
          f_exp=[expected_x[key[0]] * expected_y[key[1]] / total_observed for key in sorted(observed.keys())]
          logging.debug('chisquare for total %i observed %s vs expected %s based on observed %s expected_x %s expected_y %s', total_observed, f_obs, f_exp, observed, expected_x, expected_y)
          pvalue = scipy.stats.chisquare(f_obs=[observed[key] for key in sorted(observed.keys())], f_exp=[expected_x[key[0]] * expected_y[key[1]] / total_observed for key in sorted(observed.keys())], ddof=ddof)[1]
        current_ds.append(' '.join(['{}/{}={} ({:.2f}%)'.format(key[0], key[1], observed[key], observed[key] / sum([observed[totals] for totals in observed if totals[0] == key[0]]) * 100) for key in sorted(observed.keys())]))
        # calculate odds (only 2x2 with pos/neg for now)
        if len(observed.keys()) == 4 and all([k[0] in POS_NEG and k[1] in POS_NEG for k in observed.keys()]):
          base_key = NEG.intersection(set(list(expected_x.keys()))).pop()
          alt_key = POS.intersection(set(list(expected_x.keys()))).pop()
          negative_key = NEG.intersection(set(list(expected_y.keys()))).pop()
          positive_key = POS.intersection(set(list(expected_y.keys()))).pop()
          base_positives =  observed[(base_key, positive_key)]
          base_negatives =  observed[(base_key, negative_key)]
          alt_positives =  observed[(alt_key, positive_key)]
          alt_negatives =  observed[(alt_key, negative_key)]
          if alt_negatives > 0 and base_positives > 0:
            current_or.append(alt_positives * base_negatives / alt_negatives / base_positives)
            current_bs.append(base_key)
          else:
            current_or.append(np.nan)
            current_bs.append('')
        else:
          current_or.append(np.nan)
          current_bs.append('')
      else: # no observations
        pvalue = 1
        current_ds.append('N/A')
        current_or.append(np.nan)
        current_bs.append('')

      if math.isnan(pvalue):
        pvalue = -1
      logging.debug('%s vs %s: %f...', x, y, pvalue)
      current.append(pvalue)

    zs.append(current)
    cs.append(current_cs)
    ds.append(current_ds)
    ts.append(current_ts)
    ors.append(current_or)
    bs.append(current_bs)
    
  if plot_or is not None:
    lors = []
    for row in ors:
      lors.append([math.log(c) if c != np.nan else np.nan for c in row])
    plot(plot_or, xs, lors, dpi, 'Log odds ratio', figwidth, figheight)

  if plot_pvalue is not None:
    plot(plot_pvalue, xs, zs, dpi, 'Correlation p-value', figwidth, figheight, cutoff=0.05)

  if out is not None:
    out.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format('x', 'y', 'p', 'or', 'or_base', 'n', 'data'))
    for x in range(len(xs)):
      for y in range(len(xs)):
        if x == y:
          continue
        out.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(xs[x], xs[y], zs[x][y], ors[x][y], bs[x][y], cs[x][y], ds[x][y]))

  logging.info('done')
  return {'xs': xs, 'zs': zs, 'cs': cs, 'ts': ts, 'ds': ds}

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Run correlation on selecetd columns')
  parser.add_argument('--cols', required=False, nargs='+', help='colnames to include')
  parser.add_argument('--delimiter', default=',', help='csv input delimiter')
  parser.add_argument('--plot_pvalue', required=False, help='plot to filename')
  parser.add_argument('--plot_or', required=False, help='plot to filename')
  parser.add_argument('--dpi', required=False, default=300, type=int, help='plot to filename')
  parser.add_argument('--plot_height', required=False, default=10, type=int, help='plot to filename')
  parser.add_argument('--plot_width', required=False, default=10, type=int, help='plot to filename')
  parser.add_argument('--empty', required=False, nargs='+', default=['N/A', ''], type=list, help='colnames to include')
  parser.add_argument('--equal_categories', action='store_true', help='calculate expected values')
  parser.add_argument('--verbose', action='store_true', help='more logging')
  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

  result = correlation(sys.stdin, sys.stdout, args.cols, args.delimiter, args.plot_pvalue, args.plot_or, args.dpi, args.plot_height, args.plot_width, args.empty, args.equal_categories)
