import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.000Z"
TODAY = datetime.now()

# NOTE: CONVERTS EACH STRING CONNECT_TIME TO DATETIME IN ORDER
#       TO DETERMINE TIME LAPSED SINCE PRESENT. COULD SAVE TIME
#       BY ENSURING DATA IS SORTED BEFORE GRAPHING, AND ONLY
#       TAKING FARTHEST DATE AND UP.
def clean(time):
    return datetime.strptime(time, DATE_FORMAT)

# Limit dataframe to only data that has occured within total_days of present
def time_limit(df, total_days):

    df = df.copy()

    # Convert time string to datetime and constrain by days from present
    df['CONNECT_TIME'] = df['CONNECT_TIME'].apply(clean)
    old_time = TODAY - timedelta(days=total_days)
    df = df.loc[df['CONNECT_TIME'] > old_time]

    # Convert CLOSE_TIME to datetime object too
    df['CLOSE_TIME'] = df['CLOSE_TIME'].apply(clean)

    return df

# Make dataframe only include countries of interest and nonzero values for duration
def country_limit_zero_remove(df, country_subset=[], remove_zeros=True):
    if (len(country_subset)==0): country_subset=retrieve_countries(df)
    if (remove_zeros):
        return df.loc[(df['COUNTRY_ISO3'].isin(country_subset))
                                & (df['DURATION'] != 0)]
    return df.loc[df['COUNTRY_ISO3'].isin(country_subset)]

# Retrieve all countries contained in database
def retrieve_countries(df):
    return list(df.COUNTRY_ISO3.unique())

# Combines filters into one for Dash implementation
def refine_celitech_dataframe(df, total_days=365, country_subset=[], remove_zeros=True):
    df = country_limit_zero_remove(df, country_subset, remove_zeros)
    df = time_limit(df, total_days)
    return df
