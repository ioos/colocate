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
    headers = {'User-agent': '{}-{}'.format((requests.__version__), "erddap-colocate")}
    #print(headers)

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
