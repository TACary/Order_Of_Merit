# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 17:59:50 2021

@author: Tim
"""

import plotly.express as px
import plotly.figure_factory as ff
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

df = pd.read_csv(r"C:\Users\Tim\Documents\Python Scripts\OOM_results.csv")

Event = df['Event'].unique()

app = dash.Dash(__name__)
server = app.server


app.layout = html.Div([
    html.Div([dcc.Dropdown(id='Event-select', options=[{'label': i, 'value': i} for i in Event],
                           value='Event', style={'width': '140px'})]),
    dcc.Graph(id='table',figure=fig)
])

@app.callback(
    Output('table', 'figure'),
    [Input('Event-select', 'value')]
)
def update_graph(event):
    import plotly.express as px
    import plotly.figure_factory as ff
    return ff.create_table(df[df['Event']==event])

if __name__ == '__main__':
    app.run_server(debug=False)