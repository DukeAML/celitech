import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

from dataclean import *

# Change values here to get different graphs
COUNTRY_SUBSET = ['USA', 'DEU'] # options: input ISO3's into list|call retrieve_countries()
DAYS_TO_RECORD = 300


# Create list of DAYS_TO_RECORD points for line graph
def accumulate_data(df, total_days):

    num_data = [0 for i in range(total_days)]
    avg_mins = [0 for i in range(total_days)]
    num_users = {i+1:[] for i in range(total_days)}

    # Iterate through data and increment list for each datapoint's hours
    # Determine time placement based off CONNECT_TIME
    for index, row in df.iterrows():

        day = (TODAY - row["CONNECT_TIME"]).days
        diff = row["CLOSE_TIME"] - row["CONNECT_TIME"]
        total_hours = diff.total_seconds() / 3600

        num_data[day-1] += total_hours
        num_users.get(day).append(row["ICCID"])

    for i in range(total_days):
        total_users = len(set(num_users.get(i+1)))
        if total_users != 0: avg_mins[i] = (num_data[i]) / total_users

    return num_data, avg_mins


def main(df):
    # Data cleaning and plot variables created
    df = country_limit_zero_remove(df, COUNTRY_SUBSET)
    df = time_limit(df, DAYS_TO_RECORD)
    num_data,avg_mins = accumulate_data(df, DAYS_TO_RECORD)
    num_days = [i+1 for i in range(DAYS_TO_RECORD)]


    fig = go.Figure()

    fig.add_trace(go.Scatter(
            x=num_days,
            y=num_data,
            line = dict(color='royalblue', width=2),
            name="Hours of Cellular Data",
            opacity = 0.5,
            text=[avg_mins[i] for i in range(DAYS_TO_RECORD)],
            hovertemplate='%{x} Days, %{y:.1f} hrs' + ', %{text:.1f} avg hrs'
    ))

    fig.add_trace(go.Scatter(
            x=num_days,
            y=avg_mins,
            line = dict(color='#330C73', width=2),
            name = "Average Hours per User",
            opacity = 0.3,
            text=[num_data[i] for i in range(DAYS_TO_RECORD)],
            hovertemplate='%{x} Days, %{text:.1f} hrs' + ', %{y:.1f} avg hrs'
    ))

    fig.update_layout(
            title="Total Cellular Used per Day",
            xaxis_title="Day",
            hovermode="closest",
            xaxis={'showspikes':True, 'spikemode':'across', 'spikethickness':1}
    )


    fig.show()

if __name__=="__main__":
    df = pd.read_csv("sample_data.csv")
    main(df)
