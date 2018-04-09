#!/usr/bin/env python
"""Some tests covering the linting code.
Provide example project contents like:

    --tests
            |--lint_examples
            |     |--example_project1
            |     |     |...<files here>
            |     |--example_project2
            |     |     |....<files here>
            |     |...
            |--test_lint.py
"""
import os
import unittest

import r_lint.lint as lint

def listfiles(path):
    files_found = []
    for (_,_,files) in os.walk(path):
        files_found.extend(files)
    return files_found

def pf(wd, path):
    return os.path.join(wd, path)

WD = os.path.dirname(__file__)
PATH_MINIMAL_WORKING_EXAMPLE = pf(WD, "lint_examples/minimal_working_example")

class TestLint(unittest.TestCase):
    """ Class for lint tests """
    
    def test_read_dir_content_and_pass(self):
        """ Check if the dir contains several files/dirs.
            
            Fails if not present: Dockerfile, rpackages.txt
            Warns if not present: scripts, data
        """
        lint_obj = lint.RContainerLint(PATH_MINIMAL_WORKING_EXAMPLE)
