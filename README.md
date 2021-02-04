# Project Co-Locators


## Preview/Run:

#### ERDDAP colocate.ipynb:
[![binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ioos/colocate/master?filepath=notebooks%2Fcolocate.ipynb)
[![nbviewer](https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.svg)](https://nbviewer.jupyter.org/github/ioos/colocate/blob/master/notebooks/colocate.ipynb)

#### ERDDAP colocate-dev.ipyb:
[![binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ioos/colocate/master?filepath=notebooks%2Fcolocate-dev.ipynb)
[![nbviewer](https://raw.githubusercontent.com/jupyter/design/master/logos/Badges/nbviewer_badge.svg)](https://nbviewer.jupyter.org/github/ioos/colocate/blob/master/notebooks/colocate-dev.ipynb)


## Installation:

### Install with conda:
```
git clone https://github.com/ioos/colocate.git
cd colocate
conda env create -f environment.yml
conda activate colocate
```

### Run via command line:
```
erddap-co-locate
```

### Run in Jupyter notebook:
```
jupyter notebook &
```

### Run in JupyterLab:

This step may be necessary for ipyleaflet and HoloViz to run correctly in JupyterLab.  Run the following on the command line with the 'colocate' conda environment active:
```
jupyter labextension install @jupyter-widgets/jupyterlab-manager
jupyter labextension install jupyter-leaflet
jupyter labextension install @pyviz/jupyterlab_pyviz
```
Then, start JupyterLab:
```
jupyter-lab &
```

### Run with voila:
```
voila colocate.ipynb --enable_nbextensions=True --VoilaConfiguration.file_whitelist="['.*']"
```

## Local Development:
If you want to develop locally, clone from GitHub, `cd` to the cloned repository root directory, and run `pip install` as follows:
```
git clone https://github.com/ioos/colocate.git
cd colocate
pip install -e . --no-deps --force-reinstall
```


# OceanHackWeek 2019 'co-locators' Project
Description of the original OceanHackWeek 2019 project that led to the development of this module.  

## The problem
Co-locate oceanographic data (served via ERDDAP) by establishing constraints to use as data server query filters.  

Submit the identical filter criteria to all ERDDAP servers indexed by the [awesome-erddap project](https://github.com/IrishMarineInstitute/awesome-erddap) and visualize the results.

### Application example
A user is interested in all the available oceanographic data in a region where an eddy just formed. They provide the geospatial bounds of the region and a temporal range and get an aggregated response of all available data.

## Collaborators:

| Name | Year |
|------------|----|
|Mathew Biddle|2019|
|Sophie Chu|2019|
|Yeray Santana Falcon|2019|
|Molly James|2019|
|Pedro Magaña|2019|
|Jazlyn Natalie|2019|
|Laura Gomez Navarro|2019|
|Shikhar Rai|2019|
|Micah Wengren|2019|
|Jacqueline Tay|2020|
|Mike Morley|2020|
|Yuta Norden|2020|


### Specific tasks
- [x] Collect temporal bounds.
- [x] Collect spatial bounds.
- [x] _Collect keywords?_
- [x] Build query url.
- [x] Do the search.
- [ ] Evaluate the response.
- [ ] Manage response.
- [ ] Geospatial plotting.
- [ ] Temporal plotting.
- [ ] Link back to dataset on erddap server.
- [ ] _Aggregated download?_


### Existing methods
- The Irish Marine Institute has developed a [keyword search across existing ERDDAP
  servers](https://github.com/IrishMarineInstitute/search-erddaps)
  - [Here is the list of all ERDDAP's they use.](https://github.com/IrishMarineInstitute/search-erddaps/blob/master/erddaps.json)
- OHW18 built a [search interface for one ERDDAP server](https://github.com/oceanhackweek/ohw18_erddap-explorer)
- yodapy: https://github.com/cormorack/yodapy


### Proposed methods/tools
- Jupyter
- Python
  - [erddapy](https://github.com/ioos/erddapy)
  - [Pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/overview.html)

### Background reading

Optional: links to manuscripts or technical documents for more in-depth analysis.
