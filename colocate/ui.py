import warnings
warnings.simplefilter('ignore')

import ipywidgets as widgets
from ipyleaflet import Map, DrawControl
from IPython.display import clear_output

from colocate import erddap_query, run, plot
from datetime import date, timedelta

m = Map(zoom=2)

dc = DrawControl(polyline={}, polygon={}, circlemarker={}, rectangle={'shapeOptions': {'color': '#0000FF'}})

kw = None
coords = None
df = None

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


out = widgets.Output()


@out.capture()
def on_button_clicked(_):
    global kw, df

    clear_output()
    if coords:
        kw = get_data()
        df = run.ui_query(kw)
        if df.shape[0] == 0:
            msg = '\nNo data returned... select different filter criteria'
        else:
            df.dropna(subset=['tabledap'], inplace=True)
            msg = '\nFound {} datasets'.format(df.shape[0])

    else:
        msg = '\nPlease, select some area'

    with out:
        print(msg)


def on_graph_button(_):
    all_coords = erddap_query.get_coordinates(df, **kw)
    plot.plot(all_coords)


def get_data():
    lats = []
    lons = []

    for point in coords[-1][:-1]:
        lon_180 = ((point[0] - 180) % 360) - 180
        lons.append(lon_180)

        lat_90 = ((point[1] - 90) % 180) - 90
        lats.append(lat_90)

    params = {
        'min_lon': lons[0],
        'max_lon': lons[2],
        'min_lat': lats[0],
        'max_lat': lats[2],
        'min_time': dates.value[0].strftime('%Y-%m-%dT%H:%M:%SZ'),
        'max_time': dates.value[1].strftime('%Y-%m-%dT%H:%M:%SZ'),
        'standard_name': drpdwn.value
    }

    return params


btn = widgets.Button(description='Search servers')

btn.on_click(on_button_clicked)

button = widgets.VBox([btn, out])

std_names=['sea_water_practical_salinity','sea_water_temperature','sea_surface_wave_significant_height','mass_concentration_of_chlorophyll_in_sea_water','eastward_sea_water_velocity','northward_sea_water_velocity']


drpdwn = widgets.Dropdown(
    options=std_names,
    description='CF Standard Names:',
    disabled=False,
)

graph = widgets.Button(description='Make plot')

graph.on_click(on_graph_button)
