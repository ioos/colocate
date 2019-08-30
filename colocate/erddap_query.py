from erddapy import ERDDAP
from erddapy import utilities

import sys
import json
import requests
import pandas as pd
import urllib3
import random

# some configuration:
headers = {'User-agent': '{}-{}'.format((requests.__version__), "erddap-colocate-ohw19")}

def query(url, **kw):
    ds = pd.DataFrame()

    # we need to rstrip to prevent a '//' in the URL for some reason:
    url = url.rstrip("/")
    e = ERDDAP(
             server=url,
             protocol='tabledap',
             response='csv'
             )

    # submit the query:
    try:
        r = requests.get(e.get_search_url(**kw), headers=headers)
        r.raise_for_status()
        print(e.get_search_url(**kw))

        ds = pd.read_csv("{}".format(e.get_search_url(**kw)))
        ds['server'] = url
        ds.dropna(subset=['tabledap'],inplace=True)
        #print(ds.head())

        return ds[['server','Dataset ID','tabledap','Institution','Summary']]

        # this is for the data query part.... hold:
        #ds = e.to_pandas()
        #return ds

    except requests.exceptions.RequestException as ex:
        print("Bad ERDDAP!!! {}".format(url))
        #print(e.get_search_url(**kw))
        print("Encountered: requests.exceptions.RequestException")
    except requests.exceptions.ConnectTimeout as ex:
        print("Bad ERDDAP!!! {}".format(url))
        #print(e.get_search_url(**kw))
        print("Encountered: requests.exceptions.ConnectTimeout")
    except requests.exceptions.ConnectionError as ex:
        print("Bad ERDDAP!!! {}".format(url))
        #print(e.get_search_url(**kw))
        print("Encountered: requests.exceptions.ConnectTimeout")
    except urllib3.exceptions.NewConnectionError as ex:
        print("Bad ERDDAP!!! {}".format(url))
        #print(e.get_search_url(**kw))
        print("Encountered: requests.exceptions.ConnectTimeout")

    return None

    '''
        except requests.exceptions.HTTPError as e:
            print("Bad ERDDAP!!! {}".format(url))
        except requests.exceptions.SSLError as e:
            print("Bad ERDDAP!!! {}".format(url))
        except OpenSSL.SSL.Error as e:
            print("Bad ERDDAP!!! {}".format(url))
        except ssl.SSLError as e:
            print("Bad ERDDAP!!! {}".format(url))
        except urllib3.exceptions.MaxRetryError as e:
            print("Bad ERDDAP!!! {}".format(url))
    '''

def get_coordinates(ds, kw):
    '''
    ds = pd.DataFrame(columns=['server','Dataset ID',...])

    kw = {'search_for': 'all',
     'min_lon': -123.628173,
     'max_lon': -122.02382599999999,
     'min_lat': 47.25972200000001,
     'max_lat': 48.32253399999999,
     'min_time': '2018-01-27T00:00:00Z',
     'max_time': '2019-12-31T00:00:00Z'}
    '''
    # pick a couple random datasets
    if ds.shape[0] > 9:
        print("Found %i datasets. Reducing return to 10." % ds.shape[0])
        ds = ds.iloc[random.sample(range(0,ds.shape[0]),10)]
    df_coords = pd.DataFrame()
    all_datasets = ds
    for i in range(all_datasets.shape[0]):
        server_url = all_datasets['server'].iloc[int(i)]
        dataset_id = all_datasets['Dataset ID'].iloc[int(i)]

        if "ROMS" in dataset_id or "DOP" in dataset_id: # skip ROMS model output
            #print("Skipping %s" % server_url + dataset_id)
            continue
        #if dataset_id in df_coords['Dataset ID']:
        #    continue
        #print(i)
        e = ERDDAP(
                     server=server_url,
                     protocol='tabledap',
                     response='csv'
               )
        try:
            e.variables=["latitude","longitude"]#,"time"]
            e.dataset_id = all_datasets['Dataset ID'].iloc[int(i)]
            e.constraints = {
                   "time>=": kw['min_time'],
                   "time<=": kw['max_time'],
                   "longitude>=": kw['min_lon'],
                   "longitude<=": kw['max_lon'],
                   "latitude>=": kw['min_lat'],
                   "latitude<=": kw['max_lat'],
                   "distinct" : ()
            }


            r = requests.get(e.get_download_url())
            r.raise_for_status()
            #print(e2.get_download_url())
            df = e.to_pandas()
            #print("Found %i unique coordinates." % df.shape[0])
            df['dataset_count'] = i
            df['dataset_download_url'] = e.get_download_url()
            df['Dataset ID'] = dataset_id

            df_coords = pd.concat([df_coords,df])
        except:
            pass
        #print(e.get_download_url(response="csv"))

        #dataset_url = '%s/tabledap/%s.csvp?latitude,longitude,time&longitude>=-72.0&longitude<=-69&latitude>=38&latitude<=41&time>=1278720000.0&time<=1470787200.0&distinct()' % (all_datasets['server'].iloc[int(i)],all_datasets['Dataset ID'].iloc[int(i)])

    return df_coords
