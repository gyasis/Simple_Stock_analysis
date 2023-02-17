import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from data_import import get_stock_data

# Load the stock data from a CSV file
df = get_stock_data()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout for the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Simple Stock Analysis", className="text-primary"),
            html.Hr(),
            html.P(
                "Select a company and a stock to display its historical price data.",
                className="lead",
            ),
            html.P(
                "You can also sort the results by opening or closing price, or search for a specific stock.",
                className="lead",
            ),
            html.Div([
                html.P('Company'),
                dcc.Dropdown(
                    id='company-dropdown',
                    options=[{'label': c, 'value': c} for c in df['company_name'].unique()],
                    value=df['company_name'].unique()[0]
                ),
                html.Br(),
                html.P('Stock'),
                dcc.Dropdown(
                    id='stock-dropdown',
                    options=[{'label': s, 'value': s} for s in df['stock_name'].unique()],
                    value=df['stock_name'].unique()[0]
                ),
                html.Br(),
                html.P('Sort By'),
                dcc.Dropdown(
                    id='sort-dropdown',
                    options=[
                        {'label': 'Price (Open)', 'value': 'open_price'},
                        {'label': 'Price (Close)', 'value': 'close_price'},
                        {'label': 'Weekly Changes', 'value': 'weekly_changes'}
                    ],
                    value='close_price'
                ),
                html.Br(),
                html.P('Search'),
                dcc.Input(
                    id='search-input',
                    type='text',
                    placeholder='Enter a stock name'
                ),
            ], className='sidebar'),
        ], md=4),
        dbc.Col([
            dcc.Graph(id='graph'),
        ], md=8),
    ]),
])

@app.callback(
    Output('graph', 'figure'),
    [
        Input('company-dropdown', 'value'),
        Input('stock-dropdown', 'value'),
        Input('sort-dropdown', 'value'),
        Input('search-input', 'value')
    ]
)
def update_graph(company_name, stock_name, sort_by, search_term):
    # If the stock name dropdown is blank, display all stocks for the selected company
    if not stock_name:
        filtered_df = df[df['company_name'] == company_name]
    else:
        filtered_df = df[(df['company_name'] == company_name) & (df['stock_name'] == stock_name)]
    if search_term:
        filtered_df = filtered_df[filtered_df['stock_name'].str.contains(search_term)]
    filtered_df = filtered_df.sort_values(sort_by)
    fig = px.line(filtered_df, x='date', y='close_price')
    fig.update_layout(title=f'{company_name} - {stock_name}')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
