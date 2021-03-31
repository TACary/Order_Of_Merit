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

totals = df[df['Event']=='Total']
totals = totals[['Player','Rank','Points']]
df = df.astype({'Points': 'int32'})
fig_totals = ff.create_table(totals)

fig_totals.update_layout(width=500)

df = df[df['Event']!='Total']

df=df.astype({'Front 9': 'int32','Back 9': 'int32','Total Gross': 'int32','Total Net': 'int32'})


Event = df['Event'].unique()

fig = ff.create_table(df)

app = dash.Dash(__name__)
server = app.server
fig_totals = ff.create_table(totals)
fig_totals.update_layout(width=500)

app.layout = html.Div(children=[
    html.H1(
        children='Order Of Merit Standings',
        style={
            'textAlign': 'center',
            'font-size':'50px'
        }
    ),
    

    dcc.Graph(figure=fig_totals,
              style={'display':'block','margin-right':'Auto','margin-left':'Auto','width': '50%'}
             ),

    
    html.H1(
        children='Event Results',
        style={
            'textAlign': 'center',
            'font-size':'50px'
        }
    ),
    
    html.Label('Select Event',style={'font-size':'20px'}),
    dcc.Dropdown(id='Event-select', options=[{'label': i, 'value': i} for i in Event],
                           value=Event[-1], style={'width': '140px','font-size':'20px'}
                ),
    
    dcc.Graph(
        id='table',
        figure=fig,
        style={'display':'block','margin-right':'Auto','margin-left':'Auto','width': '50%'}
    )
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