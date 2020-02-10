# Import required libraries
import pickle
import copy
import pathlib
import dash
import math
from datetime import datetime, timedelta
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

# Import plots and data cleaning functions
import dataclean as clean
import line_plot
import heatmap_1


# Retrieve relative folder and load data
PATH = pathlib.Path(__file__).parent
df = pd.read_csv(PATH.joinpath("sample_data.csv"), low_memory=False)
COUNTRIES = clean.retrieve_countries(df) # ISO_3 format


# Create controls
country_options = [{'label': i, 'value': i} for i in COUNTRIES]


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server


app.layout = html.Div([
    html.Div(
        [
            dcc.Markdown('''
                Celitech
                '''
            ),

        ], style = {'text-align': 'center', 'margin-bottom': '15px'}
    ),

    html.Div([

        html.P("Filter by Country", className="control_label"),
                        dcc.RadioItems(
                            id="country_selector",
                            options=[
                                {"label": "All ", "value": "all"},
                                {"label": "Customize", "value": "custom"},
                            ],
                            value="all",
                            labelStyle={"display": "inline-block"},
                            className="dcc_control",
                        ),
                        dcc.Dropdown(
                            id="country_selections",
                            options=country_options,
                            multi=True,
                            value=COUNTRIES,
                            className="dcc_control",
                        ),
        html.P('Days Since Present', className="control_label"),
                        dcc.Input(
                            id="days_since_present",
                            min=1,
                            value=365,
                            type='number'
                        )
    ]),
        dcc.Graph(id = 'line_plot_4'),
        dcc.Graph(id = 'heatmap_1')
])


# Radio -> multi
@app.callback(
    Output("country_selections", "value"), [Input("country_selector", "value")]
)
def display_country(selector):
    if selector == "all":
        return COUNTRIES
    return []


@app.callback(
    Output('line_plot_4', 'figure'),
    [
        Input('country_selections', 'value'),
        Input('days_since_present', 'value')
    ]
)
def create_line_plot_4(country_selections, days_since_present):
    dff = df[df['COUNTRY_ISO3'].isin(country_selections)]
    dff = clean.time_limit(dff, days_since_present)
    num_data = line_plot.accumulate_data(dff, days_since_present)
    num_days = [i+1 for i in range(days_since_present)]
    return({
        'data': [ go.Scatter(
            x = num_days,
            y = num_data,
            opacity = 0.7)
        ],
        'layout': go.Layout(
            title = "Total Cellular Used per Day",
            xaxis_title = "Days Since Present",
            yaxis_title = "Hours of Cellular Data"
        )
    })

@app.callback(
    Output('heatmap_1', 'figure'),
    [
        Input('days_since_present', 'value')
    ]
)
def create_heatmap_1(days_since_present):
    time = [i for i in range(24)] # Y-axis
    dff = clean.time_limit(df, days_since_present)
    hour_density = heatmap_1.accumulate_data(dff).astype(int) # Convert back for compatibility with plotly
    return({
        'data': [ go.Heatmap(
        z = hour_density,
        x = COUNTRIES,
        y = time,
        colorscale = 'Viridis')
        ],
        'layout': go.Layout(
            title='Length of Average Connection Opened Each Hour',
            xaxis_title="Countries",
            yaxis_title="Time of the Day",
            yaxis=dict(autorange='reversed')
        )
    })

if __name__ == "__main__":
    app.run_server(debug=True)

