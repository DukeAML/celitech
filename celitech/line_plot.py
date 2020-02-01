import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Change values here to get different graphs
COUNTRY_SUBSET = ['USA', 'DEU'] # options: input ISO3's into list
DAYS_TO_RECORD = 210

REGULAR_YEAR = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
LEAP_YEAR = [0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.000Z"
TODAY = datetime.now()

# Make dataframe only include countries of interest and nonzero values for duration
df = pd.read_csv("sample_data.csv")
df.loc[(df['COUNTRY_ISO3'].isin(COUNTRY_SUBSET)) & (df['DURATION'] == 0)]


# NOTE: CONVERTS EACH STRING CONNECT_TIME TO DATETIME IN ORDER
#       TO DETERMINE TIME LAPSED SINCE PRESENT. COULD SAVE TIME
#       BY ENSURING DATA IS SORTED BEFORE GRAPHING, AND ONLY
#       TAKING FARTHEST DATE AND UP.
def clean(time):
    return datetime.strptime(time, DATE_FORMAT)

# Limit dataframe to only data that has occured within total_days of present
def time_limit(df, total_days):
    print(len(df))
    # Convert time string to datetime and constrain by days from present
    df['CONNECT_TIME'] = df['CONNECT_TIME'].apply(clean)
    old_time = TODAY - timedelta(days=total_days)
    df.loc[df['CONNECT_TIME'] > old_time]
    print(len(df))
    # Convert CLOSE_TIME to datetime object too
    df['CLOSE_TIME'] = df['CLOSE_TIME'].apply(clean)

    return df

# Create list of DAYS_TO_RECORD points for line graph
def accumulate_data(df, total_days):

    num_data = [0 for i in range(total_days)]

    # Iterate through data and increment list for each datapoint's hours
    # Determine time placement based off CONNECT_TIME
    for index, row in df.iterrows():

        day = (TODAY - row["CONNECT_TIME"]).days
        diff = row["CLOSE_TIME"] - row["CONNECT_TIME"]
        total_hours = diff.total_seconds() / 3600
        print(row["CONNECT_TIME"] > (TODAY - timedelta(days=total_days)))
        print(day, row["CONNECT_TIME"])

        print(len(num_data))
        num_data[day-1] += total_hours

    return num_data


df = time_limit(df, DAYS_TO_RECORD)
num_data = accumulate_data(df, DAYS_TO_RECORD)
num_days = [i+1 for i in range(DAYS_TO_RECORD)]


fig = go.Figure()
fig.add_trace(go.Scatter(
        x=num_days,
        y=num_data,
        line = dict(color='royalblue', width=4)
                         ))

fig.show()



# hour = int(connect_time[11:13])
# local_day = int(connect_time[8:10])
# month = int(connect_time[5:7])
# year = int(connect_time[0:4])
# connect_time = str(row["CONNECT_TIME"])
