from erddapy import ERDDAP
from erddapy import utilities

import sys
import json
import requests
import pandas as pd
import urllib
import urllib3
import random

# some configuration:
headers = {'User-agent': '{}-{}'.format((requests.__version__), "erddap-colocate-ohw19"),
        'From': 'noreply@oceanhackweek.github.io'}
#headers = {'From': 'noreply@oceanhackweek.github.io'}

def query(url, **kw):
    df = pd.DataFrame()

    # we need to rstrip to prevent a '//' in the URL for some reason:
    url = url.rstrip("/")
    e = ERDDAP(
             server=url,
             protocol='tabledap',
             response='csv'
             )

    # submit the query:
    try:
        # this is redundant to ERDDAPY API query below:
        #r = requests.get(e.get_search_url(**kw), headers=headers)
        #r.raise_for_status()
        print("Testing ERDDAP {}".format(url))
        df = pd.read_csv("{}".format(e.get_search_url(**kw), headers=headers))
        print("ERDDAP {} returned results from URL: {}".format(url, e.get_search_url(**kw)))
        df['server'] = url
        df.dropna(subset=['tabledap'],inplace=True)

        return df[['server','Dataset ID','tabledap','Institution','Summary']]
    except Exception as ex:
        # can happen if the dataset does not have any features within the query window, just log it here:
        if type(ex).__name__ in ["HTTPError"]:
            print(ex)
            #raise
        pass

#     except urllib.error.HTTPError as ex:
#         #print("Bad ERDDAP!!! {}, exception encountered: {}".format(url, type(ex).__name__))
#         pass
#     except urllib3.exceptions.NewConnectionError as ex:
#         #print("Bad ERDDAP!!! {}, exception encountered: {}".format(url, type(ex).__name__))
#         pass
#     except requests.exceptions.ConnectionError as ex:
#         #print("Bad ERDDAP!!! {}, exception encountered: {}".format(url, type(ex).__name__))
#         pass
#     except requests.exceptions.ConnectTimeout as ex:
#         #print("Bad ERDDAP!!! {}, exception encountered: {}".format(url, type(ex).__name__))
#         pass
#     except requests.exceptions.RequestException as ex:
#         #print("Bad ERDDAP!!! {}, exception encountered: {}".format(url, type(ex).__name__))
#         pass
#     except requests.exceptions.URLError as ex:
#         #print("Bad ERDDAP!!! {}, exception encountered: {}".format(url, type(ex).__name__))
#         pass
    return None


def get_coordinates(df, **kw):
    '''
    df = pd.DataFrame(columns=['server','Dataset ID',...])

    kw = {
     'min_lon': -123.628173,
     'max_lon': -122.02382599999999,
     'min_lat': 47.25972200000001,
     'max_lat': 48.32253399999999,
     'min_time': '2018-01-27T00:00:00Z',
     'max_time': '2019-12-31T00:00:00Z'}

     dataset_url = '%s/tabledap/%s.csvp?latitude,longitude,time&longitude>=-72.0&longitude<=-69&latitude>=38&latitude<=41&time>=1278720000.0&time<=1470787200.0&distinct()' % (all_datasets['server'].iloc[int(i)],all_datasets['Dataset ID'].iloc[int(i)])
    '''
    df_coords = pd.DataFrame()

    # pick 10 random datasets from our search results:
    #count = 10
    #if df.shape[0] > count:
    #    print("Found %i datasets. Reducing return to %i." % (df.shape[0],count))
    #    subset_datasets = df.iloc[random.sample(range(0,df.shape[0]),count+1)]
    #else:
    #    subset_datasets = df
    #    final_dataset_limit = df.shape[0]


    # alternate approach to above is iterate the original DataFrame passed (df), stopping either
    #   at final_dataset_limit (10 currently) or the max # of rows in df (conclusion of for loop)
    #   previous enclosing while loop is unnecessary as a result
    final_dataset_limit = 10
    datasets_found = 0
    if df.shape[0] < final_dataset_limit:
        final_dataset_limit = df.shape[0]

    index_random = random.sample(range(0,df.shape[0]),df.shape[0])
    print("index_random: {}".format(index_random))

    #for i in range(subset_datasets.shape[0]):
    for i in index_random:
        server_url = df['server'].iloc[int(i)]
        dataset_id = df['Dataset ID'].iloc[int(i)]
        institution = df['Institution'].iloc[int(i)]

        # skip some difficult datasets for now:
        if "ROMS" in dataset_id or "DOP" in dataset_id: # skip ROMS model output
            #print("Skipping %s" % server_url + dataset_id)
            continue

        e = ERDDAP(
                server=server_url,
                protocol='tabledap',
                response='csv'
                )
        try:
            print("datasets_found: {}".format(datasets_found))
            # former config for query, replaced with new code below:
            #e.variables=["latitude","longitude"]#,"time"]
            #e.dataset_id = all_datasets['Dataset ID'].iloc[int(i)]
            #e.constraints = {
            #       "time>=": kw['min_time'],
            #       "time<=": kw['max_time'],
            #       "longitude>=": kw['min_lon'],
            #       "longitude<=": kw['max_lon'],
            #       "latitude>=": kw['min_lat'],
            #       "latitude<=": kw['max_lat'],
            #       "distinct" : ()
            #}

            # Generate a download URL via e.get_download_url and pass to Pandas DataFrame via read_csv
            #   we need to use e.constraints here rather than in e.get_download_url to allow appending '>=' '<=' to the contstraints keys to match ERDDAP's API
            #   (parameter signature differs from the search API used above)
            # also add a 'distinct = ()' param, generate a download url, and submit a csv dataset download request to ERDDAP
            #kw["distinct"] = "()"
            e.constraints = {
                   "time>=": kw['min_time'],
                   "time<=": kw['max_time'],
                   "longitude>=": kw['min_lon'],
                   "longitude<=": kw['max_lon'],
                   "latitude>=": kw['min_lat'],
                   "latitude<=": kw['max_lat'],
                   "distinct" : ()
            }
            url = e.get_download_url(
                    #constraints=kw,
                    response="csvp",
                    dataset_id=df['Dataset ID'].iloc[int(i)],
                    variables=["latitude","longitude"]
                    )
            print("Download URL: {}".format(url))

            #coords = pd.read_csv(url, headers=headers)
            coords = pd.read_csv(url)
            coords['dataset_count'] = i
            coords['dataset_download_url'] = url
            coords['Dataset ID'] = dataset_id
            coords['Institution'] = institution

            #get_var_by_attr example (ToDo):
            #e.get_var_by_attr(dataset_id, standard_name='northward_sea_water_velocity')

            print(coords.head())
            df_coords = pd.concat([df_coords,coords])

            # reaching this point in the query means the dataset query was successful, increment
            #   we need to break out of for loop here however if we reach final_dataset_limit to not go over:
            datasets_found += 1
            print("new dataset acquired; datasets_found: {}".format(datasets_found))
            # not needed:
            #df.drop([i])
            if datasets_found == final_dataset_limit: break

        except Exception as ex:
            # can happen if the dataset does not have any features within the query window, just log it here:
            if type(ex).__name__ in ["HTTPError"]:
                print(ex)
            #raise
            pass

    return df_coords
