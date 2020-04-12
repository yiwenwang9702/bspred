from bokeh.layouts import row
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
    stations = pd.read_csv(path+'stations.csv', sep = ',', engine='python', index_col=0)
    stations = merc_for_df(stations)
    stations = stations[['latitude', 'longitude', 'x', 'y', 'name', 'arrivals_characteristic', 'departures_characteristic']]
    source = ColumnDataSource(stations)
    df = merc_for_df(df)
    new_source = ColumnDataSource(df)
    palette_0 = ['#aeb2b1', '#aeb2b1', '#929999', '#646b6b', '#484949']
    palette_1 = ['#AED6F1', '#85C1E9', '#529fd3', '#3285bc', '#156499']
    palette_2 = ['#f7ccbe', '#f4ae97', '#f49677', '#ea4d17', '#c43b0d']

    TOOLS='pan,wheel_zoom,box_zoom,reset,tap,box_select,lasso_select'
    
    hover_1 = HoverTool(names=['old_1'], tooltips = [('Station Name', '@name'), ('Characteristic Arrivals', '@arrivals_characteristic{1.11}')])
    hover_2 = HoverTool(names=['old_2'], tooltips = [('Station Name', '@name'), ('Characteristic Departures', '@departures_characteristic{1.11}')])
    new_hover_1 = HoverTool(names=['new_1'], tooltips = [('New Station Address', '@address'), ('Characteristic Arrivals', '@Characteristic_Arrivals{1.11}')])
    new_hover_2 = HoverTool(names=['new_2'], tooltips = [('New Station Address', '@address'), ('Characteristic Departures', '@Characteristic_Departures{1.11}')])
    
    color_mapper_1 = LinearColorMapper(palette=palette_0, low = 0, high = 1500)
    color_mapper_2 = LinearColorMapper(palette=palette_0, low = 0, high = 1500)
    color_bar_1 = ColorBar(color_mapper=color_mapper_1, label_standoff=10, border_line_color=None, location=(0,0))
    color_bar_2 = ColorBar(color_mapper=color_mapper_1, label_standoff=10, border_line_color=None, location=(0,0))
    
    new_color_mapper_1 = LinearColorMapper(palette=palette_1, low = 0, high = 1500)
    new_color_mapper_2 = LinearColorMapper(palette=palette_2, low = 0, high = 1500)
    new_color_bar_1 = ColorBar(color_mapper=new_color_mapper_1, label_standoff=10, border_line_color=None, location=(0,0))
    new_color_bar_2 = ColorBar(color_mapper=new_color_mapper_2, label_standoff=10, border_line_color=None, location=(0,0))
    
    p_1 = figure(title='Characteristic Arrivals', plot_width = 550, plot_height=450, x_range=(-8246547.8779657055, -8226510.369622918), y_range=(4958652.406523315, 4988034.58002491),tools=[hover_1, new_hover_1, TOOLS])
    p_1.add_tile(tp.CARTODBPOSITRON_RETINA)
    p_1.xaxis.visible = False
    p_1.yaxis.visible = False
    p_1.circle(name='old_1', x='x', y='y', line_color=None, fill_color={"field":"arrivals_characteristic", "transform":color_mapper_1}, fill_alpha=1, size=6, source=source)
    p_1.circle(name='new_1', x='x', y='y', line_color=None, fill_color={"field":"Characteristic_Arrivals", "transform":new_color_mapper_1}, fill_alpha=1, size=6, source=new_source)
    p_1.add_layout(color_bar_1,'right')
    p_1.add_layout(new_color_bar_1,'right')
    
    p_2 = figure(title='Characteristic Departures', plot_width = 550, plot_height=450, x_range=(-8246547.8779657055, -8226510.369622918), y_range=(4958652.406523315, 4988034.58002491),tools=[hover_2, new_hover_2, TOOLS])
    p_2.add_tile(tp.CARTODBPOSITRON_RETINA)
    p_2.xaxis.visible = False
    p_2.yaxis.visible = False
    p_2.circle(name='old_2', x='x', y='y', line_color=None, fill_color={"field":"departures_characteristic", "transform":color_mapper_2}, fill_alpha=1, size=6, source=source)
    p_2.circle(name='new_2', x='x', y='y', line_color=None, fill_color={"field":"Characteristic_Departures", "transform":new_color_mapper_2}, fill_alpha=1, size=6, source=new_source)
    p_2.add_layout(color_bar_2,'right')
    p_2.add_layout(new_color_bar_2,'right')
    p = row([p_1, p_2])
    
    return p
