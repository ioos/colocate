import pandas as pd
import cmocean as cmo

import geoviews as gv
import hvplot.pandas
from holoviews import dim

import datashader as ds

import colorcet as cc
from colorcet.plotting import swatch

import cartopy.crs as ccrs
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

    colors = cc.glasbey_bw
    x_proj, y_proj = ds.utils.lnglat_to_meters(df_coords['longitude (degrees_east)'], df_coords['latitude (degrees_north)'])
    df_coords = df_coords.join([pd.DataFrame({'easting': x_proj}), pd.DataFrame({'northing': y_proj})])

    #tiles = gv.tile_sources.EsriOceanBase
    #tiles = gv.tile_sources.CartoEco
    tiles = gv.tile_sources.CartoDark

    '''
    figure = tiles * df_coords.hvplot.points(
       x='easting', y='northing', s=4, by='Institution',
       hover_cols=['Dataset ID', 'dataset_count'],
       width=900, height=600, cmap=cc.b_glasbey_bw,
       datashade=True,
       title='ERDDAP Co-Locate Results'
    )
    '''

    '''
    '''
    figure = tiles * df_coords.hvplot.points(
       x='easting', y='northing', size=4, c='Dataset ID',
       #color=dim('easting'),
       #alpha=0.5, hover_alpha=1,
       #s='Dataset ID', scale=10,
       hover_cols=['Dataset ID', 'dataset_count'],
       width=900, height=600, cmap=cc.b_glasbey_bw,
       legend='bottom',
       datashade=False,
       title='ERDDAP Co-Locate Results'
    )


    return figure
    #return df_coords
