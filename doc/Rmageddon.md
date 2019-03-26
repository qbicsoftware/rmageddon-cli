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

Once you have installed Rmageddon, just call it with the ``--help`` option to get an overview of the subcommands
available in Rmageddon:

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
                                                                                 
                                                  
    2019, QBiC software, Sven Fillinger
    sven.fillinger@qbic.uni-tuebingen.de
        
    Usage: rmageddon [OPTIONS] COMMAND [ARGS]...

    Options:
    --version      Show the version and exit.
    -v, --verbose  Verbose output (print debug statements)
    --help         Show this message and exit.

    Commands:
    build  Resolve R packages resources from Anaconda...
    lint   Check R project against linting guidelines
    validate Performs a diff on two R-analysis output files
```


If you want to know the positional arguments and options of each subcommand, just type ``rmageddon build --help`` or 
``rmageddon lint --help``.


The subcommand <b>build</b>
----------------------

The subcommand ``build`` is a small helper tool, that is able to parse ``sessionInfo`` output from R and extract the package names with versions.

It then takes these and checks on [Anaconda Cloud](https://anaconda.org/) if these are available in one of the pre-defined channels `[default, r, bioconda]`. If successful, it will automatically add the corresponding conda package with version in the `environment.yml`. If a package cannot be found, a warning is printed on the command-line.
If a specified version of a package is not found, it prints the available versions on the command-line.    
**In case you are using anaconda** you can export your current build using:
```bash
conda env export > environment.yml
```
**If you are not using anaconda** you have to provide an environment.yml file created by [Rmageddon-cookiecutter](doc/Rmageddon-cookiecutter.md). It has to look remotely similar to this:    
```bash
name: QABCD000_basic_ranalysis0.1.0    
channels:    
  - bioconda    
  - r    
  - defaults    
dependencies:    
  - r-base=3.2.4    
```


To start the build, be sure you have an active internet connection and run it with:

```bash 
    $ rmageddon build <sessioninfo file> environment.yml
```

The ``R package list`` can be obtained from inside your active R session, that was used to run your R analysis successfully. From within your R console, just type:

```R

    > sessionInfo()$otherPkgs
```
where $otherPkgs is an **optional** character vector of other attached packages.
If you need any additional information about the ``sessioninfo`` command you can refer to [Sessioninfo Doc](https://www.rdocumentation.org/packages/utils/versions/3.5.3/topics/sessionInfo).          
This is your R package list or commonly refered to 'sessioninfo file', which is needed for Rmageddon build.


The subcommand <b>lint</b>
---------------------

The subcommand <lint> is actually checking an R container project against some specified rule-set. Currently, *Rmageddon* is assuming the following project structure:
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

The subcommand <b>validate</b>
---------------------
The subcommand <validate> is validating two R-analysis output files. For now it performs a diff of the two files and displays any differing lines.
```bash
 $ rmageddon validate /path/to/R-analysis-file-one /path/to/R-analysis-file-two
```    
