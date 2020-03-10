import pandas as pd
import matplotlib.pyplot as plt
import pycountry
import plotly
import plotly.graph_objs as go
import json
from datetime import datetime
from dataclean import BYTES_TO_MB

fig = go.Figure()

def make_heatmap(df, fig=fig):
    # Global heat map
    countries = {}
    for country in pycountry.countries:
        countries[country.name] = country.alpha_3

    country_dict = {}

    for index, row in df.iterrows():
        country_iso3 = str(row["COUNTRY_ISO3"])
        duration = int(row["DURATION"])
        duration = duration/BYTES_TO_MB
        if country_iso3 in country_dict.keys():
            country_dict[country_iso3] = country_dict[country_iso3] + duration
        else:
            country_dict[country_iso3] = duration

    with open('heatmap/world_geojson.json') as file:
        world = json.load(file)

    fig.add_trace(go.Choroplethmapbox(geojson=world,locations=list(country_dict.keys()),z=list(country_dict.values()),
                                        colorscale='Darkmint',zmin=0,zmax=90,
                                        marker_opacity=0.7, marker_line_width=0))
    fig.update_layout(mapbox_style="carto-positron", mapbox_zoom = 1.5)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

def main(df):
    make_heatmap(df)
    fig.show()

if __name__=="__main__":
    df = pd.read_csv("sample_data.csv")
    main(df)
