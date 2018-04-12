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

        for files in files_fail:
            if not os.path.isfile(self.pf(files)):
                self.failed.append((1, 'File {} not found.'.format(files)))
            else:
                self.passed.append((1, 'File {} found.'.format(files)))
        
        for files in files_warn:
            if not os.path.isdir(self.pf(files)):
                self.warned.append((1, 'Dir {} not found.'.format(files)))
            else:
                self.passed.append((1, 'Dir {} found.'.format(files)))
        
    
    def check_dockerfile(self):
        """ Check the Dockerfile not to be empty and fulfill
        some basic checks:
            - Building from r-base
            - Import of the rpackages.txt
            - Some labels present
        """
        with open(self.pf('Dockerfile')) as d_file: content = d_file.readlines()
        
        if not content:
            self.failed.append((2, 'Dockerfile seems to be empty.'))
            return

        labels = {}
        base_img = []
        rpackage_def = []

        for line in content:
            if 'LABEL' in line:
                line = line.strip()
                labels[line.split('=')[0].strip()] = line.split('=')[1].strip()
            if 'FROM' in line:
                line = line.strip()
                base_img.append(line)
            if 'rpackage.txt' in line:
                line = line.strip()
                rpackage_def.append(line)
        
        # 1. Evaluate the base image beeing from r-base
        if not base_img:
            self.failed.append((2, 'No base image was defined in the Dockerfile.'))
            return
        if any('r-base' in base for base in base_img[0].strip().split()):
            self.passed.append((2, 'Base image \'r-base\' was found in the Dockerfile.'))
        else:
            self.failed.append((2, 'Container is not build from \'r-base\' image'))

    def check_rpackages(self):
        """ Make some simple checks for the rpackages.txt,
        like raise a warning, if it is empty and fail, if there
        is more than one package listed per line.
        """
        with open(self.pf('rpackages.txt'), 'r') as fh: package_list = fh.read().splitlines() 
        
        if not package_list:
            self.warned.append((3, 'The R package list seems to be empty.'))
            return

        for index, line in enumerate(package_list):
            content = line.strip().split()
            if len(content) > 1:
                self.failed.append((3, 'Line {} seems to have more than one package defined.'.format(index)))
                return
        self.passed.append((3, 'R package list seems to be OK.'))

    def pf(self, file_path):
        """ Quick path join helper method """
        return os.path.join(self.path, file_path)

