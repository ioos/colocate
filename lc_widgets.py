import ipywidgets as widgets
import geoviews as gv
import holoviews as hv
import cartopy.crs as ccrs

# from holoviews.streams import PointDraw, PolyEdit, BoxEdit, PolyDraw

# url = "http://c.tile.openstreetmap.org/{Z}/{X}/{Y}.png"
# dx = dy = 180
# lat, lon = 47.60, -122.33
# extents = lon-dx, lat-dy, lon+dx, lat+dy

# tiles = gv.WMTS(url, extents=extents, crs=ccrs.PlateCarree())

# hv.extension("bokeh")

# class WorldMap():
#     def __init__(self):
#         %%opts Polygons [width=750 height=500] 
#         %%opts Polygons (fill_alpha=0 line_color="black" selection_fill_color="red" line_width=5)

#         sample_box = [[-13873713, 5925064], [-13873713, 6348504],
#               [-13461934, 6348504], [-13461934, 5925064],]

#         self.box_poly = gv.Polygons([sample_box], crs=ccrs.GOOGLE_MERCATOR)
#         self.box_stream = BoxEdit(source=box_poly)
#         self.positions = []
#         self.dispMap = tiles * box_poly
        
#     def bbox(poly):
#         "Convert the polygon returned by the BoxEdit stream into a bounding box tuple"
#         xs,ys = poly.array().T
#         return (xs[0], ys[0], xs[2], ys[2])
    
    
#     def getPos(self):
#     if self.box_stream.element:
#         polygons = gv.operation.project_path(box_stream.element, 
#                                          projection=ccrs.PlateCarree()).split()
#         bboxes = [bbox(p) for p in polygons]
#         print(bboxes)

       


class boxClass():
    latMin = widgets.FloatText(
        value=38,
        description='Min Lat:',
        disabled=False
    )

    latMax = widgets.FloatText(
        value=41,
        description='Max Lat:',
        disabled=False
    )

    lonMin = widgets.FloatText(
        value=-72,
        description='Min Lon:',
        disabled=False
    )

    lonMax = widgets.FloatText(
        value=-69,
        description='Max Lon:',
        disabled=False
    )

    time_min = widgets.Text(
        value='2010-07-10',
        placeholder='YYYY-MM-DD',
        description='Start Date:',
        disabled=False
    )

    time_max = widgets.Text(
        value='2010-08-10',
        placeholder='YYYY-MM-DD',
        description='End Date:',
        disabled=False
    )

    def dispBox(self):
      display(self.latMin, self.latMax, self.lonMin,
              self.lonMax, self.time_min, self.time_max)

    def getDict(self):
      kw = {
          'search_for': 'all',
          'min_lon': self.lonMin.value,
          'max_lon': self.lonMax.value,
          'min_lat': self.latMin.value,
          'max_lat': self.latMax.value,
          'min_time': self.time_min.value + 'T00:00:00Z',
          'max_time': self.time_max.value + 'T00:00:00Z'
      }

      return kw
    


