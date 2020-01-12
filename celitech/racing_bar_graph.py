import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pycountry
import plotly
import plotly.graph_objs as go
import json
import matplotlib.ticker as ticker
from matplotlib.animation import FuncAnimation
from datetime import datetime
from IPython.display import HTML

countries_in_data = ["FRA", "USA", "ESP", "UKR", "DEU", "ITA", "CHE", "GBR"]
df = pd.read_csv("sample_data.csv")

# Generate country code dictionary
countries = {}
for country in pycountry.countries:
    countries[country.name] = country.alpha_3

# Generate dictionary of country vs. usage for particular day
def country_by_day(month, day):
    date = "2019-"+str(month).zfill(2)+"-"+str(day).zfill(2)

    usage_dict = {}
    for index, row in df.iterrows():
        row_date = row["CLOSE_TIME"]
        if date in row_date:
            country_name = str(row["COUNTRY_NAME"])
            country_code =  countries.get(country_name)
            duration = int(row["DURATION"])
            duration = duration/(1E9)
            if country_code in usage_dict:
                usage_dict[country_code] = usage_dict[country_code] + duration
            else:
                usage_dict[country_code] = duration
    return sorted(usage_dict)

# Generate usage vs country dictionary for a particular month
def data_for_month(month):
    date = "2019-"+str(month).zfill(2)
    usage_dict = {}
    for index, row in df.iterrows():
        row_date = row["CLOSE_TIME"]
        if date in row_date:
            country_name = str(row["COUNTRY_NAME"])
            country_code =  countries.get(country_name)
            duration = int(row["DURATION"])
            duration = duration/(1E9)
            if country_code in usage_dict:
                usage_dict[country_code] = usage_dict[country_code] + duration
            else:
                usage_dict[country_code] = duration
    
    for country in countries_in_data:
        if country not in usage_dict:
            usage_dict[country] = 0.0

    return usage_dict

# Aggregate data from series of country vs. usage dictionaries
def aggregate_dates(dicts):
    total_usage = {}
    for date in dicts:
        for loc in date:
            if loc in total_usage:
                total_usage[loc] = total_usage[loc] + date[loc]
            else:
                total_usage[loc] = date[loc]
    
    return total_usage

# Determine month of session based on CLOSED_TIME
def get_month(time_string):
    month = "july"
    if "-08" in time_string:
        month = "august"
    if "-09" in time_string:
        month = "september"
    return month



fig, ax = plt.subplots(figsize=(15, 8))
def draw_barchart(month):
    month_dict = data_for_month(month)
    print(month_dict)
    print(month_dict)
    ax.clear()
    y_pos = np.arange(len(month_dict.keys()))
    ax.barh(y_pos, month_dict.values(), align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(month_dict.keys())
    ax.invert_yaxis()
    ax.set_xlabel('Data Usage (GB)')
    ax.set_title('Data Usage by Country')

animator = FuncAnimation(fig, draw_barchart, frames=range(7,10), interval=1000)
# HTML(animator.to_jshtml()) 

plt.show()