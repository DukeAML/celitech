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

    country_connections = {key: 0 for key in COUNTRIES}

    for key in COUNTRIES:
        total_users = len(df[df['COUNTRY_ISO3'].str.match(key)].ICCID.unique())
        total_connects = len(df[df['COUNTRY_ISO3'].str.match(key)])


        if (total_users != 0):
            country_connections[key] = total_connects / total_users

    return country_connections



df = country_limit_zero_remove(df, COUNTRIES)
df = time_limit(df, DAYS_TO_RECORD)
country_connections = accumulate_data(df)
new_df = pd.DataFrame(list(country_connections.items()), columns=["Country", "avg_calls_per_user"])
new_df = new_df.sort_values("avg_calls_per_user", ascending=False)


fig = px.bar(new_df, x="Country", y="avg_calls_per_user",
             labels={"avg_calls_per_user":"Average Number of Connections Opened per User"}
)

fig.update_layout(
        title="Average Connections per User by Country",
)

fig.show()
