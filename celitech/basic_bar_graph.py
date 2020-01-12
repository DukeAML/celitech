import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("sample_data.csv")

id_dict = {}

# Iterate through data and measure data by user
for index, row in df.iterrows():
    ICCID = str(row["ICCID"])
    duration = int(row["DURATION"])
    duration = duration/(1E6) # bytes to MB
    
    if ICCID in id_dict:
        id_dict[ICCID] = id_dict[ICCID] + duration
    else:
        id_dict[ICCID] = duration

user_range = range(1, len(id_dict)+1)

# Generate plot
plt.bar(user_range, id_dict.values())
plt.xticks(user_range, id_dict.keys(), rotation=90)
plt.ylabel("Data Usage (MB)")
plt.xlabel("ICCID")
plt.title("Data Usage by User (July-September 2019)")

plt.show()