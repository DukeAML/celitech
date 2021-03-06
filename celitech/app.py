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
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px

# Import plots and data cleaning functions
import dataclean as clean
import line_plot
import heatmap_1
import polar_bar_chart
import bar_graph_2
import bar_graph_3
import global_heatmap

# Retrieve relative folder and load data
PATH = pathlib.Path(__file__).parent
df = pd.read_csv(PATH.joinpath("sample_data.csv"), low_memory=False)
COUNTRIES = clean.retrieve_countries(df) # ISO_3 format


# Create controls
country_options = [{'label': i, 'value': i} for i in COUNTRIES]

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server


app.layout = html.Div(
    [
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("celitech-logo.png"),
                            id="celitech-image",
                            style={
                                "height": "70px",
                                "width": "auto",
                                "margin-left": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Celitech",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Data Usage Overview", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [],
                    className="one-third column",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [

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
                    debounce=True,
                    type='number',
                    className="dcc_control"
                ),
                        html.P("Time Interval for Pie Chart", className="control_label"),
        dcc.RadioItems(
            id="polar_chart_time",
            options=[
                {"label": "By Day", "value": "DAY"},
                {"label": "By Month", "value": "MONTH"}
            ],
            value="MONTH",
            labelStyle={"display": "inline-block"},
            className="dcc_control"
        ),

                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [


                        html.Div(
                            [dcc.Graph(id="line_plot_4")],
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="polar_bar_chart")],
                    className="pretty_container five columns",
                ),
                html.Div(
                    [dcc.Graph(id="heatmap_1")],
                    className="pretty_container seven columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="bar_graph_3")],
                    className="pretty_container six columns",
                ),
                html.Div(
                    [dcc.Graph(id="bar_graph_2")],
                    className="pretty_container six columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="global_heatmap")],
                    className="pretty_container twelve columns"
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)



# Create callbacks
app.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="resize"),
    Output("output-clientside", "children"),
    [Input("line_plot_4", "figure"), Input("heatmap_1", "figure"),
    Input("bar_graph_2", "figure"), Input("bar_graph_3", "figure"), Input("polar_bar_chart", "figure"), Input("global_heatmap", "figure")],
)

# Country RadioItems
@app.callback(
    Output("country_selections", "value"), [Input("country_selector", "value")]
)
def display_country(selector):
    if selector == "all":
        return COUNTRIES
    return []

@app.callback(
    Output('global_heatmap', 'figure'),
    [
        Input('days_since_present', 'value')
    ]
)
def create_global_heatmap(days_since_present):
    # Doesn't currently use days_since_present, but could in the future
    fig = go.Figure()
    dff = clean.country_limit_zero_remove(df)
    global_heatmap.make_heatmap(dff, fig)
    fig.update_layout(
            #title="Aggregate Data Usage per Country in Bytes",
            autosize=True
    )
    return fig

@app.callback(
    Output('bar_graph_3', 'figure'),
    [
        Input('days_since_present', 'value')
    ]
)
def create_bar_graph_3(days_since_present):
    dff = clean.country_limit_zero_remove(df)
    dff = clean.time_limit(dff, days_since_present)
    country_aggregate = bar_graph_3.accumulate_data(dff, COUNTRIES)
    dff = pd.DataFrame(country_aggregate, columns=["Countries", "Average Connections per User", "Average GB per User", "Average Time per User"])
    dff = dff.sort_values("Average GB per User", ascending=False)

    fig = go.Figure()
    fig.add_trace(go.Histogram(histfunc="sum", y=list(dff["Average Connections per User"]), x=list(dff["Countries"]), name="Average Connections per User"))
    fig.add_trace(go.Histogram(histfunc="sum", y=list(dff["Average GB per User"]), x=list(dff["Countries"]), name="Average GB per User", marker_color='#330C73'))
    fig.add_trace(go.Histogram(histfunc="sum", y=list(dff["Average Time per User"]), x=list(dff["Countries"]), name="Average Minutes per User", marker_color='LightSkyBlue'))
    time = str(days_since_present) + " Days"
    fig.update_layout(
            title="Average User Data Usage Over {} by Country".format(time),
            autosize=True
    )
    fig.update_yaxes(type='log')

    return fig

@app.callback(
    Output('bar_graph_2', 'figure'),
    [
        Input('days_since_present', 'value')
    ]
)
def create_bar_graph_2(days_since_present):
    dff = clean.country_limit_zero_remove(df)
    dff = clean.time_limit(dff, days_since_present)
    country_aggregate = bar_graph_2.accumulate_data(dff, COUNTRIES)
    dff = pd.DataFrame(country_aggregate, columns=["Countries", "Total Usage Time", "Total Bytes Used"])
    dff = dff.sort_values("Total Bytes Used", ascending=False)

    fig = go.Figure()
    fig.add_trace(go.Histogram(histfunc="sum", y=list(dff["Total Bytes Used"]), x=list(dff["Countries"]), name="Total Bytes Used (GB)"))
    fig.add_trace(go.Histogram(histfunc="sum", y=list(dff["Total Usage Time"]), x=list(dff["Countries"]), name="Total Usage Time (HRS)", marker_color='#330C73'))
    time = str(days_since_present) + " Days"
    fig.update_layout(
            title="Total Data Usage Over {} by Country".format(time),
            autosize=True
    )
    fig.update_yaxes(type='log')

    return fig

@app.callback(
    Output('line_plot_4', 'figure'),
    [
        Input('country_selections', 'value'),
        Input('days_since_present', 'value')
    ]
)
def create_line_plot_4(country_selections, days_since_present):
    dff = clean.country_limit_zero_remove(df, country_selections)
    dff = clean.time_limit(dff, days_since_present)
    num_data,avg_mins = line_plot.accumulate_data(dff, days_since_present)
    num_days = [i+1 for i in range(days_since_present)]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
            x=num_days,
            y=num_data,
            line = dict(color='royalblue', width=2),
            name="Hours of Cellular Data",
            opacity = 0.5,
            text=[avg_mins[i] for i in range(days_since_present)],
            hovertemplate='%{x} Days, %{y:.1f} hrs' + ', %{text:.1f} avg hrs'
    ))

    fig.add_trace(go.Scatter(
            x=num_days,
            y=avg_mins,
            line = dict(color='#330C73', width=2),
            name = "Average Hours per User",
            opacity = 0.3,
            text=[num_data[i] for i in range(days_since_present)],
            hovertemplate='%{x} Days, %{text:.1f} hrs' + ', %{y:.1f} avg hrs'
    ))

    fig.update_layout(
            title="Total Cellular Used per Day",
            xaxis_title="Day",
            hovermode="closest",
            xaxis={'showspikes':True, 'spikemode':'across', 'spikethickness':1}
    )

    return fig

@app.callback(
    Output('heatmap_1', 'figure'),
    [
        Input('days_since_present', 'value')
    ]
)
def create_heatmap_1(days_since_present):
    time = [i for i in range(24)] # Y-axis
    dff = clean.country_limit_zero_remove(df)
    dff = clean.time_limit(df, days_since_present)
    hour_density = heatmap_1.accumulate_data(dff, COUNTRIES).astype(int) # Convert back for compatibility with plotly
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
            yaxis=dict(autorange='reversed'),
            autosize=True
        )
    })

@app.callback(
    Output('polar_bar_chart', 'figure'),
    [
        Input('country_selections', 'value'),
        Input('polar_chart_time', 'value')
    ]
)
def create_polar_bar_chart(country_selections, polar_chart_time):
    dff = clean.country_limit_zero_remove(df, country_selections)
    num_data = polar_bar_chart.select_data_on_timesplit(dff, "DURATION", polar_chart_time)
    num_splits = len(num_data)
    increments = [(x+1)*(360/num_splits) for x in range(num_splits)]
    time_int = polar_chart_time.lower().capitalize()

    return ({
        'data': [ go.Barpolar(
        r = num_data,
        theta = increments,
        text=[time_int + " " + str((x+1)) for x in range(365)],
        hovertemplate='%{r:.2f} GB' + ', %{text}',
        marker_color = px.colors.sequential.deep,)
        ],
        'layout': go.Layout(
            title="Total Gigabytes of Data Used on Each {} of All Years".format(time_int),
            autosize=True
        )
    })

if __name__ == "__main__":
    app.run_server(debug=True)

