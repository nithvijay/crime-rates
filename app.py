import dash
import pandas as pd
import time
import dash_core_components as dcc
import dash_html_components as html
#import plotly_express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots




nyc = pd.read_csv("/Users/nvijayakumar/OneDrive/Workspace/Projects/NodeFinalProject/NYCArrests.csv")
nyc["ARREST_DATETIME"] = pd.to_datetime(nyc["ARREST_DATE"], cache=True)

sp500 = pd.read_csv("/Users/nvijayakumar/OneDrive/Workspace/Projects/NodeFinalProject/S&P500.csv")
sp500["Date"] = pd.to_datetime(sp500["Date"])

to_merge1 = sp500.loc[
    sp500["Date"].isin(nyc["ARREST_DATETIME"].value_counts().index), ["Date", "Close"]
]
to_merge2 = (
    nyc["ARREST_DATETIME"]
    .value_counts()
    .reset_index(name="Num Arrests")
    .rename({"index": "Date"}, axis=1)
)

daily = pd.merge(to_merge1, to_merge2)
daily.columns

daily["Year"] = daily["Date"].dt.year
daily["Week"] = daily["Date"].dt.week
daily["Month"] = daily["Date"].dt.month

weekly = daily.groupby(["Year", "Week"]).mean().reset_index()

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])]
        +
        # Body
        [
            html.Tr([html.Td(dataframe.iloc[i][col]) for col in dataframe.columns])
            for i in range(min(len(dataframe), max_rows))
        ]
    )


app.layout = html.Div(
    children=[
        html.H1(children="Dash Test"),
        # generate_table(sp500),
        html.Div(
            children="""
        Dash: A web application framework for Python.
    """
        ),
        dcc.Markdown(
            """
            # Markdown Test
            This is pretty cool
            - item 1
            - item 2
            *emphasis*
            """
        ),
        html.Div(
            id="radio-items",
            children=dcc.RadioItems(
                id="radio-test",
                options=[
                    {"label": "New York City", "value": "NYC"},
                    {"label": "Montréal", "value": "MTL"},
                    {"label": "San Francisco", "value": "SF"},
                ],
                value="MTL",
            ),
        ),
        #dcc.Graph(id="example-graph"),
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


# @app.callback(Output("example-graph", "figure"), [Input("radio-test", "value")])
# def update(title):
#     return px.scatter(x=sp500.loc[:1000, "Date"], y=sp500.loc[:1000, "Close"])


@app.callback(Output("weekly-by-year", "figure"), [Input("years-slider", "value")])
def update_weekly_app(year):
    return update_weekly(year)

def update_weekly(year):
    weekly_by_year = weekly.loc[
        weekly["Year"] == year, ["Week", "Close", "Num Arrests", "Month"]
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


if __name__ == '__main__':
    app.run_server(debug=True)