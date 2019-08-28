from IPython.display import clear_output
from array import array
#from more_intertools import interleave
import ipywidgets as widgets
from erddapy import ERDDAP
from erddapy import utilities
import numpy as np

import json
import urllib
import requests
import pandas as pd

def getVars(kw):
    file = urllib.request.urlopen(
        'https://raw.githubusercontent.com/IrishMarineInstitute/search-erddaps/master/erddaps.json')
    servers = json.loads(file.read())
    file.getcode()
    #servers=servers[:3]


    all_datasets = pd.DataFrame()
    scount = 0

    for key in servers:
        scount += 1
        d = widgets.FloatProgress(
            value=scount,
            min=0,
            max=len(servers),
            step=1,
            description='Loading:',
            bar_style='info',
            orientation='horizontal'
        )
        display(d)
        noerr = True
        url = key['url']
        url = url.rstrip("/")
        #r = requests.get(url)
        try:
            #r.raise_for_status()
            e = ERDDAP(
                server=url,
                protocol='tabledap',
                response='csv'
            )
            print(e.get_search_url(**kw))
            #noerr = True
        except requests.exceptions.RequestException as err:
            #print("Bad ERDDAP!!! Req Err{}".format(url))
            noerr = False
        except requests.exceptions.HTTPError as errh:
            #print("Bad ERDDAP!!! HTTP err {}".format(url))
            noerr = False
        except requests.exceptions.ConnectionError as errc:
            #print("Bad ERDDAP!!! Con err {}".format(url))
            noerr = False
        except requests.exceptions.Timeout as errt:
            #print("Bad ERDDAP!!! TimeOut err {}".format(url))
            noerr = False
#         except requests.exceptions.HTTPSConnectionPool as errF:
#             noerr = False

        if noerr:
            #pass
              datasets = pd.read_csv(e.get_search_url(response='csv', search_for='all')
                                   )  # pd.read_csv('%s'%e.get_search_url(**kw))
              datasets['server'] = url
#             all_datasets = pd.concat([all_datasets, datasets], sort=True)
        d.close()

#     tabledap = all_datasets.loc[all_datasets['tabledap'].notnull(), 'Info']
#     tabledap = all_datasets.loc[all_datasets.notnull()]#, 'Info']


#     ii = 0
#     var_list =[]
#     a =0
#     for csv_url in tabledap:
#         a += 1
#         print(a)
#         meta = pd.read_csv(str(csv_url))
#         #print(meta['Variable Name'].unique())
#         #print()
#         e = ERDDAP(
#             server=all_datasets['server'].iloc[ii],
#             protocol='tabledap')
#         e.dataset_id = all_datasets['Dataset ID'].unique()
#         e.protocol = "tabledap"
#         ii += 1
#         var_in_url = meta['Variable Name'].unique()
#         # for variable in var_in_url:
#         #     var_list.append(variable)
#         print(var_in_url)
        
#     #varlist = array(var_in_url)
#     varlist = var_in_url()
#     return varlist

