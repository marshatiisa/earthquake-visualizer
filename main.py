import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Data source: https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv

def extract_subarea(place):
    return place[0]

def extract_area(place):
    return place[-1]

def extract_date(time):
    return str(time).split(' ')[0]

def extract_weekday(time):
    date = extract_date(time)
    return date + ' - ' + str(time.weekday())

def extract_hour(time):
    t = str(time).split(' ')
    return t[0] + ' - ' + t[1].split(':')[0]

# Fetch data and clean it up
def fetch_eq_data(period='daily', region="Worldwide", min_mag=1):
    url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/{}.csv'
    if period == 'wwekly':
        new_url = url.format('all_week')
    elif period == 'monthly':
        new_url = url.format('all_month')
    else:
        new_url = url.format('all_day')

    df_earthquake = pd.read_csv(new_url)
    df_earthquake = df_earthquake[['time', 'latitude', 'longitude', 'mag', 'place']]

    # extract sub-area in place columns
    place_list = df_earthquake['place'].str.split(',')
    df_earthquake['subarea'] = place_list.apply(extract_subarea)
    df_earthquake['area'] = place_list.apply(extract_area)
    df_earthquake = df_earthquake.drop(columns=['place'], axis=1)

    # filter data based on min. threshold (magnitude)
    if isinstance(min_mag, int) and min_mag > 0:
        df_earthquake = df_earthquake[df_earthquake['mag'] >= min_mag]
    else:
        df_earthquake = df_earthquake[df_earthquake['mag'] > 0]

    # covert 'time' to panda(pd) datetime
    df_earthquake['time'] = pd.to_dattime[df_earthquake['time']]

    # set lat and long to some default if not found
    if region in df_earthquake['area'].to_list():
        df_earthquake = df_earthquake[df_earthquake['area']] == region
        max_mag = df_earthquake['mag'].max()
        center_lat = df_earthquake[df_earthquake['mag'] == max_mag]['latitude'].values[0]
        center_long = df_earthquake[df_earthquake['mag'] == max_mag]['longitude'].values[0]
    else:
        center_lat, center_long = [54,15]

    #Set columns for animation frames
    #weekdays, dates and hours
    if period == 'weekly':
        animation_frame_col = 'weekday'
        df_earthquake[animation_frame_col] = df_earthquake['time']# to complete later

# Create visualizer