import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

daily = pd.read_csv('https://raw.githubusercontent.com/nithvijay/crime-rates/master/daily.csv')
weekly = pd.read_csv('https://raw.githubusercontent.com/nithvijay/crime-rates/master/weekly.csv')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def update_weekly(year):
    weekly_by_year = weekly.loc[
        weekly["Year"] == year,
        ["Week", "Close", "Num Arrests", "Month", "Mean.TemperatureF"],
    ]
    fig = go.Figure()
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=weekly_by_year["Week"],
            y=weekly_by_year["Num Arrests"],
            name="Number of Crimes",
            mode="markers",
            yaxis="y1",
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=weekly_by_year["Week"],
            y=weekly_by_year["Close"],
            name="S&P500 Close Price",
            yaxis="y2",
        ),
        secondary_y=True,
    )
    fig.update_xaxes(
        ticktext=[
            "January",
            "March",
            "June",
            "August",
            "October",
            "December",
        ],  # 1, 3, 5, 7, 9, 11
        tickvals=[1, 10, 20, 30, 40, 50],
    )
    fig.update_layout(
        xaxis={"zeroline": False},
        title=year,
        transition={"duration": 1000},
        yaxis1={"title": "Number of Arrests"},
        yaxis2={"title": "S&P"},
    )
    print(year)
    return fig


app.layout = html.Div(
    children=[
        html.H1(children="Dash Test"),
        html.Div(
            children="""
                     Dash: A web application framework for Python.
                     """
        ),
        html.Div(
            id="radio-items",
            children=dcc.RadioItems(
                id="radio-test",
                options=[
                    {"label": "New York City", "value": "NYC"},
                    {"label": "Montréal", "value": "MTL"},
                ],
                value="MTL",
            ),
        ),
        # dcc.Graph(id="example-graph"),
        html.H3(id="graph-title", children="This is the graph title"),
        dcc.Graph(id="weekly-by-year"),
        dcc.Slider(
            id="years-slider",
            min=weekly["Year"].min(),
            max=weekly["Year"].max(),
            value=weekly["Year"].min(),
            marks={str(year): {"label": str(year)} for year in weekly["Year"].unique()},
        ),
        html.Br(),
    ]
)

@app.callback(Output("weekly-by-year", "figure"), [Input("years-slider", "value")])
def update_weekly_app(year):
    return update_weekly(year)

if __name__ == '__main__':
    app.run_server(debug=True)