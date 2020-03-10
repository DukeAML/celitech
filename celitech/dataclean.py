import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.000Z"
TODAY = datetime.now()
BYTES_TO_MB = 1048576
BYTES_TO_GB = 1073741824

# NOTE: CONVERTS EACH STRING CONNECT_TIME TO DATETIME IN ORDER
#       TO DETERMINE TIME LAPSED SINCE PRESENT. COULD SAVE TIME
#       BY ENSURING DATA IS SORTED BEFORE GRAPHING, AND ONLY
#       TAKING FARTHEST DATE AND UP.
def clean(time):
    return datetime.strptime(time, DATE_FORMAT)

def convert_timedelta_mins(timedel):
    return timedel.total_seconds() / 60

# Converts df attributes to datetime objects
def convert_to_datetime(df):
    df['CONNECT_TIME'] = df['CONNECT_TIME'].apply(clean)
    df['CLOSE_TIME'] = df['CLOSE_TIME'].apply(clean)
    return df

# Limits dataframe to start-end period using CONNECT_TIME as time indicator
def time_period(df, START, END):
    df = df.copy()
    df = convert_to_datetime(df)

    dff = df[ (df["CONNECT_TIME"] >= START ) & (df["CONNECT_TIME"] < END) ]

    return dff



# Limit dataframe to only data that has occured within total_days of present
def time_limit(df, total_days):

    # Convert time string to datetime and constrain by days from present
    df = df.copy()
    df = convert_to_datetime(df)

    old_time = TODAY - timedelta(days=total_days)
    df = df.loc[df['CONNECT_TIME'] > old_time]

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


def is_leap_year(year):
    """Determine whether a year is a leap year."""

    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
