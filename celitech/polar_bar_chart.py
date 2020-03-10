import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from dataclean import BYTES_TO_GB,TODAY, is_leap_year

# Change values here to get different graphs
COUNTRY_SUBSET = ['USA', 'DEU'] # options: input ISO3's into list
TIMESPLIT = 'MONTH' # options: DAY|MONTH
DATATYPE = 'DURATION' # options: CALLS|DURATION

REGULAR_YEAR = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
LEAP_YEAR = [0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
YEAR = REGULAR_YEAR

if (is_leap_year(TODAY.year)): YEAR = LEAP_YEAR

def select_data_on_timesplit(df, datatype, time):
    # Determine length of num_data
    if (time=="DAY"): num_data = [0 for i in range(365)]
    else: num_data = [0 for i in range(12)]

    # Iterate through data and increment list for each datapoint
    # Determine time placement based off CONNECT_TIME
    for index, row in df.iterrows():
        connect_time = str(row["CONNECT_TIME"])
        local_day = int(connect_time[8:10])
        month = int(connect_time[5:7])

        if(datatype=="CALLS"):
            if(time=="DAY"):
                day = YEAR[month-1] + local_day
                num_data[day-1] += 1
            else: num_data[month-1] += 1
        else:
            if(time=="DAY"):
                day = YEAR[month-1] + local_day
                num_data[day-1] += int(row["DURATION"]) / BYTES_TO_GB # Bytes to GB
            else: num_data[month-1] += int(row["DURATION"]) / BYTES_TO_GB # Bytes to GB

    return num_data

def main(df):
    # Change arguments based off customizations
    num_data = select_data_on_timesplit(df, DATATYPE, TIMESPLIT)

    num_splits = len(num_data)
    increments = [(x+1)*(360/num_splits) for x in range(num_splits)]


    fig = go.Figure(go.Barpolar(
        r=num_data,
        theta=increments,
        marker_color=px.colors.sequential.deep
                                ))

    fig.update_layout(
            title="Total {} on Each Day of All Years".format(DATATYPE.lower().capitalize()),
    )

    fig.show()


if __name__=="__main__":
    # Make dataframe only include countries of interest and nonzero values for duration
    df = pd.read_csv("sample_data.csv")
    df = df[(df['COUNTRY_ISO3'].isin(COUNTRY_SUBSET)) & (df['DURATION'] != 0)]
    main(df)
