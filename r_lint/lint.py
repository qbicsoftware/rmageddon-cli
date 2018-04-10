#!/usr/bin/env python
""" Linting code for QBiC R analysis environment
checks.
"""
import os
import logging

import click

class RContainerLint(object):
    """ Object that hold linting info and result """

    def __init__(self, pipeline_dir):
        """ Init the linting object """
        self.path = pipeline_dir
        self.failed = []
        self.warned = []
        self.passed = []

    
    def lint_rproject(self):
        """ Main linting function.

        This function takes the R project directory and scans 
        it for different files/dirs and compares it
        against best practice rules we defined at QBiC for
        having an interoperable, reproducible R environment
        for bioinformatic analysis.

        Returns:
            dict: Summary of test result messages structured as follows:
            {
                'pass': [
                    ( test-id (int), message (string) ),
                    ( test-id (int), message (string) )
                ],
                'warn': [(id, msg)],
                'fail': [(id, msg)],
            }
        
         Raises:
            If a critical problem is found, an AssertionError is raised.
        """
        check_functions = [
            'check_files_exist',
            'check_dockerfile',
            'check_rpackages'
        ]

        with click.progressbar(check_functions, label='Running R projects tests', item_show_func=repr) as fnames:
            for fname in fnames:
                getattr(self, fname)()
                if len(self.failed) > 0:
                    logging.error("Found test failures in '{}', halting lint run.".format(fname))
                    break
    
    def check_files_exist(self):
        files_fail = [
            'Dockerfile',
            'rpackages.txt'
        ]
        files_warn = [
            'data',
            'scripts'
        ]

        def pf(file_path):
            return os.path.join(self.path, file_path)

        for files in files_fail:
            if not os.path.isfile(pf(files)):
                self.failed.append((1, 'File {} not found.'.format(files)))
            else:
                self.passed.append((1, 'File {} found.'.format(files)))
        
        for files in files_warn:
            if not os.path.isdir(pf(files)):
                self.warned.append((1, 'Dir {} not found.'.format(files)))
            else:
                self.passed.append((1, 'Dir {} found.'.format(files)))
        
    
    def check_dockerfile(self):
        pass

    def check_rpackages(self):
        pass
