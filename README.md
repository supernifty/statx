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
Perform an anova with up to 7 groups.

```
python statx/anova.py --values1 1 2 3 --values2 3 4 5 6
```

## binomial.py
Applies a binomial test. 

Generates a pvalue, as well as confidence intervals for the probability of success.

```
python statx/binomial.py --k 10 --n 15 --p 0.4
```

## chi.py
Performs a Fisher exact test (if 4 values), or otherwise a chi-square test

```
python statx/chi.py --values 13 2 1 10
```

## cluster.py
Try to cluster a column into three groups

```
python statx/cluster.py --column a --newcolumn b < example/data2.tsv
```

## correlation.py
measure pearson or spearman correlation from provided values or columns in a table

```
statx/correlation.py --values1 1 1 2 4 6 8 --values2 1 2 3 4 5 6
```

## correlation_matrix.py
correlation of each column vs each other column
```
python statx/correlation_matrix.py --cols a b c < example/data2.tsv
```

## distance.py
cosine distance of every row vs every other row, excluding the specified row which becomes the row's name
```
statx/distance.py --name a < example/data2.tsv
```

## grubbs.py
statistical test for a point belonging to a specified normal distribution

```
python statx/grubbs.py --value 12 --values 2 3 4 5 6 7 8 9
```

## mann_whitney.py
Performs a mann whitney U test

```
python statx/mann_whitney.py --values1 2 3 4 5 6 7 8 9 --values2 7 8 9 10
```

## metrics.py
Common measures of accuracy based on 2x2 data

```
python statx/metrics.py --tp 3 --tn 4 --fn 1 --fp 0
```

## multiple.py
Apply multiple hypothesis correction

```
python statx/multiple.py --delimiter '   ' --pvalue pvalue --target bh < example/pvalues.tsv
```

## multiple_testing.py
Apply multiple hypothesis correction

```
python statx/multiple_testing.py --verbose --adjustments bonferroni benjamini_hochberg --pvalue pvalue < example/pvalues.tsv
```

## proportion.py
Perform a 2-sample proportion test

```
python statx/proportion.py --values1 2 3 4 5 6 7 8 9 --values2 7 8 9 10
```

## t_test.py
Perform a t-test

```
python statx/t_test.py --values1 1 2 3 --values2 3 4 5 6
```

## table_cols.py
performs a t-test row by row for the specified columns

```
python statx/table_cols.py --cols1 x1 x2 --cols2 y1 y2 y3 --delimiter '	' < example/data.tsv
```

## table_correlation.py
generate pair-wise chi-square for all specified columns; can also generate heatmaps of pvalues or odds ratios

```
python statx/table_correlation.py --cols x1 x2 y1 y2 --delimiter '	' < example/data.tsv
```

## table_group.py
makes groups based on one column, with values from another column, then runs a t-test, anova or chi-square
```
python statx/table_group.py --group n --col x1 --test t_test --delimiter '	' < example/data.ts

```

## table_test.py
## table_z.py

