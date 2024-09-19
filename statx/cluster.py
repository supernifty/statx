#!/usr/bin/env python
'''
  apply clustering based on column
'''

import argparse
import csv
import logging
import sys

import numpy as np
import sklearn.mixture

def main(ifh, ofh, column, newcolumn, delimiter='\t'):
  logging.info('reading from stdin...')
  X = []
  rows = []
  idr = csv.DictReader(ifh, delimiter=delimiter)
  for r in idr:
    X.append([float(r[column])])
    rows.append(r)

  # cluster it
  logging.info('clustering...')
  model = sklearn.mixture.BayesianGaussianMixture(
      n_components=3,
      covariance_type="full",
      weight_concentration_prior=1e-2,
      weight_concentration_prior_type="dirichlet_process",
      mean_precision_prior=1e-2,
      covariance_prior=0.5 * np.eye(1),
      init_params="random",
      max_iter=1000,
      random_state=2,
  ).fit(X)

  ys = model.predict(X)
  logging.info('writing...')
  odw = csv.DictWriter(ofh, delimiter=delimiter, fieldnames=idr.fieldnames + [newcolumn])
  odw.writeheader()
  for r, y in zip(rows, ys):
    r[newcolumn] = y
    odw.writerow(r)

  logging.info('done')

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Try to cluster into two groups based on column')
  parser.add_argument('--column', required=True, help='input column')
  parser.add_argument('--newcolumn', required=True, help='column name to add specifying predicted cluster')
  parser.add_argument('--verbose', action='store_true', help='more logging')
  args = parser.parse_args()
  if args.verbose:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.DEBUG)
  else:
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

  main(sys.stdin, sys.stdout, args.column, args.newcolumn)

