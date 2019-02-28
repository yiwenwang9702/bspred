from bokeh.embed import components
from bokeh.plotting import figure
import bokeh.tile_providers as tp
from bokeh.models import ColumnDataSource, HoverTool, LinearColorMapper, ColorBar
import math
import pandas as pd
from .get_path import *

def merc(lat, lon):
    x = 6378137.000 * math.radians(lon)
    y = 180.0/math.pi * math.log(math.tan(math.pi/4.0 + lat * (math.pi/180.0)/2.0)) * x/lon
    return [x, y]
def merc_for_df(df):
    l = len(df)
    lat = df['latitude'].values
    lon = df['longitude'].values
    x = []
    y = []
    for i in range(l):
        a, b = merc(lat[i], lon[i])
        x.append(a)
        y.append(b)
    df['x'] = x
    df['y'] = y
    return df

def plot_with_new(df):
    path = get_path()
    stations = pd.read_csv(path+'stations.csv', sep = ',', engine='python')
    stations = merc_for_df(stations)
    stations = stations[['latitude', 'longitude', 'x', 'y', 'name', 'arrivals_characteristic', 'departures_characteristic']]
    stations['total'] = stations['arrivals_characteristic'] + stations['departures_characteristic']    
    df['total'] = df['Characteristic_Arrivals'] + df['Characteristic_Departures']
    source = ColumnDataSource(stations)
    df = merc_for_df(df)
    new_source = ColumnDataSource(df)
    palette_1 = ['#D6EAF8', '#AED6F1', '#85C1E9', '#529fd3', '#3285bc', '#156499']
    palette_2 = ['#f7ccbe', '#f4ae97', '#f49677', '#ea4d17', '#c43b0d']

    TOOLS='pan,wheel_zoom,box_zoom,reset,tap,box_select,lasso_select'
    hover = HoverTool(names=['old'], tooltips = [('Station Name', '@name'), ('Characteristic Arrivals', '@arrivals_characteristic{1.11}'), ('Characteristic Departures', '@departures_characteristic{1.11}')])
    new_hover = HoverTool(names=['new'], tooltips = [('New Station Address', '@address'), ('Characteristic Arrivals', '@Characteristic_Arrivals{1.11}'), ('Characteristic Departures', '@Characteristic_Departures{1.11}')])
    color_mapper = LinearColorMapper(palette=palette_1[1:], low = 0, high = 3000)
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=10, border_line_color=None, location=(0,0))
    new_color_mapper = LinearColorMapper(palette=palette_2, low = 0, high = 3000)
    new_color_bar = ColorBar(color_mapper=new_color_mapper, label_standoff=10, border_line_color=None, location=(0,0))
    p = figure(plot_width = 650, plot_height=500, x_range=(-8246547.8779657055, -8226510.369622918), y_range=(4958652.406523315, 4988034.58002491),tools=[hover, new_hover, TOOLS])
    p.add_tile(tp.CARTODBPOSITRON_RETINA)
    p.xaxis.visible = False
    p.yaxis.visible = False
    p.circle(name='old', x='x', y='y', line_color=None, fill_color={"field":"total", "transform":color_mapper}, fill_alpha=1, size=6, source=source)
    p.circle(name='new', x='x', y='y', line_color=None, fill_color={"field":"total", "transform":new_color_mapper}, fill_alpha=1, size=6, source=new_source)
    p.add_layout(color_bar,'right')
    p.add_layout(new_color_bar,'right')
    
    return p
