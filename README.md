Project-Co_locators
=======================


###Run ERDDAP colocate in Binder!
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/oceanhackweek/ohw19-project-co_locators/master?filepath=colocate.ipynb)

### Collaborators on this project
Mathew Biddle <br />
Hannah Blondin <br />
Sophie Chu <br />
Yeray Santana Falcon <br />
Molly James <br />
Pedro Magaña <br />
Jazlyn Natalie <br />
Laura Gomez Navarro  <br />
Will Oestreich <br />
Shikhar Rai  <br />
Micah Wengren <br />

### The problem
Co-locate oceanographic data by establishing constraints.

### Application example
A user is interested in all the available oceanographic data in a region where an eddy just formed. They provide the geospatial bounds of the region and a temporal range and get an aggregated response of all available data.

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
  - [Pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/overview.html)?
- ?

### Background reading

Optional: links to manuscripts or technical documents for more in-depth analysis.
