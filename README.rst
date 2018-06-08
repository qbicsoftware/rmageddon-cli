
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


The command-line interface
===========================


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



