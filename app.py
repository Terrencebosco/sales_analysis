import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

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

## do this before loading in data ##
df = pd.read_csv('db_csv.csv')
df = df[df['year']!=2017]

month_year_group = df.groupby(['year','month_name'])['sales_amount'].sum()
month_year_group = month_year_group.reindex(months, level='month_name').reset_index()

app.layout = dbc.Container([
    # header
    dbc.Row([
            dbc.Col(html.H1("web application, sales by year",
            style={'text-align':'center'},
            className='mb-5'),width=12)
    ]),

    # year revenue over time
    dbc.Row([

            dbc.Col([

            dcc.Checklist(id='year2', value=[2018,2019,2020],
                          options=[{'label':x, 'value':x}
                                   for x in sorted(month_year_group['year'].unique())],
                          labelClassName="mr-3"),

            dcc.Graph(id='month_year', figure={})],
            xs=12, sm=12, md=12, lg=12, xl=12
                )
    ]),

    # second row of graphs
    dbc.Row([

        # pie: year breakdown revenue by market
        dbc.Col([
            dcc.Dropdown(
                id='year',
                options=[{'label':x, 'value':x}
                                   for x in sorted(month_year_group['year'].unique())],
                multi=False,
                value=2020,
                style={'width':'50%'}
                ),

            dcc.Graph(id='revenue', figure={})],
            xs=12, sm=12, md=12, lg=6, xl=6
                ),

        # bar: customer contrbution by seperated by buisness type.
        dbc.Col([
            dcc.Graph(id='customer_type', figure={})],
            xs=12, sm=12, md=12, lg=6, xl=6
                )

    ], align='center'),

    dbc.Row([
        dbc.Col([

            dcc.Dropdown(
                id='year3',
                options=[{'label':x, 'value':x}
                                   for x in sorted(month_year_group['year'].unique())],
                multi=False,
                value=2020,
                style={'width':'62%'}
                ),

            dcc.Input(
                id='look_at',
                placeholder='Value between 0 and 259',
                type='number',
                value=5,
                min=0,
                max=259
                ),

            dcc.Dropdown(
                id='market',
                options=[{'label':x, 'value':x}
                                   for x in sorted(df['markets_name'].unique())],
                multi=False,
                value='Mumbai',
                style={'width':'62%'}
                ),

            dcc.Graph(id='market_product_bar', figure={})],
            xs=12, sm=12, md=12, lg=6, xl=6
                ),

        dbc.Col([
            dcc.Graph(id='market_product_pie', figure={})],
            xs=12, sm=12, md=12, lg=6, xl=6
                )

        ],align='center')

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
        title=f'revenue by market for year {option_selected}',
        )
    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig


# ------ figure 2 call back and plot
@app.callback(
    Output('month_year', 'figure'),
    Input('year2', 'value')
)

def update_graph(values):
    temp = month_year_group[month_year_group['year'].isin(values)]
    fig2 = px.line(temp, x="month_name", y='sales_amount', color='year')
    fig2.update_xaxes(type='category', tick0='January')
    fig2.update_layout(hovermode="x")
    return fig2


# ----- figure 3 -----
@app.callback(
    Output('customer_type', 'figure'),
    Input('year', 'value')
)

def update_graph(option_selected):
    dff = df.copy()
    dff = dff[dff['year']== option_selected]

    customer_type_sum = dff.groupby(['customer_type'])['sales_amount'].sum().reset_index()
    bm = customer_type_sum.iloc[0][1].round(2)
    ec = customer_type_sum.iloc[1][1].round(2)

    customer_sales = dff.groupby(['custmer_name','customer_type'])['sales_amount'].sum().reset_index()

    fig = px.bar(customer_sales, x='custmer_name', y='sales_amount', color='customer_type',
                title = f'Brick & Mortar sales: {bm:,} , E-Commerce sales: {ec:,}')
    fig.update_layout(hovermode="x")

    return fig

# ----- figure 4 -----
@app.callback(
    Output('market_product_bar', 'figure'),
    [Input('year3', 'value'),
    Input('look_at', 'value'),
    Input('market', 'value')]
)

# bar_product_market
# year, market, look_at
def update_graph(year, look_at, market):

    dff = df.query(f'year=={year}')
    total_products = total_products = len(dff[dff['markets_name']==market]['product_code'].unique())
#     look_at = 5
    temp = dff[dff['markets_name']==market]['product_code'].value_counts().head(look_at)
    fig = px.bar(temp, y=temp.values, x=temp.index,
                 title=f'top {look_at} out of {total_products} products sold in {market}')

    return fig

# ----- figure 5 ----
@app.callback(
    Output('market_product_pie', 'figure'),
    [Input('year3', 'value'),
    Input('look_at', 'value'),
    Input('market', 'value')]
)

def update_graph(year, look_at, market):

    #data
    dff = df.query(f'year=={year}')

    # get n out of total to show percent of total
    total = len(dff['product_code'].unique())
    zeros = np.zeros(total)
    pull = [.1] * int(look_at)
    test = list(np.concatenate([pull, zeros[10:]]))

    # expand 'look_at' amount for pie chart
    explode = len(dff['product_code'].unique())
    product_out_of_100 = dff[dff['markets_name']==market]['product_code'].value_counts()

    product_out_of_100.sum()
    fig = go.Figure(data=[go.Pie(labels=product_out_of_100.index, values=product_out_of_100.values, pull=test)])
    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig

if __name__ == '__main__':

    app.run_server(debug=True)

    #TODO
    # check spelling of custmer_names to customer_names. line142