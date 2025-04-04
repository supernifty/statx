#!/usr/bin/env python

import setuptools
import pathlib
from glob import glob

name = "statx"
version = "0.1"
release = "0.1.0"
here = pathlib.Path(__file__).parent.resolve()

setuptools.setup(
    name=name,
    version=version,
    install_requires=['scipy'],
    packages=setuptools.find_packages(),
    scripts=[i for i in glob('statx/*.py') if "__init__" not in i],
)
