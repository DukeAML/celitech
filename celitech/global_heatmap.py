import pandas as pd
import matplotlib.pyplot as plt
import pycountry
import plotly
import plotly.graph_objs as go
import json
from datetime import datetime

df = pd.read_csv("sample_data.csv")


# Global heat map
countries = {}
for country in pycountry.countries:
    countries[country.name] = country.alpha_3

country_dict = {}

for index, row in df.iterrows():
    country_name = str(row["COUNTRY_NAME"])
    country_code =  countries.get(country_name)
    duration = int(row["DURATION"])
    duration = duration/(1E6)
    if country_name in country_dict:
        country_dict[country_code] = country_dict[country_code] + duration
    else:
        country_dict[country_code] = duration

with open('heatmap/world_geojson.json') as file:
    world = json.load(file)

fig = go.Figure(go.Choroplethmapbox(geojson=world,locations=country_dict.keys(),z=country_dict.values(),
                                    colorscale='rainbow',zmin=0,zmax=90,
                                    marker_opacity=0.7, marker_line_width=0))
fig.update_layout(mapbox_style="carto-positron", mapbox_zoom = 1.5)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

# Show plots
fig.show()
