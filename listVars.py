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



import matplotlib.pyplot as plt
import cartopy.crs as ccrs

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

def getGetTableDapDS_collec(kw):
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
        df = pd.DataFrame()
        erdaplist = []
        try:
            #r.raise_for_status()
            e = ERDDAP(
                server=url,
                protocol='tabledap',
                response='csv'
            )
            erdaplist.append(e)
            #print(e.get_search_url(**kw))
            df = pd.read_csv(e.get_search_url(response='csv',**kw))
            noerr = True
        except:# requests.exceptions.RequestException as err:
            noerr = False
            
        
            
        d.close()
        if df.empty != True:
            df['server'] = url
            datasets = df[['server','Dataset ID','tabledap']]
            datasets.dropna(subset=['tabledap'],inplace=True)
            all_datasets = pd.concat([all_datasets,datasets])
    
    return all_datasets
           
##### MERGING FROM HERE ####################    

def getLatLon(dataset_collec,kw):
    all_coords = pd.DataFrame()
    for dataset_count in range(len(dataset_collec)):
        error = False
        dataset = dataset_collec.iloc[dataset_count]
        e2 = ERDDAP(
            server=dataset['server'],
            protocol='tabledap',
            response='csv'
        )
        e2.variables=["latitude","longitude","time"]
        e2.dataset_id = dataset['Dataset ID']
        e2.constraints = {
           "time>=": kw['min_time'],
           "time<=": kw['max_time'],
           "longitude>=": kw['min_lon'],
           "longitude<=": kw['max_lon'],
           "latitude>=": kw['min_lat'],
           "latitude<=": kw['max_lat']
        }
        #print(e2.get_download_url())
        try:
            df = e2.to_pandas()
            df['server'] = dataset['server']
            df['Dataset ID'] = dataset['Dataset ID']            
            all_coords = pd.concat([all_coords,df])
        except:
            error = True
            
        if not error:
            print(all_coords.head())
            
    return all_coords            
       
            
            
            
            
            
            
            
            
            
            
            
##### MERGING FINISHES ####################            
            
#             dataset_ids = df.loc[~df['tabledap'].isnull(), 'Dataset ID'].tolist()
#             #print(df.head())
#             if dataset_ids:
                
#                 print(dataset_ids)
                
#                 cp_e = erdaplist[0]
                
                
#                 cp_e.dataset_id = dataset_ids[1]
#                 cp_e.protocol = "tabledap"

#                 cp_e.variables = [
#                     "latitude",
#                     "longitude",
#                     "time",
#                 ]

#                 url = cp_e.get_download_url()

#                 print('url for first Dataset',url)
                
#                 print(type(cp_e))

#                 pltData = cp_e.to_pandas()
#                 print(pltData.head())
# #                     index_col='time (UTC)',
# #                     parse_dates=True,
# #                     ).dropna()

#                 #df.head()
#                 # 
#                 # 
#                 #dx, dy = 2, 4
#                 x = pltData["longitude (degrees_east)"]
#                 y = pltData["latitude (degrees_north)"]
                
#                 print('xvals',x)
#                 print('yvals',y)

# #                 fig, ax = plt.subplots(figsize=(5, 5),
# #                        subplot_kw={"projection": ccrs.PlateCarree()}
# #                        )
# #                 cs = ax.scatter(x, y, marker='o')#c=pltData[r"sci_water_temp (\u00baC)"],
# # #                 s=50, alpha=0.5, edgecolor='none')
# # #                 cbar = fig.colorbar(cs, orientation='vertical',fraction=0.1, shrink=0.9, extend='both')
# #                 ax.coastlines('10m')
# #                 ax.set_extent([x.min()-dx, x.max()+dx, y.min()-dy, y.max()+dy])
