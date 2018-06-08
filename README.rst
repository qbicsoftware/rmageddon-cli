
Rmageddon
##############

.. image:: https://travis-ci.org/qbicsoftware/r-lint-cli.svg?branch=master
    :target: https://travis-ci.org/qbicsoftware/r-lint-cli

.. image:: https://codecov.io/gh/qbicsoftware/qbic-r-lint/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/qbicsoftware/qbic-r-lint

A small linting and building command line tool for reproducible R analysis with Docker at QBiC.

Motivation
    Performing a reproducible analysis with R and share the environment status of an R installation with the 
    necessary packages and all that with the correct version is a very challenging task.

    In order to face this issue, under the umbrella of better reproducibility of computational results, we created
    `Rmageddon`, a small command-line tool, that assists in the build of Docker container with specified version of R and
    a dedicated, version-defined package installation. 

    The container collection is hosted on a different GitHub repository: https://github.com/qbicsoftware/r-container-lib.

    All containers there passed the linting and have been build with `Rmageddon`.

.. contents:: **Table of Contents**


Installation
============

The easiest way is to install a stable release of ``r-lint`` from PyPi_ with pip_:

.. code-block:: bash

    $ pip install r-lint

Or if you want the latest development version, you can install from the ``master`` branch on GitHub with:

.. code-block:: bash

    $ pip install git+https://github.com/qbicsoftware/r-lint-cli

.. _PyPi: https://pypi.org/
.. _pip: https://pypi.org/project/pip/


The command-line interface
===========================

Once you have installed *r-lint*, just call it with the ``--help`` option to get an overview of the subcommands
available in *r-lint*:

.. code-block:: bash

    $ r-lint --help
    ______     __         __     __   __     ______  
   /\  == \   /\ \       /\ \   /\ "-.\ \   /\__  _\ 
   \ \  __<   \ \ \____  \ \ \  \ \ \-.  \  \/_/\ \/ 
    \ \_\ \_\  \ \_____\  \ \_\  \ \_\ "\_\    \ \_\ 
     \/_/ /_/   \/_____/   \/_/   \/_/ \/_/     \/_/ 
                                                  
    2018, QBiC software, Sven Fillinger
    sven.fillinger@qbic.uni-tuebingen.de
        
    Usage: r-lint [OPTIONS] COMMAND [ARGS]...

    Options:
    --version      Show the version and exit.
    -v, --verbose  Verbose output (print debug statements)
    --help         Show this message and exit.

    Commands:
    build  Resolve R packages resources from Anaconda...
    lint   Check R project against linting guidelines


If you want to know the positional arguments and options of each subcommand, just type ``r-lint build --help`` or 
``r-lint lint --help``.


The subcommand <lint>
---------------------

The subcommand <lint> is actually checking an R container project against some specified rule-set. Currently, *r-lint* is assuming the following project structure:

.. code-block: bash

    .
    ├── data
    │   └── input_data   // A collection of input data
    |   └── ...
    ├── Dockerfile       // Docker container recipe
    ├── environment.yml  // Conda environment recipe
    └── scripts
        └── example.R    // A collection of R scripts
        └── ...

Start the linting of a project directoy with:

.. code-block: bash

    $ r-lint lint /path/to/project
 
The linting will report warnings and failures by default. Failure events are recorded, if you did not provide:

- A file named ``Dockerfile``, the receipe for the Docker container 
- A file named ``environment.yml``, the **Conda configuration file**

There a warnings raised, if you did not provide:

- A folder named ``data``, with the input data for the R analysis
- A folder named ``scripts``, with the R scripts themselves

Dockerfile 
    For the ``Dockerfile`` some things are mandatory, like:
        
    - ``LABEL name`` - The name of the container. Needs to match the regex ``(Q|q)[a-zA-Z0-9]{4}-ranalysis``, for example **qtest-ranalysis**
    - ``LABEL maintainer`` - The name of the container maintainer with email, for example **Sven Fillinger <sven.fillinger@qbic.uni-tuebingen.de>**
    - ``LABEL version`` - The 3-digit numeric version string following the `semantic version standard`__
    - ``LABEL organization`` - The organization's name
    - ``LABEL github`` - The link to the GitHub repository

__ semantic_
.. _semantic: https://semver.org/


The subcommand <build>
----------------------

TODO: describe.
