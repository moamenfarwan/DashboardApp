#COVID-19 DASHBOARD CODE

#importing libraries
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

#Loading the dataset
df = pd.read_csv('covid_19_data_tr.csv')
print(df.head())
conf_cases = df[['Confirmed']]
recv_cases = df[['Recovered']]
dead_cases = df[['Deaths']]

#function to get the sum of the dataframe
def get_total_value(data):
    return data.iloc[:, -1].sum()

total_conf_cases = get_total_value(conf_cases)
total_recv_cases = get_total_value(recv_cases)
total_dead_cases = get_total_value(dead_cases)

#for the figure (graph) using the plotly function to plot my graph
def get_category(ctgry_value):
    print(ctgry_value)
    fig = px.line(df, x="Last_Update", y=ctgry_value)
    fig.update_layout(title_x=0.5, plot_bgcolor='white', paper_bgcolor='#F2DFCE', xaxis_title="Date")
    return fig


#Creating the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Covid-19 Dashboard'

#designing the layout 1) the title 2)cards 3)checklist 4)graph
app.layout = dbc.Container([
    dbc.Row([
        html.H1('Covid-19 Dashboard', style={'textAlign': 'center', 'color': 'blue'}),
        html.P('For Turkey 2022', style={'textAlign': 'center', 'color': 'black'}),
       ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Recovered', style={'textAlign': 'center', 'fontSize': '150%'}),
                dbc.CardBody([
                    html.H5(total_recv_cases, style={'textAlign': 'center'}),
                    html.P('Recovered cases', style={'textAlign': 'center'})
                ])
            ], color= 'success', inverse= True)

    ]),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Confirmed', style={'textAlign': 'center', 'fontSize': '150%'}),
                dbc.CardBody([
                    html.H5(total_conf_cases, style={'textAlign': 'center'}),
                    html.P('Confirmed cases', style={'textAlign': 'center'})
                ])
            ], color= 'warning', inverse= True)
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Deaths', style={'textAlign': 'center', 'fontSize': '150%'}),
                dbc.CardBody([
                    html.H5(total_dead_cases, style={'textAlign': 'center'}),
                    html.P('Death cases', style={'textAlign':'center'})
                ])
            ], color='dark', inverse= True)
        ]),
    ], className='mb-4'),
    dbc.Row([
        dbc.Col(
            dcc.Checklist(
                options=[
                    {'label': 'Recovered', 'value': 'Recovered'},

                    {'label': 'Confirmed', 'value': 'Confirmed'},

                    {'label': 'Deaths', 'value': 'Deaths'},

                ],
                value=['Deaths'],
                id = 'ttt',
                labelStyle={'display': 'inline-block'}
            ), md=dict(size=5), className='inline' #md and className are ready made bootstrap styles

        ),

dbc.Col(dcc.Graph(id="mygraph", figure= get_category('Deaths')), md=dict(size=8, offset=2))], className='mb-4')
])

#decorator = specifies the input and output
@app.callback(
    Output('mygraph', 'figure'),
    Input('ttt', 'value')
)
#the function = makes the plotly figure dependant on the checklist
def update_graph(input_ctgry):
    return get_category(input_ctgry)

#running the server
if __name__ == '__main__':
    app.run_server(debug=True)