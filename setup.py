#!/usr/bin/env python

from setuptools import setup, find_packages

version = '0.1.0'

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name = 'r-lint',
    version = version,
    description = 'Small linting tool for R containers at QBiC',
    long_description = readme,
    keywords = ['R', 'linting', 'lint', 'Docker', 'container'],
    author = 'Sven Fillinger',
    author_email = 'sven.fillinger@qbic.uni-tuebingen.de',
    license = license,
    scripts = ['scripts/r-lint'],
    install_requires = required,
    packages = find_packages(exclude=('docs')),
    include_package_data = True
)