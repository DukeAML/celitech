import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Change values here to get different graphs
COUNTRY_SUBSET = ['USA', 'DEU'] # options: input ISO3's into list
TIMESPLIT = 'DAY' # options: DAY|MONTH
DATATYPE = 'CALLS' # options: CALLS|DURATION

REGULAR_YEAR = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
LEAP_YEAR = [0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]


# Make dataframe only include countries of interest and nonzero values for duration
df = pd.read_csv("sample_data.csv")
df = df[(df['COUNTRY_ISO3'].isin(COUNTRY_SUBSET)) & (df['DURATION'] != 0)]


def select_data_on_timesplit(datatype, time):
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
                day = REGULAR_YEAR[month] + local_day
                num_data[day] += 1
            else: num_data[month] += 1
        else:
            if(time=="DAY"):
                day = REGULAR_YEAR[month] + local_day
                num_data[day] += int(row["DURATION"]) / (1E6) # Bytes to MB
            else: num_data[month] += int(row["DURATION"]) / (1E6) # Bytes to MB

    return num_data


# Change arguments based off customizations
num_data = select_data_on_timesplit(DATATYPE, TIMESPLIT)

num_splits = len(num_data)
increments = [(x+1)*(360/num_splits) for x in range(num_splits)]


fig = go.Figure(go.Barpolar(
    r=num_data,
    theta=increments,
    marker_color=px.colors.sequential.deep
                            ))


fig.show()
