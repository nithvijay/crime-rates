import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

daily = pd.read_csv(
    "https://raw.githubusercontent.com/nithvijay/crime-rates/master/daily.csv",
    parse_dates=["Date"],
)
daily["UnixTime"] = daily["Date"].astype(np.int64)
weekly = pd.read_csv(
    "https://raw.githubusercontent.com/nithvijay/crime-rates/master/weekly.csv"
)

def make_2y_axis_plot(x, y1, trace_1, y2, trace_2, y1_title, y2_title, graph_title):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(x=x, y=y1, name=trace_1, mode="markers", yaxis="y1",),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(x=x, y=y2, name=trace_2, yaxis="y2",), secondary_y=True,
    )
    fig.update_layout(
        xaxis={"zeroline": False},
        title=graph_title,
        transition={"duration": 1000},
        yaxis1={"title": y1_title},
        yaxis2={"title": y2_title},
    )
    return fig

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
daily["Month-Year"] = daily["Month"].astype(str) + "/" + daily["Year"].astype(str)
marks_df = daily.loc[:: (int(daily.shape[0] / 30)), ["UnixTime", "Month-Year"]].rename(
    {"Month-Year": "label"}, axis=1
)
marks_df["style"] = [
    {"writing-mode": "vertical-lr", "margin-bottom": "1000px"}
    for i in range(marks_df.shape[0])
]
marks = marks_df.set_index("UnixTime").to_dict("index")
marks

sp_options = ["Open", "Close", "Volume"]
col_options_sp = [dict(label=x, value=x) for x in sp_options]
weather_options = ["Mean.TemperatureF", "PrecipitationIn"]
col_options_weather = [dict(label=x, value=x) for x in weather_options]

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                dcc.Markdown(
                    """
            # Node Final Project
            ## New York City Crime Analysis from 2006-2015
            
            ### Introduction
            We chose to examine New York City crime data along with weather and S&P500 stock data 
            to discern any possible trends and make assumptionsWe chose to examine New York City crime data along with weather and S&P500 stock data 
            to discern any possible trends and make assumptionsWe chose to examine New York City crime data along with weather and S&P500 stock data 
            to discern any possible trends and make assumptionsWe chose to examine New York City crime data along with weather and S&P500 stock data 
            to discern any possible trends and make assumptionsWe chose to examine New York City crime data along with weather and S&P500 stock data 
            to discern any possible trends and make assumptionsWe chose to examine New York City crime data along with weather and S&P500 stock data 
            to discern any possible trends and make assumptionsWe chose to examine New York City crime data along with weather and S&P500 stock data 
            to discern any possible trends and make assumptionsWe chose to examine New York City crime data along with weather and S&P500 stock data 
            to discern any possible trends and make assumptionsWe chose to examine New York City crime data along with weather and S&P500 stock data 
            to discern any possible trends and make assumptionsWe chose to examine New York City crime data along with weather and S&P500 stock data 
            to discern any possible trends and make assumptionsWe chose to examine New York City crime data along with weather and S&P500 stock data 
            to discern any possible trends and make assumptionsWe chose to examine New York City crime data along with weather and S&P500 stock data 
            to discern any possible trends and make assumptionsWe chose to examine New York City crime data along with weather and S&P500 stock data 
            to discern any possible trends and make assumptionsWe chose to examine New York City crime data along with weather and S&P500 stock data 
            to discern any possible trends and make assumptionsWe chose to examine New York City crime data along with weather and S&P500 stock data 
            to discern any possible trends and make assumptionsWe chose to examine New York City crime data along with weather and S&P500 stock data 
            to discern any possible trends and make assumptionsWe chose to examine New York City crime data along with weather and S&P500 stock data 
            to discern any possible trends and make assumptions
            
            ### Datasets
            
            1. NYC Crime Data
            - explanation:
            - cleaning we had to do:
            - link:
            
            2. S&P 500 Prices
            - explanation:
            - cleaning we had to do:
            - link:
            
            3. Weather
            - explanation:
            - cleaning we had to do:
            - link:
            
            We merged based on Date, all three overlapped from 2006-2015. Stock market is not open everyday, 
            so data is sporadic **Insert figure/statistic on how much data we have and how many data points we have per year**
            
            
            ### Basic Correlation
            """
                ),
                html.Div(
                    [
                        html.P(children="Select what to graph"),
                        dcc.RadioItems(
                            id="radio-initial",
                            options=[
                                {"label": "S&P500", "value": "sp"},
                                {"label": "NYC Weather Data", "value": "weather"},
                            ],
                            value="sp",
                        ),
                    ]
                ),
                html.Div(
                    [
                        html.P(children="Select column to graph"),
                        dcc.RadioItems(
                            id="y2_selector",
                            options=col_options_sp,
                            value=col_options_sp[0]["value"],
                        ),
                    ]
                ),
            ],
            style={
                "marginLeft": "15%",
                "marginRight": "15%",
                "marginTop": 20,
                "marginBottom": 20,
                "border": "thin lightgrey",
                "padding": "6px 0px 0px 8px",
            },
        ),
        dcc.Graph(id="weekly-by-year"),
        html.Div(
            children=dcc.Slider(
                id="years-slider",
                min=weekly["Year"].min(),
                max=weekly["Year"].max(),
                value=weekly["Year"].min(),
                marks={
                    str(year): {"label": str(year)} for year in weekly["Year"].unique()
                },
            ),
            style={"padding": "0px 20px 20px 20px"},
        ),
        html.Br(),
        dcc.Graph(id="daily_graph"),
        html.Div(
            [
                dcc.RangeSlider(
                    id="daily-range-slider",
                    min=daily["UnixTime"].min(),
                    max=daily["UnixTime"].max(),
                    value=[daily["UnixTime"].min(), daily["UnixTime"].max()],
                    marks=marks,
                )
            ]
        ),
    ]
)


@app.callback(
    [Output("y2_selector", "options"), Output("y2_selector", "value")],
    [Input("radio-initial", "value")],
)
def update_radio_items(value):
    if value == "sp":
        return [col_options_sp, col_options_sp[0]["value"]]
    else:
        return [col_options_weather, col_options_weather[0]["value"]]


@app.callback(
    Output("weekly-by-year", "figure"),
    [Input("years-slider", "value"), Input("y2_selector", "value")],
)
def update_weekly_app(year, col):
    if col in sp_options:
        description = "S&P 500 " + col
    else:
        description = col
    weekly_by_year = weekly[weekly["Year"] == year]
    fig = make_2y_axis_plot(
        x=weekly_by_year["Week"],
        y1=weekly_by_year["Num Arrests"],
        trace_1="Number of Arrests Weekly",
        y2=weekly_by_year[col],
        trace_2=description,
        y1_title="Number of Arrests",
        y2_title=description,
        graph_title="This is a weekly graph",
    )
    fig.update_xaxes(
        ticktext=[
            "January",
            "March",
            "June",
            "August",
            "October",
            "December",
        ],  # 1, 3, 6, 8, 10, 12
        tickvals=[1, 10, 20, 30, 40, 50],
    )
    return fig


@app.callback(
    [Output("daily_graph", "figure")],
    [Input("daily-range-slider", "value"), Input("y2_selector", "value")],
)
def update_daily(value, col):
    print(value)
    date_begin = datetime.fromtimestamp(value[0] / 1e9)
    date_end = datetime.fromtimestamp(value[1] / 1e9)
    daily_by = daily[(daily["Date"] > date_begin) & (daily["Date"] < date_end)]
    if col in sp_options:
        description = "S&P 500 " + col
    else:
        description = col
    fig = make_2y_axis_plot(
        x=daily_by["Date"],
        y1=daily_by["Num Arrests"],
        trace_1="Number of Arrests Daily",
        y2=daily_by[col],
        trace_2=description,
        y1_title="Number of Arrests",
        y2_title=description,
        graph_title="This is a daily graph",
    )
    return [fig]


if __name__ == "__main__":
    app.run_server(debug=True)