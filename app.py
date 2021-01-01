import pandas as pd
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                'content': 'width-device-didth, initial-scale-1.0'}])

server = app.server

months = ['January','February','March','April','May','June'
        ,'July','August','September','October','November','December']

df = pd.read_csv('db_csv.csv')
df = df[df['year']!=2017]

month_year_group = df.groupby(['year','month_name'])['sales_amount'].sum()
month_year_group = month_year_group.reindex(months, level='month_name').reset_index()

app.layout = dbc.Container([

    dbc.Row([
            dbc.Col(html.H1("web application, sales by year",
            style={'text-align':'center'},
            className='mb-5'),width=12)
    ]),

    dbc.Row([

        dbc.Col([

            dcc.Dropdown(
                id='year',
                options=[{'label':x, 'value':x}
                                   for x in sorted(month_year_group['year'].unique())],

                multi=False,
                value=2020,
                style={'width':'40%'}
                ),

            dcc.Graph(id='revenue', figure={})],
            xs=12, sm=12, md=12, lg=6, xl=6
                ),

       dbc.Col([

            dcc.Checklist(id='year2', value=[2018,2019,2020],
                          options=[{'label':x, 'value':x}
                                   for x in sorted(month_year_group['year'].unique())],
                          labelClassName="mr-3"),

            dcc.Graph(id='month_year', figure={})],
            xs=12, sm=12, md=12, lg=6, xl=6
                )

    ], justify='center'),

    dbc.Row([

        ])


    ])




# ----- figure 1 call back and plot
@app.callback(
    # outputs 1
    Output('revenue','figure'),
    # input from user
    Input('year', 'value')
)

def update_graph(option_selected):

    dff = df.copy()
    dff = dff[dff['year']== option_selected]

    fig = px.pie(
        dff,
        values='sales_amount',
        names='markets_name',
        title=f'revenue by market for year {option_selected}'
        )

    return fig


# ------ figure 2 call back and plot
@app.callback(
    Output('month_year', 'figure'),
    Input('year2', 'value')
)

def update_graph(values):
    print(values)
    temp = month_year_group[month_year_group['year'].isin(values)]
    fig2 = px.line(temp, x="month_name", y='sales_amount', color='year')
    fig2.update_xaxes(type='category', tick0='January')

    return fig2

if __name__ == '__main__':
  app.run_server()