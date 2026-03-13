#!/usr/bin/env python
'''
  apply t-test for each group value vs all other groups, for multiple columns
'''

import argparse
import collections
import csv
import logging
import sys

import numpy as np

import statx.t_test

def table_group_multi(fh, out, group, cols, delimiter):
  '''
  For each group value and each column, calculate a t-test comparing
  values from that group versus values from all other groups.
  
  group: variable to separate groups on
  cols: list of column names to analyze
  '''
  logging.info('reading stdin...')
  fhr = csv.DictReader(fh, delimiter=delimiter)
  
  # Collect values for each group and column
  group_vals = collections.defaultdict(lambda: collections.defaultdict(list))
  for i, row in enumerate(fhr):
    logging.debug('processing row %i...', i)
    group_name = row[group]
    if group_name == '':
      continue
    for col in cols:
      if row[col] != '':
        group_vals[group_name][col].append(float(row[col]))
  
  groups = sorted([x for x in list(group_vals.keys()) if x != ''])
  logging.info('found %i groups: %s', len(groups), groups)
  
  # Write header
  out.write('group\tcol\tgroup_mean\tcol_mean\tgroup_sd\tcol_sd\tp_value\tsignificant\tdirection\n')
  
  # For each group and column, perform t-test
  for grp in groups:
    for col in cols:
      group_values = group_vals[grp][col]
      other_values = []
      for other_grp in groups:
        if other_grp != grp:
          other_values.extend(group_vals[other_grp][col])
      
      if len(group_values) == 0 or len(other_values) == 0:
        logging.warning('skipping %s/%s: empty groups', grp, col)
        continue
      
      logging.debug('comparing group %s vs others for column %s (%i vs %i values)', 
                   grp, col, len(group_values), len(other_values))
      
      result = statx.t_test.t_test(
        group_values, 
        other_values, 
        one_sided=False, 
        paired=False, 
        output=None
      )
      
      group_mean = np.mean(group_values)
      group_sd = np.std(group_values, ddof=1)
      col_mean = np.mean(other_values)
      col_sd = np.std(other_values, ddof=1)
      p_value = result['p-value']
      
      # Significance stars: *** p<0.001, ** p<0.01, * p<0.05
      if p_value < 0.001:
        significant = '***'
      elif p_value < 0.01:
        significant = '**'
      elif p_value < 0.05:
        significant = '*'
      else:
        significant = ''
      
      # Direction: positive if group has higher mean, otherwise negative
      direction = 'positive' if group_mean > col_mean else 'negative'
      
      # Format p_value: use scientific notation for very small values
      if p_value < 0.00001:
        p_value_str = '{:.2e}'.format(p_value)
      else:
        p_value_str = '{:.6f}'.format(p_value)
      
      out.write('{}\t{}\t{:.6f}\t{:.6f}\t{:.6f}\t{:.6f}\t{}\t{}\t{}\n'.format(
        grp, col, group_mean, col_mean, group_sd, col_sd, p_value_str, significant, direction
      ))
  
  logging.info('done')

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Run t-test for each group vs others, for multiple columns')
  parser.add_argument('--cols', required=True, nargs='+', help='columns to analyze')
  parser.add_argument('--group', required=True, help='column to separate groups on')
  parser.add_argument('--delimiter', default=',', help='input delimiter')
  parser.add_argument('--verbose', action='store_true', help='more logging')
  parser.add_argument('--quiet', action='store_true', help='less logging')
  args = parser.parse_args()
  
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  elif args.quiet:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.WARNING)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
  
  table_group_multi(sys.stdin, sys.stdout, args.group, args.cols, args.delimiter)
