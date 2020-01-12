import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import datetime

def getDateTime(dt):
    data_arr = dt.split('T')
    date = data_arr[0].split('-')
    time = data_arr[1].split('.')[0].split(':')
    return datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]), int(time[2]))
    
df = pd.read_csv("sample_data.csv")

durs = []
lens = []
starts = []
ends = []
date_dur = {}
date_len = {}

for index, row in df.iterrows():
    dt_start = row["CONNECT_TIME"]
    dt_close = row["CLOSE_TIME"]
    dur = int(row["DURATION"])/1000000
    start_date_time = getDateTime(dt_start)
    starts.append(start_date_time)
    end_date_time = getDateTime(dt_close)
    ends.append(end_date_time)
    len = end_date_time - start_date_time
    durs.append(dur)
    lens.append(len.seconds)
    if(start_date_time.date in date_dur):
        date_dur[start_date_time.date] = date_dur[start_date_time.date] + dur
    else:
        date_dur[start_date_time.date] = dur

    if(start_date_time.date in date_len):
        date_len[start_date_time.date] = date_len[start_date_time.date] + len
    else:
        date_len[start_date_time.date] = len

# plt.plot(lens, durs, 'b.')
plt.plot(starts, durs, 'b.')
plt.title("Duration vs. Length")
plt.xlabel("Duration")
plt.ylabel("Connection Length")
plt.show()
plt.clf()

