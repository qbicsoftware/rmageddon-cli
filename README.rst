Rmageddon
##############

.. image:: https://travis-ci.org/qbicsoftware/r-lint-cli.svg?branch=master
    :target: https://travis-ci.org/qbicsoftware/r-lint-cli

.. image:: https://codecov.io/gh/qbicsoftware/r-lint-cli/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/qbicsoftware/r-lint-cli

A small linting and building command line tool for reproducible R analysis with Docker at QBiC.

Motivation
####

Performing a reproducible analysis with R and share the environment status of an R installation with the 
necessary packages and all that with the correct version is a very challenging task.

In order to face this issue, under the umbrella of better reproducibility of computational results, we created
`Rmageddon`, a small command-line tool, that assists in the build of Docker container with specified version of R and
a dedicated, version-defined package installation. Moreover, Rmageddon provides cookiecutter templates for the easy creation of docker environments for your R analysis.

The container collection is hosted on a different GitHub repository: [R-container-lib](https://github.com/qbicsoftware/r-container-lib) .All containers there passed the linting and have been build with Rmageddon.

The complete workflow for the creation of a new container for your R-analysis is depicted in the following image: 
    
![Rmageddon_workflow](https://user-images.githubusercontent.com/21954664/53096328-2acf5580-351f-11e9-898a-1b8ce790afee.png)

This README will guide you through the complete process of starting with the sessioninfo of your R-analysis and finally sharing your docker powered R-environment on our [R-container-lib](https://github.com/qbicsoftware/r-container-lib).

1. Create a sessioninfo from your R-analysis. The official R-documentation explains this process well: [Sessioninfo](https://www.rdocumentation.org/packages/utils/versions/3.5.2/topics/sessionInfo).
2. Install Rmageddon. This is explained in the documentation for Rmageddon: [Rmageddon documentation](doc/Rmageddon.md)
3. Run Rmageddon build on your sessioninfo. This is again explained in the documentation for Rmageddon: [r-lint documentation](doc/Rmageddon.md), especially in the build subcommand section.
4. Create a docker environment using the cookiecutter template. This process is described in the documentation for the Rmageddon-cookiecutter [Rmageddon-cookiecutter documentation](doc/Rmageddon-cookiecutter.md)
5. Copy the generated environment.yml content into the environment.yml of your just created R-container 
6. Add your R-scripts that you used for your analysis to your just created R-container 
7. Validate your just created R-container: Run Rmageddon lint on it. Please refer to the documentation for Rmageddon: [Rmageddon documentation](doc/Rmageddon.md), especially in the lint subcommand section.
8. If validation was successful your R-container is now ready to be added to our R-container library. Please refer to the final documentation of the [R-container-lib](https://github.com/qbicsoftware/r-container-lib).
9. Enjoy!

