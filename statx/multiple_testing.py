#!/usr/bin/env python
'''
  add multiple testing
'''

import argparse
import csv
import logging
import sys


def main(infh, outfh, delimiter, pvalue, adjustments, alpha=0.05):
  logging.info('reading from stdin...')
  idr = csv.DictReader(infh, delimiter=delimiter)
  rows = []
  for r in idr:
    rows.append(r)
  logging.info('%i records', len(rows))

  # sort by pvalue
  sorted_rows = sorted(rows, key=lambda x: float(x[pvalue]))
  #logging.debug(sorted_rows)
  
  if 'benjamini_hochberg' in adjustments:
    benjamini_thresholds = [(xi + 1) / len(rows) * alpha for xi in range(len(rows))]
    logging.debug(benjamini_thresholds)
    pvalues = [float(sorted_rows[xi][pvalue]) for xi in range(len(rows))]
    logging.debug(pvalues)
    benjamini_significant = [float(sorted_rows[xi][pvalue]) < benjamini_thresholds[xi] for xi in range(len(rows))]
    logging.debug(benjamini_significant)
    max_benjamini_index = max([-1] + [xi for xi in range(len(rows)) if benjamini_significant[xi]])
    logging.debug('benjamini index is %i', max_benjamini_index)

  odw = csv.DictWriter(outfh, delimiter=delimiter, fieldnames=idr.fieldnames + adjustments)
  odw.writeheader()
  for idx, r in enumerate(sorted_rows):
    if 'benjamini_hochberg' in adjustments:
      r['benjamini_hochberg'] = 'Yes' if  idx <= max_benjamini_index else 'No'
    if 'bonferroni' in adjustments:
      r['bonferroni'] = float(r[pvalue]) * len(rows)
    odw.writerow(r)

  logging.info('done')

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Add multiple testing p-values')
  parser.add_argument('--delimiter', required=False, default=',', help='table format')
  parser.add_argument('--pvalue', required=True, help='column with pvalue')
  parser.add_argument('--adjustments', required=True, nargs='+', help='bonferroni benjamini_hochberg')
  parser.add_argument('--verbose', action='store_true', help='more logging')
  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

  main(sys.stdin, sys.stdout, args.delimiter, args.pvalue, args.adjustments)
