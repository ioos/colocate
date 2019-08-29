import argparse
import json
import requests
import pandas as pd

from .erddap_query import query

def main():
    """
    Entrypoint
    """
    servers = None


    # download master ERDDAP server list:
    try:
        #servers = json.loads(requests.get('https://raw.githubusercontent.com/IrishMarineInstitute/search-erddaps/master/erddaps.json').text)
        servers = json.loads(requests.get('https://raw.githubusercontent.com/IrishMarineInstitute/awesome-erddap/master/erddaps.json').text)
        print(servers)
    except Exception as e:
        return None

    for server in servers:
        print("name: {}\nurl: {}\npublic: {}".format(server['name'], server['url'], server['public']))

    # define parameters (placeholder)
    time_min = '2010-07-10T00:00:00Z'
    time_max = '2016-08-10T00:00:00Z'
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

    print("\n\n********Run ERDDAP Advanced Serach via erddapy to find datasets***********")
    for server in servers[0:1]:
        print("url: {}".format(server['url']))

        ds = query(server['url'], **kw)

        #datasets = ds[['server','Dataset ID','tabledap']]
        #datasets.dropna(subset=['tabledap'],inplace=True)
        all_datasets = pd.concat([all_datasets,ds])


        print(all_datasets)
    return all_datasets
