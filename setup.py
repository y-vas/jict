#!/usr/bin/env python
#
# Copyright (C) 2015 Leo Goodstadt <jict@llew.org.uk>
#
# This file is part of jict.
#
# jict is free software: you can redistribute it and/or modify
# it under the terms of the MIT license as found here
# http://opensource.org/licenses/MIT.
#
"""Setup module for nested-dict."""

import re
import os

# First, we try to use setuptools. If it's not available locally,
# we fall back on ez_setup.
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup


# Following the recommendations of PEP 396 we parse the version number
# out of the module.
def parse_version(module_file):
    """
    Parse the version string from the specified file.

    This implementation is ugly, but there doesn't seem to be a good way
    to do this in general at the moment.
    """
    f = open(module_file)
    s = f.read()
    f.close()
    match = re.findall("__version__ = '([^']+)'", s)
    return match[0]


f = open(os.path.join(os.path.dirname(__file__), "README.rst"))
jict_readme = f.read()
f.close()
jict_version = parse_version(os.path.join("jict", "__init__.py"))

setup(
    name="jict",
    version=jict_version,
    description="Python dictionary with automatic and arbitrary levels of nestedness",
    long_description=jict_readme,
    packages=["jict"],
    author='Leo Goodstadt',
    author_email='jict@llew.org.uk',
    url="http://pypi.python.org/pypi/jict",
    install_requires=[],
    setup_requires=[],
    keywords=["nested", "dict", "defaultdict", "dictionary", "auto-vivification"],
    license="MIT",

    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Developers",
        'Intended Audience :: Information Technology',
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Scientific/Engineering",
        "Topic :: Utilities",
    ],

    test_suite="tests.test_jict",
)

# python setup.py register
# flake8 *.py tests --exclude=ez_setup.py --max-line-length=100
# nosetests --with-coverage --cover-package jict --cover-inclusive --cover-min-percentage 85
# make -C docs html
# git tag -a v1.5.1 -m "Version 1.5.1"
# python setup.py sdist --format=gztar,zip upload
