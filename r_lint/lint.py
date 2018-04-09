#!/usr/bin/env python
""" Linting code for QBiC R analysis environment
checks.
"""

import logging

import click

class RContainerLint(object):
    """ Object that hold linting info and result """

    def __init__(self, pipeline_dir):
        """ Init the linting object """
        self.path = pipeline_dir
    
    def lint_rproject(self):
        pass

