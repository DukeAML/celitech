import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

from dataclean import *

# Change values here to get different graphs
DAYS_TO_RECORD = 365
COUNTRIES = []

# Create list of DAYS_TO_RECORD points for line graph
def accumulate_data(df, COUNTRIES):

    country_aggregate = {"Countries":COUNTRIES,
                        "Average Connections per User":[0 for i in range(len(COUNTRIES))],
                        "Average GB per User":[0 for i in range(len(COUNTRIES))],
                        "Average Time per User":[0 for i in range(len(COUNTRIES))]}

    for i in range(len(COUNTRIES)):
        key = COUNTRIES[i]
        total_users = len(df[df['COUNTRY_ISO3'].str.match(key)].ICCID.unique())
        total_connects = len(df[df['COUNTRY_ISO3'].str.match(key)])
        total_bytes = sum(df[df['COUNTRY_ISO3'].str.match(key)]["DURATION"]) / BYTES_TO_GB #GB
        total_time_col = (df[df['COUNTRY_ISO3'].str.match(key)]["CLOSE_TIME"] - df[df['COUNTRY_ISO3'].str.match(key)]["CONNECT_TIME"])
        total_time_mins = sum(total_time_col.apply(convert_timedelta_mins))


        if (total_users != 0):
            country_aggregate["Average Connections per User"][i] = total_connects / total_users
            country_aggregate["Average GB per User"][i] = total_bytes / total_users
            country_aggregate["Average Time per User"][i] = total_time_mins / total_users

    return country_aggregate


def main(df):
    df = country_limit_zero_remove(df, COUNTRIES)
    df = time_limit(df, DAYS_TO_RECORD)
    country_aggregate = accumulate_data(df, COUNTRIES)

    new_df = pd.DataFrame(country_aggregate, columns=["Countries", "Average Connections per User", "Average GB per User", "Average Time per User"])
    new_df = new_df.sort_values("Average GB per User", ascending=False)


    fig = go.Figure()
    fig.add_trace(go.Histogram(histfunc="sum", y=list(new_df["Average Connections per User"]), x=list(new_df["Countries"]), name="Average Connections per User"))
    fig.add_trace(go.Histogram(histfunc="sum", y=list(new_df["Average GB per User"]), x=list(new_df["Countries"]), name="Average GB per User", marker_color='#330C73'))
    fig.add_trace(go.Histogram(histfunc="sum", y=list(new_df["Average Time per User"]), x=list(new_df["Countries"]), name="Average Minutes per User", marker_color='LightSkyBlue'))
    time = str(DAYS_TO_RECORD) + " Days"
    fig.update_layout(
            title="Average User Data Usage Over {} by Country".format(time)
            )
    fig.update_yaxes(type='log')
    fig.show()


if __name__=="__main__":
    df = pd.read_csv("sample_data.csv")
    COUNTRIES = retrieve_countries(df)
    main(df)
