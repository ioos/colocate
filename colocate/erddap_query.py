from erddapy import ERDDAP
from erddapy import utilities

import sys
import json
import requests
import pandas as pd
import urllib3

def query(url, **kw):

    ds = pd.DataFrame()

    # some configuration:
    #config = {'verbose': sys.stderr}
    headers = {'User-agent': '{}-{}'.format((requests.__version__), "erddap-colocate")}
    print(headers)

    # submit the query:
    try:
        print("In the try...")
        #r = requests.get(url,  headers=headers)
        #r.raise_for_status()
        print("In the try 2...")
        e = ERDDAP(
                 server=url,
                 protocol='tabledap',
                 response='csv'
           )
        print(e.get_search_url(kw))
        print("In the try 3...")
        ds = e.to_pandas()
        print("In the try 4...")
        print(ds.head())
        return ds

        #datasets = ds[['server','Dataset ID','tabledap']]
        #datasets.dropna(subset=['tabledap'],inplace=True)
        #all_datasets = pd.concat([all_datasets,datasets])

    except requests.exceptions.RequestException as e:
        print("Bad ERDDAP!!! {}".format(url))
        print("Encountered: requests.exceptions.RequestException")
    except requests.exceptions.ConnectTimeout as e:
        print("Bad ERDDAP!!! {}".format(url))
        print("Encountered: requests.exceptions.ConnectTimeout")
    except requests.exceptions.ConnectionError as e:
        print("Bad ERDDAP!!! {}".format(url))
        print("Encountered: requests.exceptions.ConnectTimeout")
    except urllib3.exceptions.NewConnectionError as e:
        print("Bad ERDDAP!!! {}".format(url))
        print("Encountered: requests.exceptions.ConnectTimeout")

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


    return None
