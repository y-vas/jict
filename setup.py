#!/usr/bin/env python
#
# Copyright (C) 2015 Leo Goodstadt <nested_dict@llew.org.uk>
#
# This file is part of nested_dict.
#
# nested_dict is free software: you can redistribute it and/or modify
# it under the terms of the MIT license as found here
# http://opensource.org/licenses/MIT.
#

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


import sys
if not sys.version_info[0:2] >= (2, 7):
    sys.stderr.write("Requires Python later than 2.7\n")
    sys.exit(1)


# Following the recommendations of PEP 396 we parse the version number
# out of the module.
def parse_version(module_file):
    """
    Parses the version string from the specified file.
    This implementation is ugly, but there doesn't seem to be a good way
    to do this in general at the moment.
    """
    f = open(module_file)
    s = f.read()
    f.close()
    match = re.findall("__version__ = '([^']+)'", s)
    return match[0]


f = open(os.path.join(os.path.dirname(__file__), "README.txt"))
nested_dict_readme = f.read()
f.close()
nested_dict_version = parse_version(os.path.join("nested_dict", "__init__.py"))

setup(
    name="nested_dict",
    version=nested_dict_version,
    description="An example Python package to simulate Kingman's coalescent",
    long_description=nested_dict_readme,
    packages=["nested_dict"],
    author='Leo Goodstadt',
    author_email='nested_dict@llew.org.uk',
    url="http://pypi.python.org/pypi/nested_dict",
    install_requires=[json],
    keywords=["dict", "defaultdict", "nested", "dictionary"],
    license="MIT",

    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        'Intended Audience :: Information Technology',
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries",
    ],
)

# python setup.py register
# python setup.py sdist --format=gztar,zip upload
