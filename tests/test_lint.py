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
import yaml
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
PATH_OPTIMAL_WORKING_EXAMPLE = pf(WD, "lint_examples/awesome_working_example")
PATH_BAD_EXAMPLE = pf(WD, "lint_examples/bad_example")
# The maximum number of checks that can be passed
MAX_PASS_CHECKS = 5

class TestLint(unittest.TestCase):
    """ Class for lint tests """

    def assess_lint_status(self, lint_obj, **expected):
        """Little helper function for assessing the lint
        object status lists"""
        for list_type, expect in expected.items():
            observed = len(getattr(lint_obj, list_type))
            oberved_list = yaml.safe_dump(getattr(lint_obj, list_type))
            self.assertEqual(observed, expect, "Expected {} tests in '{}', but found {}.\n{}".format(expect, list_type.upper(), observed, oberved_list))
    
    def test_read_dir_content_and_pass(self):
        """ Check if the dir contains several files/dirs.
            Minimal example for passing.

            Fails if not present: Dockerfile, rpackages.txt
            Warns if not present: scripts, data
        """
        lint_obj = lint.RContainerLint(PATH_MINIMAL_WORKING_EXAMPLE)
        lint_obj.lint_rproject()
        expectations = {"failed": 0, "warned": 2, "passed": MAX_PASS_CHECKS - 2}
        self.assess_lint_status(lint_obj, **expectations)
    
    def test_read_dir_ultimate_content_and_pass(self):
        """ Check if the dir contains several files/dirs.
            Optimal example for passing.

            Fails if not present: Dockerfile, rpackages.txt
            Warns if not present: scripts, data
        """
        lint_obj = lint.RContainerLint(PATH_OPTIMAL_WORKING_EXAMPLE)
        lint_obj.lint_rproject()
        expectations = {"failed": 0, "warned": 0, "passed": MAX_PASS_CHECKS}
        self.assess_lint_status(lint_obj, **expectations)
    
    def test_dockerfile_without_base_image(self):
        """ Check if a Dockerfile has the correct base image
        included from r-base 
        """
        lint_obj = lint.RContainerLint(PATH_BAD_EXAMPLE)
        lint_obj.check_dockerfile()
        expectations = {"failed": 1, "warned": 0, "passed": 0}
        self.assess_lint_status(lint_obj, **expectations)
    