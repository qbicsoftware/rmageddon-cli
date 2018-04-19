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

import requests
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
        self.resolved = {}
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
        """ Check the rpackage list against the Anaconda cloud API """
        if not self.rpackages:
            self.warned.append((2, "The R package file seems to be empty."))
            return
        
        # Define the conda channels in which to search for R packages
        channels = {
            'r': 'r',
            'bioconda': 'bioconductor'
        }

        for rpackage in self.rpackages:
            for channel in channels.keys():
                anaconda_url = "https://api.anaconda.org/package/{ch}/{pkg}".format(
                    ch = channel,
                    pkg = "{prefix}-{pkg}".format(
                        prefix = channels.get(channel),
                        pkg = rpackage
                        )
                )
                try:
                    resp = requests.get(anaconda_url, timeout=10)
                except (requests.exceptions.Timeout):
                    self.warned.append((2, "Server Timout! Package {pkg} could not be resolved.".format(
                       pkg = rpackage 
                    )))
                else:
                    if resp.status_code == 200:
                        self.resolved[rpackage] = "{ch}::{prefix}-{pkg}".format(
                            ch = channel,
                            prefix = channels.get(channel),
                            pkg = rpackage
                            )
                        self.passed.append(
                            (2, "Package {pkg} resolved in channel {channel}".format(
                                pkg = rpackage,
                                channel = channel
                            ))
                        )
                        break
                    else:
                        self.resolved[rpackage] = ""

        # Check for packages that could not have been resolved
        unresolved_pkgs = list([pkg for pkg, pkg_name_ch in self.resolved.items() 
            if not pkg_name_ch])
        
        # And report them
        for pkg in unresolved_pkgs:
            self.warned.append((2,
                "Could not resolve package {pkg} on Anaconda cloud.".format(
                    pkg = pkg
                )
            ))
        

                        





        
        
    
    def parse_conda_env(self, conda_env):
        with open(conda_env, 'r') as stream:
            data = yaml.load(stream)
        return data

    def parse_package_list(self, rpackages):
        with open(rpackages, 'r') as stream:
            packages = stream.read().splitlines()
        return packages
