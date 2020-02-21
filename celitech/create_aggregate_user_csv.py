import pandas as pd
import pathlib
from datetime import datetime, timedelta
import sys

import dataclean as dc

# Retrieve relative folder and load data
PATH = pathlib.Path(__file__).parent
df = pd.read_csv(PATH.joinpath("sample_data.csv"), low_memory=False)

# Create date format e.g. 11-Nov-19
DATE_FORMAT = "%d-%b-%y"


def create_xlsx(start, end):
    tstart = datetime.strptime(start, DATE_FORMAT)
    tend = datetime.strptime(end, DATE_FORMAT)
    df = pd.read_csv(PATH.joinpath("sample_data.csv"))
    df = dc.time_period(df, tstart, tend)


    USERS = list(df.ICCID.unique())
    total_days = (tend - tstart).days
    user_aggregate = {user:[] for user in USERS}

    for user in USERS:
        dff = df.loc[df.ICCID==int(user)]
        user_usage = [0 for i in range(total_days+1)]

        user_usage[0] = sum(dff['DURATION'])
        for i in range(total_days):
            current_day = tstart + timedelta(days=i)
            day_df = dff.loc[(dff['CONNECT_TIME'].dt.day==current_day.day)
                        & (dff['CONNECT_TIME'].dt.month==current_day.month)
                        & (dff['CONNECT_TIME'].dt.year==current_day.year)]
            user_usage[i+1] = sum(day_df['DURATION'])

        user_usage = [num / (1E6) for num in user_usage] # convert all to MB
        user_aggregate[user] = user_usage

    user_consumption_df = pd.DataFrame(data=user_aggregate).transpose()
    user_consumption_df.columns = (["Period Total (MB)"] +
        [datetime.strftime(
                tstart + timedelta(days=k), DATE_FORMAT)
                for k in range(total_days)]
        )


    user_consumption_df.to_excel(PATH.joinpath("Data-consumption-table.xlsx"),header=True)


def main(start="1-Jul-19", end="30-Sep-19"):
    create_xlsx(start, end)


if __name__=="__main__":
    main(sys.argv[1], sys.argv[2])

