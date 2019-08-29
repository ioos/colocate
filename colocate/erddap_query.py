from erddapy import ERDDAP
from erddapy import utilities

import json
import requests
import pandas as pd


def query(url, **kw):

    # submit the query:
    r = requests.get(url)
    ds = pd.DataFrame()

    try:
        r.raise_for_status()
        e = ERDDAP(
                 server=url,
                 protocol='tabledap',
                 response='csv'
           )
        print(e.get_search_url(kw))
        ds = e.to_pandas()

        print(ds.head())
        return ds

        #datasets = ds[['server','Dataset ID','tabledap']]
        #datasets.dropna(subset=['tabledap'],inplace=True)
        #all_datasets = pd.concat([all_datasets,datasets])

    except requests.exceptions.RequestException as e:
        print("Bad ERDDAP!!! {}".format(url))
    except requests.exceptions.ConnectTimeout as e:
        print("Bad ERDDAP!!! {}".format(url))
    except requests.exceptions.ConnectionError as e:
        print("Bad ERDDAP!!! {}".format(url))
    except requests.exceptions.NewConnectionError as e:
        print("Bad ERDDAP!!! {}".format(url))
    except requests.exceptions.HTTPError as e:
        print("Bad ERDDAP!!! {}".format(url))
    except requests.exceptions.SSLError as e:
        print("Bad ERDDAP!!! {}".format(url))




    return None
