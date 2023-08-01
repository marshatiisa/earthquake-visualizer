import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Data source: https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv

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

    # extract sub-area in place
    place_list = df_earthquake['place'].str.split(',')
    
# Create visualizer