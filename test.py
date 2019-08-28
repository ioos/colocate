import ipywidgets as widgets


class boxClass():
    latMin = widgets.FloatText(
        value=7.5,
        description='Min Lat:',
        disabled=False
    )

    latMax = widgets.FloatText(
        value=7.5,
        description='Max Lat:',
        disabled=False
    )

    lonMin = widgets.FloatText(
        value=7.5,
        description='Min Lon:',
        disabled=False
    )

    lonMax = widgets.FloatText(
        value=7.5,
        description='Max Lon:',
        disabled=False
    )

    time_min = widgets.Text(
        value='2010-07-10',
        placeholder='Start Time',
        description='String:',
        disabled=False
    )

    time_max = widgets.Text(
        value='2010-07-10',
        placeholder='End Time',
        description='String:',
        disabled=False
    )

    def dispBox(self):
      display(self.latMin, self.latMax, self.lonMin,
              self.lonMax, self.time_min, self.time_max)

    def getDict(self):
      kw = {
          'search_for': 'all',
          'min_lon': self.lonMin,
          'max_lon': self.lonMax,
          'min_lat': self.latMin,
          'max_lat': self.latMax,
          'min_time': self.time_min+str('T00:00:00Z'),
          'max_time': self.time_max+str('T00:00:00Z'),
      }

      return kw
