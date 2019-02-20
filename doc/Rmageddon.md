# Rmageddon

This is the main documentation for the Rmageddon core functionality: building and linting. The documentation for Rmageddons cookiecutter can be found here: [Rmageddon-cookiecutter](Rmageddon-cookiecutter)


Installation
============

The easiest way is to install a stable release of ``rmageddon`` from PyPi_ with pip_:


```bash 
    $ pip install rmageddon
```


Or if you want the latest development version, you can install from the ``master`` branch on GitHub with:

```bash
    $ pip install git+https://github.com/qbicsoftware/rmageddon-cli
```


The command-line interface
===========================

Once you have installed rmageddon, just call it with the ``--help`` option to get an overview of the subcommands
available in rmageddon:

```bash

    $ rmageddon --help
 _______  _______  _______  _______  _______  ______   ______   _______  _       
(  ____ )(       )(  ___  )(  ____ \(  ____ \(  __  \ (  __  \ (  ___  )( (    /|
| (    )|| () () || (   ) || (    \/| (    \/| (  \  )| (  \  )| (   ) ||  \  ( |
| (____)|| || || || (___) || |      | (__    | |   ) || |   ) || |   | ||   \ | |
|     __)| |(_)| ||  ___  || | ____ |  __)   | |   | || |   | || |   | || (\ \) |
| (\ (   | |   | || (   ) || | \_  )| (      | |   ) || |   ) || |   | || | \   |
| ) \ \__| )   ( || )   ( || (___) || (____/\| (__/  )| (__/  )| (___) || )  \  |
|/   \__/|/     \||/     \|(_______)(_______/(______/ (______/ (_______)|/    )_)
                                                                                 
                                                  
    2018, QBiC software, Sven Fillinger
    sven.fillinger@qbic.uni-tuebingen.de
        
    Usage: rmageddon [OPTIONS] COMMAND [ARGS]...

    Options:
    --version      Show the version and exit.
    -v, --verbose  Verbose output (print debug statements)
    --help         Show this message and exit.

    Commands:
    build  Resolve R packages resources from Anaconda...
    lint   Check R project against linting guidelines
```


If you want to know the positional arguments and options of each subcommand, just type ``rmageddon build --help`` or 
``rmageddon lint --help``.


The subcommand <lint>
---------------------

The subcommand <lint> is actually checking an R container project against some specified rule-set. Currently, *rmageddon* is assuming the following project structure:
```bash

    .
    ├── data
    │   └── input_data   // A collection of input data
    |   └── ...
    ├── Dockerfile       // Docker container recipe
    ├── environment.yml  // Conda environment recipe
    └── scripts
        └── example.R    // A collection of R scripts
        └── ...
```

Start the linting of a project directoy with:

```bash

    $ rmageddon lint /path/to/project
```
 
The linting will report warnings and failures by default. **Failure** events are recorded, if you did not provide:

- A file named ``Dockerfile``, the receipe for the Docker container 
- A file named ``environment.yml``, the **Conda configuration file**

There a **warnings** raised, if you did not provide:

- A folder named ``data``, with the input data for the R analysis
- A folder named ``scripts``, with the R scripts themselves

Dockerfile 
    For the ``Dockerfile`` some things are mandatory, like:
        
    - ``LABEL name`` - The name of the container. Needs to match the regex ``(Q|q)[a-zA-Z0-9]{4}-ranalysis``, for example **qtest-ranalysis**
    - ``LABEL maintainer`` - The name of the container maintainer with email, for example **Sven Fillinger <sven.fillinger@qbic.uni-tuebingen.de>**
    - ``LABEL version`` - The 3-digit numeric version string following the `semantic version standard`__
    - ``LABEL organization`` - The organization's name
    - ``LABEL github`` - The link to the GitHub repository


The subcommand <build>
----------------------

The subcommand ``build`` is a small helper tool, that is able to parse ``sessionInfo`` output from R and extracts the package names with versions.

It then takes these and checks on [Anaconda Cloud](https://anaconda.org/) if these are available in one of the pre-defined channels `[default, r, bioconda]`. If successful, it will automatically add the corresponding conda package with version in the `environment.yml`. If a package cannot be found, a warning is printed on the command-line. If a specified version of a package is not found, it prints the available versions on the command-line.

To start the build, be sure you have an active internet connection and run it with:

```bash 
    $ rmageddon build <R package list> environment.yml
```

The ``R package list`` can be obtained from inside your active R session, that was used to run your R analysis successfully. From within your R console, just type:

```R

    > sessionInfo()$otherPkgs
```
This is your R package list, which is needed for rmageddon build to work properly.

[Anaconda](https://anaconda.org/)
