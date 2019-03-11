import os
import sys
import unittest

from ruamel.yaml import YAML

from rmageddon.validation import RAnalysisValidation


def pf(wd, path):
    return os.path.join(wd, path)


# Define the working directory
WD = os.path.dirname(__file__)

# Define several test example directories
PATH_GOOD_DIFF = pf(WD, "validation_examples/diff/good_example")
PATH_BAD_DIFF = pf(WD, "validation_examples/diff/bad_example")


class TestValidation(unittest.TestCase):
    """ Class for validation tests """

    def assess_validation_status(self, validation_obj, **expected):
        """Little helper function for assessing the lint
        object status lists"""
        for list_type, expect in expected.items():
            observed = len(getattr(validation_obj, list_type))
            yaml = YAML(typ='safe')
            observed_list = yaml.dump(getattr(validation_obj, list_type), sys.stdout)
            self.assertEqual(observed, expect, "Expected {} tests in '{}' \
                , but found {}.\n{}"
                             .format(expect, list_type.upper(), observed, observed_list))

    def test_diff_good(self):
        validation_obj = RAnalysisValidation(PATH_GOOD_DIFF + "/analysis_1.txt",
                                             PATH_GOOD_DIFF + "/analysis_2.txt")
        validation_obj.diff()
        expectations = {"passed": 1, "warned": 0, "failed": 0}
        self.assess_validation_status(validation_obj, **expectations)

    def test_diff_bad(self):
        validation_obj = RAnalysisValidation(PATH_BAD_DIFF + "/analysis_1.txt",
                                             PATH_BAD_DIFF + "/analysis_2.txt")
        validation_obj.diff()
        expectations = {"passed": 0, "warned": 0, "failed": 755}
        self.assess_validation_status(validation_obj, **expectations)
