import pandas as pd
import hvplot.pandas
import cmocean as cmo
import datashader as ds
import cartopy.crs as ccrs
#import matplotlib.pyplot as plt
import geoviews as gv
import holoviews as hv
#df_coords = pd.read_csv(‘/Users/santanay/code/OHW19/ohw19-project-co_locators/coordinates.zip’, index_col=0)
import cartopy.io.shapereader as shpreader


def plot(df_coords):
    shpfilename = shpreader.natural_earth(resolution='10m',
                                        category='physical',
                                        name='coastline')
    figure = df_coords.hvplot.scatter(
       'longitude (degrees_east)','latitude (degrees_north)', s=5, c='Dataset ID',
       projection=ccrs.PlateCarree(),
       width=600, height=540, cmap=cmo.cm.tempo,
       datashade=True
    ) * gv.Shape.from_shapefile(shpfilename, crs=ccrs.PlateCarree())

    return figure
