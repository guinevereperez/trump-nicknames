# -*- coding: utf-8 -*-
import pandas as pd
import dash
from dash import dcc, html, dash_table, Input, Output, State
import plotly.express as px
import flask

# Load data
DATA_PATH = '../data/nicknames_master.csv'
df = pd.read_csv(DATA_PATH)

# Ensure all expected columns are present
for col in ['Nickname', 'Source Type', 'Specific Source Name', 'Context', 'Sentiment Score', 'Media Format', 'Region', 'Language', 'Tags']:
    if col not in df.columns:
        df[col] = ''

# Dash app setup
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([
    html.H1("Trump Nicknames Dashboard", style={"textAlign": "center"}),

    html.Div([
        dcc.Input(id='search-input', type='text', placeholder='Search nicknames or context...', debounce=True, style={'width': '100%'}),
        html.Br(), html.Br(),

        html.Div([
            html.Label("Filter by Source Type"),
            dcc.Dropdown(
                id='source-type-filter',
                options=[{"label": src, "value": src} for src in sorted(df['Source Type'].dropna().unique())],
                multi=True
            )
        ]),

        html.Div([
            html.Label("Filter by Sentiment Score"),
            dcc.RangeSlider(
                id='sentiment-filter',
                min=-1, max=1, step=0.1,
                value=[-1, 1],
                marks={-1: "-1", 0: "0", 1: "1"}
            )
        ]),

        html.Div([
            html.Label("Filter by Tags"),
            dcc.Dropdown(
                id='tags-filter',
                options=[{"label": tag, "value": tag} for tag in sorted(set(
                    t.strip() for tags in df['Tags'].dropna() for t in str(tags).split(",")
                ))],
                multi=True
            )
        ]),

        html.Button("Download CSV", id="btn-csv"),
        dcc.Download(id="download-dataframe-csv"),

        html.Hr(),

        dash_table.DataTable(
            id='nickname-table',
            columns=[{"name": col, "id": col} for col in df.columns],
            page_size=15,
            filter_action='native',
            sort_action='native',
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '5px'},
            style_header={'fontWeight': 'bold'}
        )
    ], style={'width': '80%', 'margin': 'auto'}),

    html.H2("Sentiment Distribution", style={"textAlign": "center"}),
    dcc.Graph(id='sentiment-chart'),

    html.H2("Top Sources", style={"textAlign": "center"}),
    dcc.Graph(id='top-sources-chart')
])

@app.callback(
    Output('nickname-table', 'data'),
    Output('sentiment-chart', 'figure'),
    Output('top-sources-chart', 'figure'),
    Input('search-input', 'value'),
    Input('source-type-filter', 'value'),
    Input('sentiment-filter', 'value'),
    Input('tags-filter', 'value')
)
def update_dashboard(search, selected_sources, sentiment_range, selected_tags):
    filtered_df = df.copy()

    if search:
        filtered_df = filtered_df[
            filtered_df.apply(lambda row: search.lower() in str(row).lower(), axis=1)
        ]

    if selected_sources:
        filtered_df = filtered_df[filtered_df['Source Type'].isin(selected_sources)]

    if sentiment_range:
        filtered_df = filtered_df[
            (filtered_df['Sentiment Score'] >= sentiment_range[0]) &
            (filtered_df['Sentiment Score'] <= sentiment_range[1])
        ]

    if selected_tags:
        filtered_df = filtered_df[
            filtered_df['Tags'].apply(lambda tags: any(tag.strip() in tags for tag in selected_tags))
        ]

    pie_chart = px.pie(
        filtered_df, names='Sentiment Score',
        title='Sentiment Distribution'
    )
    bar_chart = px.bar(
        filtered_df['Specific Source Name'].value_counts().head(10).reset_index(),
        x='index', y='Specific Source Name',
        labels={'index': 'Source', 'Specific Source Name': 'Count'},
        title='Top 10 Sources'
    )
