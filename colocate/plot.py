import pandas as pd
import hvplot.pandas
import cmocean as cmo
import datashader as ds
import datashader.geo
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import geoviews as gv
import holoviews as hv
from holoviews.element.tiles import OSM
#df_coords = pd.read_csv(‘/Users/santanay/code/OHW19/ohw19-project-co_locators/coordinates.zip’, index_col=0)
import cartopy.io.shapereader as shpreader


def plot(df_coords):

    '''
    data_coords = gv.Dataset(df_coords, kdims=['longitude (degrees_east)',
                                              'latitude (degrees_north)',
                                              'Dataset ID','dataset_count'])
    points = data_coords.to(gv.Points, ['longitude (degrees_east)',
                                       'latitude (degrees_north)'],
                           ['Dataset ID','dataset_count'])
    tiles = gv.tile_sources.EsriOceanBase
    figure = tiles * points.opts(size=5, color='dataset_count', cmap='viridis',
                                 tools=['hover'], width=600, height=600, global_extent=True)
    '''

    '''
    shpfilename = shpreader.natural_earth(resolution='10m',
                                        category='physical',
                                        name='coastline')
    figure = df_coords.hvplot.scatter(
       'longitude (degrees_east)','latitude (degrees_north)', s=2, c='Dataset ID',
       projection=ccrs.PlateCarree(),
       width=600, height=540, cmap=cmo.cm.tempo,
       datashade=True
    ) * gv.Shape.from_shapefile(shpfilename, crs=ccrs.PlateCarree())
    '''

    '''
    tiles = gv.tile_sources.EsriOceanBase
    figure = df_coords.hvplot.scatter(
       'longitude (degrees_east)','latitude (degrees_north)', s=2, c='Dataset ID',
       projection=ccrs.PlateCarree(),
       width=600, height=540, cmap=cmo.cm.tempo,
       datashade=True
    ) * tiles
    '''

    '''
    tiles = gv.tile_sources.EsriOceanBase
    figure = tiles * df_coords.hvplot.points(
       x='longitude (degrees_east)', y='latitude (degrees_north)', s=2, c='Institution',
       hover_cols=['Dataset ID', 'dataset_count'],
       width=600, height=540, cmap=cmo.cm.tempo,
       projection=ccrs.PlateCarree(),
       datashade=True,
       title='ERDDAP Co-Locate Results'
    '''

    x_proj, y_proj = ds.geo.lnglat_to_meters(df_coords.x, df_coords.y)

    df_coords = df_coords.join([pd.DataFrame({'easting': x_proj}), pd.DataFrame({'northing': y_proj})])

    figure = tiles * df_coords.hvplot.points(
       x='easting', y='northing', s=2, c='Institution',
       hover_cols=['Dataset ID', 'dataset_count'],
       width=600, height=540, cmap=cmo.cm.tempo,
       datashade=True,
       title='ERDDAP Co-Locate Results'
    )

#     shpfilename = shpreader.natural_earth(resolution='10m',
#                                         category='physical',
#                                         name='coastline')
#     figure = df_coords.hvplot.scatter(
#        'longitude (degrees_east)','latitude (degrees_north)', s=5, c='Dataset ID',
#        projection=ccrs.PlateCarree(),
#        width=600, height=540, cmap=cmo.cm.tempo,
#        datashade=True
#     ) * gv.Shape.from_shapefile(shpfilename, crs=ccrs.PlateCarree())

    return figure
