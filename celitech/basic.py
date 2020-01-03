import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("sample_data.csv")

usage_dict = {}

for index, row in df.iterrows():
    ICCID = str(row["ICCID"])
    duration = int(row["DURATION"])
    duration = duration/(1E6)
    if ICCID in usage_dict:
        usage_dict[ICCID] = usage_dict[ICCID] + duration
    else:
        usage_dict[ICCID] = duration


plt.bar(range(1, len(usage_dict)+1), usage_dict.values())
plt.xticks(range(1, len(usage_dict)+1), usage_dict.keys(), rotation=90)
plt.ylabel("Data Usage (MB)")
plt.xlabel("ICCID")
plt.show()
