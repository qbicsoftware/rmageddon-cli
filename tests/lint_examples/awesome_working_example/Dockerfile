FROM continuumio/miniconda

LABEL name="qtest-ranalysis"
LABEL authors="{{ cookiecutter.author_name }}"
LABEL organization="Quantitative Biology Center"
LABEL description="{{ cookiecutter.description }}"
LABEL maintainer="{{ cookiecutter.author_name }}" < "{{ cookiecutter.author_email }}">  
LABEL version="1.0.0"
LABEL github="https://github.com/qbicsoftware"

# Install procps so that Nextflow can poll CPU usage
RUN apt-get update && apt-get install -y procps && apt-get clean -y 
# Update the base version of conda
RUN conda update -n base conda
# Copy the list of R packages into the container's /tmp dir
COPY environment.yml /tmp
RUN conda update -n base conda && \
    conda env create -f /tmp/environment.yml && \
    conda clean -a

ENV PATH /opt/conda/envs/qbicsoftware-{{ cookiecutter.project_code }}-ranalyses-{{ cookiecutter.container_version }}/bin:$PATH

