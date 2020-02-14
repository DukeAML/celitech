import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

from dataclean import *

# Change values here to get different graphs
DAYS_TO_RECORD = 365
DISPLAY = "Total Usage Time" # Total Usage Time | Total Bytes Used

df = pd.read_csv("sample_data.csv")
COUNTRIES = retrieve_countries(df)


# Create list of DAYS_TO_RECORD points for line graph
# Usage time is in HRS
def accumulate_data(df):

    country_aggregate = {"Countries":COUNTRIES,
                        "Total Usage Time":[0 for i in range(len(COUNTRIES))],
                        "Total Bytes Used":[0 for i in range(len(COUNTRIES))]}

    for i in range(len(COUNTRIES)):

        df_temp = df[df['COUNTRY_ISO3'].str.match(COUNTRIES[i])]
        for index, row in df_temp.iterrows():

            # Usage time is in HRS
            diff = row["CLOSE_TIME"] - row["CONNECT_TIME"]
            total_hours = diff.total_seconds() / 3600
            country_aggregate["Total Usage Time"][i] += total_hours

            # Total Bytes Used is in MB
            country_aggregate["Total Bytes Used"][i] += int(row["DURATION"]) / (1E9)

    return country_aggregate


def main(df=df):
    df = country_limit_zero_remove(df, COUNTRIES)
    df = time_limit(df, DAYS_TO_RECORD)
    country_aggregate = accumulate_data(df)

    new_df = pd.DataFrame(country_aggregate, columns=["Countries", "Total Usage Time", "Total Bytes Used"])


    # if (DISPLAY=="Total Bytes Used"): new_df = new_df.drop("Total Usage Time", axis=1)
    # else: new_df = new_df.drop("Total Bytes Used", axis=1)
    new_df = new_df.sort_values(DISPLAY, ascending=False)


    # fig = px.bar(new_df, x="Countries", y=DISPLAY,
    #              labels={"Countries":"Country",
    #                     "Total Bytes Used":"Total Bytes Used (GB)",
    #                     "Total Usage Time":"Total Usage Time (HRs)"}
    # )

    fig = go.Figure()
    fig.add_trace(go.Histogram(histfunc="sum", y=list(new_df["Total Bytes Used"]), x=list(new_df["Countries"]), name="Total Bytes Used (GB)"))
    fig.add_trace(go.Histogram(histfunc="sum", y=list(new_df["Total Usage Time"]), x=list(new_df["Countries"]), name="Total Usage Time (HRS)", marker_color='#330C73'))

    time = str(DAYS_TO_RECORD) + " Days"
    fig.update_layout(
            title="Total Data Usage Over {} by Country".format(time),
    )
    fig.update_yaxes(type='log')

    fig.show()

if __name__=="__main__":
    main()
