#!/usr/bin/env python
import re, os
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup


# Following the recommendations of PEP 396 we parse the version number
# out of the module.
def parse_version(module_file):
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
    name = "jict",
    version= jict_version,
    description="Python dictionary with automatic and arbitrary levels of nestedness",
    long_description= jict_readme,
    packages = ["jict"],
    author='Vasyl Yovdiy',
    author_email='yovdiyvasyl@gmail.com',
    url="https://github.com/y-vas/jict",
    install_requires=[],
    setup_requires=[],
    keywords = ["nested", "jict", "defaultdict", "dictionary", "auto-vivification"],
    license = "MIT",
    classifiers=[
        "Topic :: Utilities",
    ],
)
