# statx
Simple statistics calculations on the command line.

This package adds a simple interface to peform common statistics operation direct from the command line. It can also be used direct from other Python scripts.

## Installation
```
pip install git+https://github.com/supernifty/statx
```

## Usage

### accuracy.py
calculates auc with confidence interval (--ci), either direct on the command line (values1, values2) or reading columns from a tsv (colval, colgroup)
```
python statx/accuracy.py --values1 1 2 3 --values2 3 4 5 6
```

## anova.py

## binomial.py

## chi.py

## cluster.py

## correlation.py

## correlation_matrix.py

## distance.py

## grubbs.py

## mann_whitney.py

## metrics.py

## multiple.py
```
python statx/multiple.py --delimiter '   ' --pvalue pvalue --target bh < example/pvalues.tsv
```

## multiple_testing.py

```
python statx/multiple_testing.py --verbose --adjustments bonferroni benjamini_hochberg --pvalue pvalue < example/pvalues.tsv
```

## proportion.py

## t_test.py

```
python statx/t_test.py --values1 1 2 3 --values2 3 4 5 6
```

## table_cols.py

```
python statx/table_cols.py --cols1 x1 x2 --cols2 y1 y2 y3 --delimiter '	' < example/data.tsv
```

## table_correlation.py
## table_group.py
## table_test.py
## table_z.py

