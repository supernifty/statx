# statx
Simple statistics calculations on the command line

## Installation
```
pip install git+https://github.com/supernifty/statx
```

## Usage
```
python statx/t_test.py --values1 1 2 3 --values2 3 4 5 6
```

```
python statx/table.py --cols1 x1 x2 --cols2 y1 y2 y3 --delimiter '	' < example/data.tsv
```

```
python statx/multiple.py --delimiter '   ' --pvalue pvalue --target bh < example/pvalues.tsv
```
