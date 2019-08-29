import pandas as pd
from erddapy import ERDDAP
import urllib
import requests
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
        e2 = ERDDAP(
                     server=server_url,
                     protocol='tabledap',
                     response='csv'
               )
        e2.variables=["latitude","longitude"]#,"time"]
        e2.dataset_id = all_datasets['Dataset ID'].iloc[int(i)]
        #e2.constraints = kw
        e2.constraints = {
               "time>=": kw['min_time'],
               "time<=": kw['max_time'],
               "longitude>=": kw['min_lon'],
               "longitude<=": kw['max_lon'],
               "latitude>=": kw['min_lat'],
               "latitude<=": kw['max_lat'],
               "distinct" : ()
        }
        r = requests.get(e2.get_download_url())
        try:
            r.raise_for_status()
            #print(e2.get_download_url())
            df = e2.to_pandas()
            #print("Found %i unique coordinates." % df.shape[0])
            df['dataset_count'] = i
            df['dataset_download_url'] = e2.get_download_url()
            df['Dataset ID'] = dataset_id

            df_coords = pd.concat([df_coords,df])
        except:
            pass
            #requests.exceptions.HTTPError as err:
            #print("HTTPError data not within bounds!!! {}".format(e2.get_download_url()))
    #     except requests.exceptions.RequestException as err:
    #         #print("RequestException data not within bounds!!! {}".format(e2.get_download_url()))
    #     except requests.exceptions.ConnectionError as err:
    #         #print("ConnectionError data not within bounds!!! {}".format(e2.get_download_url()))
    #     except requests.exceptions.Timeout as err:
    #         #print("Timeout data not within bounds!!! {}".format(e2.get_download_url()))
    #     except requests.exceptions.ConnectTimeout as err:
    #         #print("ConnectionTimeout data not within bounds!!! {}".format(e2.get_download_url()))


        #print(e.get_download_url(response="csv"))

        #dataset_url = '%s/tabledap/%s.csvp?latitude,longitude,time&longitude>=-72.0&longitude<=-69&latitude>=38&latitude<=41&time>=1278720000.0&time<=1470787200.0&distinct()' % (all_datasets['server'].iloc[int(i)],all_datasets['Dataset ID'].iloc[int(i)])

    return df_coords
#print("\n\nCollected %i unique coordinate pairs from %i datasets" % 
#      (df_coords.shape[0], len(df_coords['dataset_count'].unique())))

