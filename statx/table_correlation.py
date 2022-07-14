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

def correlation(fh, out, cols, delimiter, plot, dpi=300):
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

  # process
  xs = []
  cs = []
  ds = []
  ts = []
  zs = []
  for x in sorted(data.keys()):
    xs.append(x)
    current = []
    current_cs = []
    current_ts = []
    current_ds = [] # details
    for y in sorted(data.keys()): # y is colname
      logging.debug('%s vs %s...', x, y)
      # assume chi-square
      observed = collections.defaultdict(int)
      expected_x = collections.defaultdict(int)
      expected_y = collections.defaultdict(int)
      for idx, _ in enumerate(data[x]): # values from x column
        key = (data[x][idx], data[y][idx])
        observed[key] += 1
        expected_x[data[x][idx]] += 1
        expected_y[data[y][idx]] += 1
  
      total_observed = sum([observed[key] for key in observed])
      current_cs.append(total_observed)
      current_ts.append('Chi-square')
      if total_observed > 0:
        pvalue = scipy.stats.chisquare([observed[key] for key in sorted(observed.keys())], [expected_x[key[0]] * expected_y[key[1]] / total_observed for key in sorted(observed.keys())])[1]
        current_ds.append(' '.join(['{}/{}={}'.format(key[0], key[1], observed[key]) for key in sorted(observed.keys())]))
      else:
        pvalue = 1
        current_ds.append('N/A')

      if math.isnan(pvalue):
        pvalue = -1
      logging.debug('%s vs %s: %f...', x, y, pvalue)
      current.append(pvalue)

    zs.append(current)
    cs.append(current_cs)
    ds.append(current_ds)
    ts.append(current_ts)
    
  r = {'xs': xs, 'zs': zs, 'cs': cs, 'ts': ts, 'ds': ds}
  if plot is not None:
    fig = plt.figure()
    ax = fig.add_subplot(111)
    #fig, ax = plt.subplots()

    # Show all ticks and label them with the respective list entries
    ax.set_xticks(np.arange(len(xs)))
    ax.set_yticks(np.arange(len(xs)))

    im = ax.imshow(zs)
    for i in range(len(xs)):
      for j in range(len(xs)):
        text = ax.text(j, i, '{:.2f}'.format(zs[i][j]), ha="center", va="center", color="w")

    #ax.set_xticks(np.arange(len(xs)))
    #ax.set_yticks(np.arange(len(xs)))

    ax.set_xticklabels(xs, rotation=45)
    ax.set_yticklabels(xs)

    ax.set_ylim(len(xs)-0.5, -0.5)

    ax.set_title("Correlation p-value")
    fig.tight_layout()
    plt.savefig(plot, dpi=dpi)

  logging.info('done')
  return r

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Run correlation on selecetd columns')
  parser.add_argument('--cols', required=False, nargs='+', help='colnames to include')
  parser.add_argument('--delimiter', default=',', help='csv input delimiter')
  parser.add_argument('--plot', required=False, help='plot to filename')
  parser.add_argument('--verbose', action='store_true', help='more logging')
  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

  result = correlation(sys.stdin, sys.stdout, args.cols, args.delimiter, args.plot)
  # todo better layout
  logging.info('result: %s', result)
