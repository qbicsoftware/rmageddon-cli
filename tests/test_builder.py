#!/usr/env/bin python

import os
import unittest

def pf(wd, path):
    return os.path.join(wd, path)

class TestBuilder(unittest.TestCase):
    """ Test class for the r_lint/builder.py code """

    def test_conda_env_parsing_pass(self):
        """ Parse a conda environment file sucessfully """
        