#!/usr/env/bin python

import os
import sys
import unittest

from ruamel.yaml import YAML
import rmageddon.builder as builder

def pf(wd, path):
    return os.path.join(wd, path)

# Define the working directory
WD = os.path.dirname(__file__)

# Define several test example directories
PATH_GOOD_CONDA_ENV = pf(WD, "builder_examples/good_environment")
PATH_GOOD_R_PKS = pf(WD, "builder_examples/good_r_packages")
PATH_EMPTY_R_PKS = pf(WD, "builder_examples/empty_r_packages")

class TestBuilder(unittest.TestCase):
    """ Test class for the rmageddon/builder.py code """

    def assess_lint_status(self, lint_obj, **expected):
        """Little helper function for assessing the lint
        object status lists"""
        for list_type, expect in expected.items():
            observed = len(getattr(lint_obj, list_type))
            yaml = YAML(typ='safe')
            observed_list = yaml.dump(getattr(lint_obj, list_type), sys.stdout)
            self.assertEqual(observed, expect, "Expected {} tests in '{}' \
                , but found {}.\n{}"
                .format(expect, list_type.upper(), observed, observed_list))
    
    def test_conda_env_parsing_pass(self):
        """ Parse a conda environment file sucessfully """
        builder_obj = builder.EnvBuilder(
            pf(PATH_GOOD_R_PKS, "rpackages.txt"),
            pf(PATH_GOOD_CONDA_ENV, "environment.yml")
        )
        builder_obj.build()
    
    def test_rpackage_parsing_and_warn(self):
        """ Parse a r package file and warn if empty """
        builder_obj = builder.EnvBuilder(
            pf(PATH_EMPTY_R_PKS, "rpackages.txt"),
            pf(PATH_GOOD_CONDA_ENV, "environment.yml")
        )
        builder_obj.check_rpkgs()
        expectations = {"passed": 0, "warned": 2, "failed": 0}
        self.assess_lint_status(builder_obj, **expectations)
    
    def test_rpackage_resolving_and_pass(self):
        """ Try to resolve a given R package dependency from either
        Anaconda's 'r'- or 'bioconda'-channel """
        builder_obj = builder.EnvBuilder(
            pf(PATH_GOOD_R_PKS, "rpackages.txt"),
            pf(PATH_GOOD_CONDA_ENV, "environment.yml")
        )
        builder_obj.check_rpkgs()
        expectations = {"passed": 2, "warned": 1, "failed": 0}
        self.assess_lint_status(builder_obj, **expectations)

    def test_conda_env_extension(self):
        """ Check, that resolved R packages are listed as dependencies in the 
        environment.yml """
        builder_obj = builder.EnvBuilder(
            pf(PATH_GOOD_R_PKS, "rpackages.txt"),
            pf(PATH_GOOD_CONDA_ENV, "environment.yml")
        )
        builder_obj.check_rpkgs()
        builder_obj.extend_conda_env()
        expectations = {"passed": 3, "warned": 1, "failed": 0}
        self.assess_lint_status(builder_obj, **expectations)
        self.assertEquals(len(builder_obj.conda_env.get("dependencies")),
            3)
        