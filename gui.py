import warnings
warnings.simplefilter('ignore')

import ipywidgets as widgets
from ipyleaflet import Map, DrawControl
from IPython.display import clear_output

from datetime import date, timedelta

m = Map(zoom=2)

dc = DrawControl(rectangle={'shapeOptions': {'color': '#0000FF'}})

kw = {}
coords = []


def handle_draw(self, action, geo_json):
    global coords
    coords = geo_json['geometry']['coordinates']


dc.on_draw(handle_draw)

m.add_control(dc)

start_date = date(1950, 1, 1)
end_date = date(2020, 1, 1)

days = (end_date - start_date).days
dates = []
for n_day in range(days):
    dates.append(start_date + timedelta(days=n_day))

dates = widgets.SelectionRangeSlider(
    value=(start_date, end_date - timedelta(days=1)),
    options=dates,
    description='Starting date',
    layout=widgets.Layout(width='90%')
)


def on_button_clicked(_):
    global kw
    
    if coords:
        kw = get_data(dates, coords)
        msg = kw
    else:
        msg = 'Please, select some area'
    
    with out:
        clear_output()
        print(msg)


def get_data(dates, coords):
    lats = []
    lons = []

    for point in coords[-1][:-1]:
        lon_180 = ((point[0] - 180) % 360) - 180
        lons.append(lon_180)

        lat_180 = ((point[1] - 180) % 360) - 180
        lats.append(lat_180)

    params = {
        'search_for': 'all',
        'min_lon': lons[0],
        'max_lon': lons[2],
        'min_lat': lats[0],
        'max_lat': lats[2],
        'min_time': dates.value[0].strftime('%Y-%m-%dT%H:%M:%SZ'),
        'max_time': dates.value[1].strftime('%Y-%m-%dT%H:%M:%SZ'),
    }

    return params


btn = widgets.Button(description='Get data')

out = widgets.Output()

btn.on_click(on_button_clicked)

button = widgets.VBox([btn, out])
