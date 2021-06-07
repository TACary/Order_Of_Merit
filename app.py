import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc

import plotly.express as px
import pandas as pd
import plotly.figure_factory as ff

#url = 'https://raw.githubusercontent.com/TACary/Order_Of_Merit/OOM2/Data/OOM_results.csv'
df = pd.read_csv('OOM_results.csv')

#df=pd.read_csv('OOM_results.csv')

totals = df[df['Event']=='Total']
totals = totals[['Player','Points']]
df = df.astype({'Points': 'float64'})
fig_totals = ff.create_table(totals)

#fig_totals.update_layout(width=500)

df = df[df['Event']!='Total']

df=df.astype({'Front 9': 'int32','Back 9': 'int32','Total Gross': 'int32','Total Net': 'int32'})

df = df.drop(['Front 9','Back 9','Rank','Total Gross'],axis = 1)

Event = df['Event'].unique()

fig = ff.create_table(df)

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}]
                )

server=app.server

app.layout = html.Div([
    dbc.Row([
        dbc.Col([
            html.Div('Order of Merit Overall Standings',
                     style={'textAlign':'center', 'fontSize':30}),
            html.Br(),
        ], width={'size': 8})
    ], justify='center'),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(figure=fig_totals),
            html.Br(),
        ], xs=10, sm=8, md=5, lg=6, xl=5),
        ], justify="center"),
    
    dbc.Row([
        dbc.Col([
            html.Div('Event Results',
                     style={'textAlign':'center', 'fontSize':30}),
            html.Br(),
        ], width={'size': 8})
    ], justify='center'),
    
    dbc.Row([
        dbc.Col([
                html.P("Select Event:", style={'fontSize': 15}),
                dcc.Dropdown(id='Event-select', value=Event[-1],
                             options=[{'label': i, 'value': i} for i in Event],
                             ),
                dcc.Graph(id='table',figure=fig),
            ], xs=10, sm=5, md=5, lg=6, xl=5)
        ], justify="center")
])

@app.callback(
    Output('table', 'figure'),
    [Input('Event-select', 'value')]
)
def update_graph(event):
    import plotly.express as px
    import plotly.figure_factory as ff
    fig1=ff.create_table(df[df['Event']==event])
    #fig1.update_layout(margin={"r": 30, "t": 57, "l": 30, "b": 23})
    return fig1

if __name__ == '__main__':
    app.run_server(debug=False)
