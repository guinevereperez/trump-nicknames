# -*- coding: utf-8 -*-
import pandas as pd
from dash import Dash, dcc, html, dash_table
import plotly.express as px

# Load data
df = pd.read_csv("../data/nicknames_master.csv")

# Create Dash app
app = Dash(__name__)
app.title = "Trump Nicknames Dashboard"

# Layout
app.layout = html.Div([
    html.H1("Trump Nicknames Dataset", style={"textAlign": "center"}),

    dash_table.DataTable(
        id="nickname-table",
        columns=[{"name": col, "id": col} for col in df.columns],
        data=df.to_dict("records"),
        filter_action="native",
        sort_action="native",
        page_size=20,
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "left", "padding": "5px", "minWidth": "100px", "maxWidth": "300px"},
    ),

    html.H2("Sentiment Breakdown", style={"marginTop": "30px"}),

    dcc.Graph(
        id="sentiment-chart",
        figure=px.histogram(df, x="Sentiment", title="Nickname Sentiment Distribution")
    )
])

# Run app
if __name__ == "__main__":
    app.run(debug=True)

