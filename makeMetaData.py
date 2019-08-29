import ipywidgets as widgets
from erddapy import ERDDAP
from erddapy import utilities
import numpy as np

import json
import urllib
import requests
import pandas as pd


from classes import *


def initMetadata():
    file = urllib.request.urlopen(
        'https://raw.githubusercontent.com/IrishMarineInstitute/search-erddaps/master/erddaps.json')
    serversURL = json.loads(file.read())
    
    scount = 0
    urlList = []

    for key in serversURL:
        url = key['url']
        url = url.rstrip("/")
        #print(type(url))
        urlList.append(url)
    
    servers = []

    for i in range(len(urlList)):
        servers.append(serverClass(urlList[i]))
    
    metaData= MetaDataClass(servers)
    return metaData

def update_tableGridWms_Info(metaData):
    for server_count in range(len(metaData.servers)):
        server = metaData.servers[server_count]
        url = server.url
        df = pd.DataFrame()
        tableNum = 0
        gridNum = 0
        wmsNum = 0
        try:
            e = ERDDAP(server=url)
            ### csv to pandas dataset for all datasets
            df = pd.read_csv(e.get_search_url(response='csv', search_for='all'))
            ### printing number of datasets
            tableNum = len(set(df["tabledap"].dropna()))
            gridNUM = len(set(df["griddap"].dropna()))
            wmsNum = len(set(df["wms"].dropna()))
            noerr = True
        except:  # requests.exceptions.RequestException as err:
            noerr = False

        if noerr:
            server.Err = False
            server.set_num_TableGridWms(tableNum, gridNum, wmsNum)
        
        metaData.servers[server_count] = server

    return metaData
    

def fill_info_in_meta_acc_to_constrains(metaData,kw):
    for server_count in range(len(metaData.servers)):
        server = metaData.servers[server_count]
        df = pd.DataFrame()
        try:
            #r.raise_for_status()
            e = ERDDAP(
                server=server.url,
                response='csv'
            )
            df = pd.read_csv(e.get_search_url(response='csv', **kw))
            noerr = True
        except:  # requests.exceptions.RequestException as err:
            noerr = False
        if df.empty != True:
            dataset_ids = df.loc[~df['tabledap'].isnull(),
                                 'Dataset ID'].tolist()
            for count in range(len(dataset_ids)):
                dataset_ID = dataset_ids[count]
                dataset_toAdd = dataSetsClass()
                dataset_toAdd.set_ID(dataset_ID)
                dataset_toAdd.set_datasetType('tabledap')
                #print(dataset_ids)
                server.addDatasets(dataset_toAdd)

        metaData.servers[server_count] = server

    return metaData

###################################################


def fill_lat_lonValue_to_AllDataset(metaData,kw, constraints):
    for server_count in range(len(metaData.servers)):
        server = metaData.servers[server_count]
        df = pd.DataFrame()
        elist = []
        noerr = False
        try:
            #r.raise_for_status()
            e = ERDDAP(
                server=server.url,
                response='csv'
            )
            df = pd.read_csv(e.get_search_url(response='csv', **kw))
            elist.append(e)
            noerr = True
        except:  # requests.exceptions.RequestException as err:
            noerr = False

        if noerr:
            datasets_To_remove = []
            for dataset_count in range(len(server.datasets)):
                dataset = server.datasets[dataset_count]
                if dataset.datasetType == 'tabledap':
                    e2 = elist[0]
                    e2.dataset_id = dataset.dataset_ID
                    e2.protocol = "tabledap"
                    e2.constraints = {
                        "time>=": constraints.time_min,
                        "time<=": constraints.time_max,
                        "longitude>=": constraints.lon_min,
                        "longitude<=": constraints.lon_max,
                        "latitude>=": constraints.lat_min,
                        "latitude<=": constraints.lat_max,
                        "distinct" : ()
                    }
                    e2.variables = [
                        'latitude',
                        'longitude',
                    ] 
                    try:
                        download_url = e2.get_download_url()
                        df = e2.to_pandas().dropna()
                        dataset.lon = df["longitude (degrees_east)"]
                        dataset.lat = df["latitude (degrees_north)"]
                    except:
#                         print('could not get lon lat for dataset '+ \
#                             dataset.dataset_ID + ' in server ' + server.url)
                        datasets_To_remove.append(dataset)
                else:
                    print('dataset '+ dataset.dataset_ID + ' in server ' + server.url + \
                            ' not tabledap')
                
                server.datasets[dataset_count] = dataset
            for i in range(len(datasets_To_remove)):
                #print(type(datasets_To_remove[i]))
                server.removeDatasets(datasets_To_remove[i])
        else:
            'Server error. This should have been resolved. Check code'
        
        metaData.servers[server_count] = server
    
    return metaData


def fill_lat_lonValue_to_Dataset(server, dataset, kw, constraints):
        df = pd.DataFrame()
        elist = []
        try:
            #r.raise_for_status()
            e = ERDDAP(
                server=server.url,
                response='csv'
            )
            df = pd.read_csv(e.get_search_url(response='csv', **kw))
            elist.append(e)
            noerr = True
        except:  # requests.exceptions.RequestException as err:
            noerr = False

        if noerr:
            isInServer = False
            for dataset_count in range(len(server.datasets)):
                if server.datasets[dataset_count].dataset_ID == dataset.dataset_ID:
                    isInServer = True
                    break
                    
            if isInServer:    
                dataset = server.datasets[dataset_count]
                if dataset.datasetType == 'tabledap':
                    e2 = elist[0]
                    e2.dataset_id = dataset.dataset_ID
                    e2.protocol = "tabledap"
                    e2.constraints = {
                        "time>=": constraints.time_min,
                        "time<=": constraints.time_max,
                        "longitude>=": constraints.lon_min,
                        "longitude<=": constraints.lon_max,
                        "latitude>=": constraints.lat_min,
                        "latitude<=": constraints.lat_max
                    }
                    e2.variables = [
                        'latitude',
                        'longitude'
                    ]      
                    try:
                        download_url = e2.get_download_url()
                        df = e2.to_pandas().dropna()
                        dataset.lon = df["longitude (degrees_east)"]
                        dataset.lat = df["latitude (degrees_north)"]
                    except:
                        print('could not get lon lat for dataset ' + \
                            dataset.dataset_ID + ' in server ' + server.url)
                else:
                    print('dataset '+ \
                            dataset.dataset_ID + ' in server ' + server.url + \
                            ' not tabledap')
                
                server.datasets[dataset_count] = dataset
            else:
                print('DATASET NOT IN SERVER')
        else:
            'Server error. This should have been resolved. Check code'
    
        return server.datasets[dataset_count]









