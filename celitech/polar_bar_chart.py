import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

COUNTRY_SUBSET = ['USA, DEU']
TIMESPLIT = 'MONTH' # option2: MONTH



# Make dataframe only include countries of interest and nonzero values for duration
df = pd.read_csv("sample_data.csv")
df.loc[(df['COUNTRY_ISO3'].isin(COUNTRY_SUBSET)) & (df['DURATION'] == 0)]

def select_data_on_day():
    # Determine MONTH based off CONNECT_TIME
    num_calls = [0 for i in range(365)]

    # Iterate through data and increment list for each call
    for index, row in df.iterrows():
        connect_time = str(row["CONNECT_TIME"])
        m_day = int(connect_time[8:10])
        month = int(connect_time[5:7])
        day = m_day * month
        num_calls[day] += 1

    return num_calls

def select_data_on_month():
    # Determine MONTH based off CONNECT_TIME
    num_calls = [0 for i in range(12)]

    # Iterate through data and increment list for each call
    for index, row in df.iterrows():
        connect_time = str(row["CONNECT_TIME"])
        month = int(connect_time[5:7])
        num_calls[month] += 1

    return num_calls

# Change arguments based off customizations
if (TIMESPLIT=='DAY'): num_calls = select_data_on_day()
else: num_calls = select_data_on_month()

num_splits = len(num_calls)
increments = [(x+1)*(360/num_splits) for x in range(num_splits)]


fig = go.Figure(go.Barpolar(
    r=num_calls,
    theta=increments,
    marker_color=px.colors.sequential.deep
    #colorscale=px.colors.cyclical.swatches_cyclical

                            ))


fig.show()
