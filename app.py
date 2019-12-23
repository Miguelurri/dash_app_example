#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

app = dash.Dash()
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

df = pd.read_csv('nama_10_gdp_1_Data.csv')
available_items = df['NA_ITEM'].unique()
available_locations = df['GEO'].unique()
available_units = df['UNIT'].unique()
available_time = df['TIME'].unique()

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            id='xaxis-column-a',
            options=[{'label': i, 'value': i} for i in available_items],
            value='Gross domestic product at market prices'
        )], style={'width': '48%', 'display': 'inline-block'}),
    html.Div([
        dcc.Dropdown(
            id='yaxis-column-a',
            options=[{'label': i, 'value': i} for i in available_items],
            value='Value added, gross'
        )], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        dcc.RadioItems(
            id='units-a',
            options=[{'label': i, 'value': i} for i in available_units],
            value='Chain linked volumes, index 2010=100'
        )], style={'width': '55%', 'margin': 'auto'}),

    dcc.Graph(id='output-a'),

    html.Div([dcc.Slider(
        id='year-slider-a',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}
    )], style={'width': '95%', 'margin': 'auto'}),

    # SECOND GRAPH

    html.Div([
        dcc.Dropdown(
            id='countries-b',
            options=[{'label': i, 'value': i} for i in available_locations],
            value='European Union - 28 countries'
        )], style={'width': '48%', 'display': 'inline-block'}),
    html.Div([
        dcc.Dropdown(
            id='yaxis-column-b',
            options=[{'label': i, 'value': i} for i in available_items],
            value='Value added, gross'
        )], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        dcc.RadioItems(
            id='units-b',
            options=[{'label': i, 'value': i} for i in available_units],
            value='Chain linked volumes, index 2010=100'
        )], style={'width': '55%', 'margin': 'auto'}),

    dcc.Graph(id='output-b')
])


@app.callback(
    dash.dependencies.Output('output-a', 'figure'),
    [dash.dependencies.Input('xaxis-column-a', 'value'),
     dash.dependencies.Input('yaxis-column-a', 'value'),
     dash.dependencies.Input('year-slider-a', 'value'),
     dash.dependencies.Input('units-a', 'value')])
def update_graph1(xaxis_column_name, yaxis_column_name,
                  year_value, units_value):
    dff = df[(df['TIME'] == year_value) & (df['UNIT'] == units_value)]
    return {'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
            )], 'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
            )
            }


@app.callback(
    dash.dependencies.Output('output-b', 'figure'),
    [dash.dependencies.Input('countries-b', 'value'),
     dash.dependencies.Input('yaxis-column-b', 'value'),
     dash.dependencies.Input('units-b', 'value')])
def update_graph2(countriess, yaxis_column_name, units_value):
    dff = df[(df['GEO'] == countriess) & (df['UNIT'] == units_value)]
    return {'data': [go.Scatter(
            x=dff[(dff['NA_ITEM'] == yaxis_column_name)]['TIME'],
            y=dff[(dff['NA_ITEM'] == yaxis_column_name)]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            mode='lines',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
            )], 'layout': go.Layout(
            xaxis={
                'title': 'Time',
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
            )
            }


if __name__ == '__main__':
    app.run_server(debug=False)
