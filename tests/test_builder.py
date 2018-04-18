#!/usr/env/bin python

import os
import unittest

import r_lint.builder as builder

def pf(wd, path):
    return os.path.join(wd, path)

# Define the working directory
WD = os.path.dirname(__file__)

# Define several test example directories
PATH_GOOD_CONDA_ENV = pf(WD, "builder_examples/good_environment")
PATH_GOOD_R_PKS = pf(WD, "builder_examples/good_r_packages")

class TestBuilder(unittest.TestCase):
    """ Test class for the r_lint/builder.py code """

    def test_conda_env_parsing_pass(self):
        """ Parse a conda environment file sucessfully """
        builder_obj = builder.EnvBuilder(
            pf(PATH_GOOD_R_PKS, "rpackages.txt"),
            pf(PATH_GOOD_CONDA_ENV, "environment.yml")
        )
        