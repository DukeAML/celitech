import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

from dataclean import *

# Change values here to get different graphs
DAYS_TO_RECORD = 365
DISPLAY = "Total Usage Time" # Total Usage Time | Total Bytes Used

df = pd.read_csv("sample_data.csv")
COUNTRIES = retrieve_countries(df) # X-axis
TIME = [i for i in range(24)] # Y-axis

# Create list of DAYS_TO_RECORD points for line graph
def accumulate_data(df):

    global TOTAL
    Z = np.array([[0 for i in range(24)] for i in range(len(COUNTRIES))])
    Z = Z.astype(float)

    for i in range(len(COUNTRIES)):

        df_temp = df[df['COUNTRY_ISO3'].str.match(COUNTRIES[i])]
        for index, row in df_temp.iterrows():

            # Note start time
            start_time = row["CONNECT_TIME"].hour

            # Usage time is in HRS
            diff = row["CLOSE_TIME"] - row["CONNECT_TIME"]
            total_hours = diff.total_seconds() / 3600
            Z[i][start_time] += total_hours

    Z = Z.transpose((1,0))
    return Z

def main(df=df):
    df = country_limit_zero_remove(df, COUNTRIES)
    df = time_limit(df, DAYS_TO_RECORD)
    hour_density = accumulate_data(df).astype(int) # Convert back for compatibility with plotly

    fig = go.Figure(data=go.Heatmap(
            z = hour_density,
            x = COUNTRIES,
            y = TIME,
            colorscale = 'Viridis'
    ))

    fig.update_layout(
            title='Length of Average Connection Opened Each Hour',
            xaxis_title="Countries",
            yaxis_title="Time of the Day",
            yaxis=dict(autorange='reversed')
    )



    fig.show()

if __name__=="__main__":
    main()
