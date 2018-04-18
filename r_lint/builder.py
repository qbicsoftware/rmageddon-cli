#1/usr/env/bin python
""" Class for creating a working environment.yml
for the conda environment, based on a list of R packages.

The class shall query information automatically accessing
the Anaconda cloud API for R packages living in
the 'r'-channel (CRAN packages) and 'bioconda'-channel
(i.e. Bioconductor).

R packages found in the 'r'-channel follow the scheme:
    r-<CRAN pkg name>
and for 'anaconda' it is:
    bioconductor-<bioconductor pkg name>
"""

import logging

import yaml
import click

class EnvBuilder(object):

    def __init__(self, rpackages, conda_env):
        """ Init the EnvBuilder object that is able 
        to read a R package list and tries to translate it
        to conda dependencies
        """
        self.failed = []
        self.warned = []
        self.passed = []
        self.conda_env = self.parse_conda_env(conda_env)
        self.rpackages = self.parse_package_list(rpackages)

    def build(self):
        """ Takes a list of R packages and tries to find the
        corresponding package in the Anaconda cloud
        and annotates it accordingly in the conda environment
        config file
        """
        check_functions = [
            'check_rpkgs'
        ]

        with click.progressbar(check_functions,
                label='Running R package resolve tasks', item_show_func=repr) as fnames:
            for fname in fnames:
                getattr(self, fname)()
                if len(self.failed) > 0:
                    logging.error("Found test failures in '{}', \
                    halting lint run.".format(fname))
                    break

    def check_rpkgs(self):
        """ Check the rpackage list against the openbis API """
        if not self.rpackages:
            self.warned.append((2, "The R package file seems to be empty."))
            return
    
    def parse_conda_env(self, conda_env):
        with open(conda_env, 'r') as stream:
            data = yaml.load(stream)
        return data

    def parse_package_list(self, rpackages):
        with open(rpackages, 'r') as stream:
            packages = stream.read().splitlines()
        return packages
