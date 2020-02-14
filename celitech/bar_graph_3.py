import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

from dataclean import *

# Change values here to get different graphs
DAYS_TO_RECORD = 365

df = pd.read_csv("sample_data.csv")
COUNTRIES = retrieve_countries(df)

# Create list of DAYS_TO_RECORD points for line graph
def accumulate_data(df):

    country_aggregate = {"Countries":COUNTRIES,
                        "Average Connections per User":[0 for i in range(len(COUNTRIES))],
                        "Average GB per User":[0 for i in range(len(COUNTRIES))]}

    for i in range(len(COUNTRIES)):
        key = COUNTRIES[i]
        total_users = len(df[df['COUNTRY_ISO3'].str.match(key)].ICCID.unique())
        total_connects = len(df[df['COUNTRY_ISO3'].str.match(key)])
        total_bytes = sum(df[df['COUNTRY_ISO3'].str.match(key)]["DURATION"]) / (1E9) #GB


        if (total_users != 0):
            country_aggregate["Average Connections per User"][i] = total_connects / total_users
            country_aggregate["Average GB per User"][i] = total_bytes / total_users

    return country_aggregate


def main(df=df):
    df = country_limit_zero_remove(df, COUNTRIES)
    df = time_limit(df, DAYS_TO_RECORD)
    country_aggregate = accumulate_data(df)

    new_df = pd.DataFrame(country_aggregate, columns=["Countries", "Average Connections per User", "Average GB per User"])
    new_df = new_df.sort_values("Average GB per User", ascending=False)


    fig = go.Figure()
    fig.add_trace(go.Histogram(histfunc="sum", y=list(new_df["Average Connections per User"]), x=list(new_df["Countries"]), name="Average Connections per User"))
    fig.add_trace(go.Histogram(histfunc="sum", y=list(new_df["Average GB per User"]), x=list(new_df["Countries"]), name="Average GB per User", marker_color='#330C73'))
    time = str(DAYS_TO_RECORD) + " Days"
    fig.update_layout(
            title="Average User Data Usage Over {} by Country".format(time)
            )
    fig.update_yaxes(type='log')
    fig.show()


if __name__=="__main__":
    main()
