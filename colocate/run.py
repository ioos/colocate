import argparse
import json
import requests
import pandas as pd

from .erddap_query import query, get_coordinates

def ui_query(kw):
    servers = get_erddaps()

    all_datasets=pd.DataFrame()

    print("\n\n********Run ERDDAP Advanced Search via erddapy to find datasets***********")
    print("Total ERDDAPs: {}".format(len(servers)))

    #for server in servers[:-3]:
    #for server in servers[1:-2]:
    #for server in ( servers[1:32] + servers[34:] ):
    for server in servers[1:]:
        #print("url: {}".format(server['url']))
        ds = query(server['url'], **kw)
        all_datasets = pd.concat([all_datasets,ds])
    return all_datasets



def get_erddaps():
    """
    Query the master ERDDAP server list here: https://github.com/IrishMarineInstitute/awesome-erddap/blob/master/erddaps.js
    """
    servers = None
    # download master ERDDAP server list:
    try:
        #servers = json.loads(requests.get('https://raw.githubusercontent.com/IrishMarineInstitute/search-erddaps/master/erddaps.json').text)
        servers = json.loads(requests.get('https://raw.githubusercontent.com/IrishMarineInstitute/awesome-erddap/master/erddaps.json').text)
    except Exception as e:
        return None

    # debug:
    #print("I can haz ERDDAPs???")
    #for i, server in enumerate(servers):
    #    print("i: {}\nname: {}\nurl: {}\npublic: {}".format(i,server['name'], server['url'], server['public']))

    return servers

# may not be necessary
def api_query():
    return None

def main():
    """
    Entrypoint
    """
    servers = get_erddaps()


    # define parameters (placeholder)
    #time_min = '2019-01-01T00:00:00Z'
    time_min = '2019-07-01T00:00:00Z'
    time_max = '2019-12-31T00:00:00Z'
    bbox = [-72.0, -69, 38, 41]

    kw = {
       'search_for': 'all',
       'min_lon': bbox[0],
       'max_lon': bbox[1],
       'min_lat': bbox[2],
       'max_lat': bbox[3],
       'min_time': time_min,
       'max_time': time_max,
    }

    all_datasets=pd.DataFrame()

    print("\n\n********Run ERDDAP Advanced Search via erddapy to find datasets***********")
    print("Total ERDDAPs: {}".format(len(servers)))

    #for server in servers:
    for server in servers[1:-2]:
        #print("url: {}".format(server['url']))

        ds = query(server['url'], **kw)

        #datasets = ds[['server','Dataset ID','tabledap']]
        #datasets.dropna(subset=['tabledap'],inplace=True)
        all_datasets = pd.concat([all_datasets,ds])

    print(all_datasets.head())

    # for the get_coordinates query, we need to remove 'search_for' since it isn't valid:
    kw.pop('search_for', None)
    all_coords = get_coordinates(all_datasets, **kw)
    print(all_coords.shape)
    print(all_coords.head())


    return all_datasets, all_coords
