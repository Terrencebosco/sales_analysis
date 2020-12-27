import pandas as pd
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


app = dash.Dash(__name__)
server = app.server

df = pd.read_csv('db_csv.csv')

# -----
# app.layout

app.layout = html.Div([

    html.H1("web application, sales by year", style={'text-align':'center'}),

    dcc.Dropdown(
        id='year',
        options=[
            {"label": "2020", "value":2020},
            {"label": "2019", "value":2019},
            {"label": "2018", "value":2018},
            {"label": "2017", "value":2017}],

        multi=False,
        value=2020,
        style={'width':'40%'}
        ),

    html.Div(id='output_container', children=[]),  # output 1
    html.Br(),

    dcc.Graph(id='revenue', figure={})  # output 2
])

# -----
# connect the plotly graph with dash components

@app.callback(
    # outputs 1 & 2
    [Output(component_id='output_container', component_property='children'),
    Output(component_id='revenue', component_property='figure')],

    # input from user
    [Input(component_id='year', component_property='value')]
)

# if we had two inputs we would need two arguments. since we only have one input
# we have one argument // TODO play with two inputs. (refers to input value)

def update_graph(option_selected):
    print(option_selected)
    print((type(option_selected)))

    container = "year: {}".format(option_selected)

    dff = df.copy()
    dff = dff[dff['year']== option_selected]

    fig = px.pie(
        dff,
        values='sales_amount',
        names='markets_name',
        title=f'revenue by market for year {option_selected}'
        )

    return container, fig



if __name__ == '__main__':
  app.run_server()