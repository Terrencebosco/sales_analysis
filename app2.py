import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import json
import pandas as pd
import plotly.express as px


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

df = pd.read_csv('notebooks/updated_data.csv')

with open('notebooks/states_india.geojson') as f:
    india_geojson = json.load(f)

available_indicators = df['year'].unique()

app.layout = html.Div([
    html.Div([
        html.Div([

            dcc.Checklist(
                id='year',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value=[2020,2019,2018]
            ),

            dcc.RadioItems(
                id='crossfilter-xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ]),

        html.Div([
        dcc.Graph(
            id='test'
        )
        ])
    ])
])


@app.callback(
    # outputs 1
    Output('test','figure'),
    # input from user
    Input('year', 'value')
)

def update_graph(values):
    temp = df[df['year'].isin(values)]

    t = temp.groupby(['state_code', 'markets_list', 'state'])['sales_amount'].sum()
    t = t.reset_index()
    fig = px.choropleth_mapbox(
            t,
            locations='state_code',
            geojson=india_geojson,
            mapbox_style="carto-positron",
            color='sales_amount',
            color_continuous_scale='bugn',
            center={"lat": 20, "lon": 77},
            hover_data=['state'],
            zoom=3,
            opacity=1)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)