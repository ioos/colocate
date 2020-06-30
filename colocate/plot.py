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

    shpfilename = shpreader.natural_earth(resolution='10m',
                                        category='physical',
                                        name='coastline')
    figure = df_coords.hvplot.scatter(
       'longitude (degrees_east)','latitude (degrees_north)', s=2, c='Dataset ID',
       projection=ccrs.PlateCarree(),
       width=600, height=540, cmap=cmo.cm.tempo,
       datashade=True
    ) * gv.Shape.from_shapefile(shpfilename, crs=ccrs.PlateCarree())

    return figure

def plot_datashader(df_coords):
    colors = cc.glasbey_bw
    #x_proj, y_proj = ds.utils.lnglat_to_meters(df_coords['longitude (degrees_east)'], df_coords['latitude (degrees_north)'])
    #df_coords = df_coords.join([pd.DataFrame({'easting': x_proj}), pd.DataFrame({'northing': y_proj})])
    df_coords.loc[:, 'easting'], df_coords.loc[:, 'northing'] = ds.utils.lnglat_to_meters(df_coords['longitude (degrees_east)'], df_coords['latitude (degrees_north)'])


    tiles = gv.tile_sources.EsriOceanBase
    #tiles = gv.tile_sources.EsriUSATopo
    #tiles = gv.tile_sources.CartoEco
    #tiles = gv.tile_sources.CartoDark


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
    '''

    '''

    figure = tiles * df_coords.hvplot.points(
       x='easting', y='northing', size=4, c='Dataset ID',
       #color=dim('easting'),
       #alpha=0.5, hover_alpha=1,
       #s='Dataset ID', scale=10,
       hover_cols=['Dataset ID', 'dataset_count'],
       width=900, height=600, color_key=cc.b_glasbey_bw,
       legend='bottom',
       datashade=True,
       dynspread=True,
       rasterize=True,
       title='ERDDAP Co-Locate Results'
    )
    '''

    figure = df_coords.hvplot.points(
        geo=True, tiles=tiles,
        datashade=True,
        dynspread=True,
        aggregator=ds.count_cat('dataset_count'),
        width=900, height=600,
        color_key=cc.b_glasbey_bw,
        colorbar=True,
        legend='top',
        #legend=True,

        #x='easting', y='northing', c='Dataset ID',
        #x='easting', y='northing', c='dataset_count',
        #crs=ccrs.Mercator(),

        #x='longitude (degrees_east)', y='latitude (degrees_north)', c='Dataset ID',
        x='longitude (degrees_east)', y='latitude (degrees_north)', c='dataset_count',
        crs=ccrs.PlateCarree(),
        project=True,
        rasterize=True,
        xlim=(df_coords['longitude (degrees_east)'].min(),df_coords['longitude (degrees_east)'].max()),
        ylim=(df_coords['latitude (degrees_north)'].min(),df_coords['latitude (degrees_north)'].max()),

        #projection=ccrs.PlateCarree(),
        hover=True,
        hover_cols=['Dataset ID', 'dataset_count'],

        #global_extent=False,
        #size=5,
        #size='Dataset ID'
        #alpha=0.5, hover_alpha=1,
        scale=10,
        title='ERDDAP Co-Locate Results'
    )

    return figure
