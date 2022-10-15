"""NHL Fantasy Dashboard

Runs a local web server to the Hockey Game Counter web app. 
The app retrieves and displays the number of games played by each team 
of the NHL for a given time period

Dependencies:
    dash, dash_bootstrap_components

"""
from datetime import datetime

from dash import Dash, html, dcc, Input, Output
from dash.dash_table import DataTable
import dash_bootstrap_components as dbc

from utils import nhl_api

# Constants
GAME_TYPES = [
    {'label': 'All', 'value': 'all'},
    {'label': 'Pre-Season', 'value': 'PR'},
    {'label': 'Regular Season', 'value': 'R'},
    {'label': 'Post-Season', 'value': 'P'},
]

# App Definition
app = Dash(
    name="Hockey Game Counter",
    title="Hockey Game Counter",
    external_stylesheets=[dbc.themes.SOLAR,
                          dbc.icons.BOOTSTRAP]
)


app.layout = html.Div(
        dbc.Container(
            id='app-container',
            children=[
                html.H1('Hockey Game Counter',
                className='mt-3 mb-4'),
                html.Div(
                    className='row mb-5',
                        children=[
                            html.Div(
                                className='col-lg-4',
                                id='controls',
                                children=[
                                    html.H5(
                                        className='mb-3',
                                        children="""Retrieve the number of games played 
                                            by each team of the NHL for a given time period."""
                                    ),
                                    html.Section(
                                        className='mb-3',
                                        children=[
                                        html.H5(
                                            className='mb-3',
                                            children="""Use the "Date Picker" 
                                                below to select the desired time period. """
                                        ),
                                        html.Label(
                                            htmlFor='date-picker-range',
                                            children='Game Type',
                                            style={'display': 'block'}
                                        ),
                                        dcc.Dropdown(
                                            id='game-type-select',
                                            className='mb-3',
                                            options=GAME_TYPES,
                                            value='R',
                                            style={'max-width': '20rem'},
                                            clearable=False
                                        ),
                                        html.Label(
                                            htmlFor='date-picker-range',
                                            children='Time Period',
                                            style={'display': 'block'}
                                        ),
                                        dcc.DatePickerRange(
                                            id='date-picker-range',
                                            className='mb-3',
                                            display_format='YYYY-MM-DD',
                                            start_date= (today := datetime.today().strftime("%Y-%m-%d")),
                                            end_date= today
                                        ),
                                        
                                        
                                    ]),
                                    dbc.Button(
                                        id="open-offcanvas",
                                        outline=True,
                                        href='https://github.com/aparadisgh',
                                        className="px-1 me-2",
                                        children=html.I(
                                            className="bi bi-github",
                                            style={
                                                'font-size': '2rem',
                                                 'margin': 'auto'
                                            }
                                        ),
                                    ),
                                    html.Span(
                                        className='mb-3',
                                        children="""MIT © 2022 - André Paradis"""
                                    ),
                                    
                                ]
                            ),
                            html.Div(
                                className='col-md-4',
                                id='table-container',
                                children=['Data Table...']
                            ),
                            html.Div(
                                className='col-xl-2',
                            ),
                        ]
                )
            ]
        )
    )


@app.callback(
    Output(component_id='table-container', component_property='children'),
    Input('date-picker-range','start_date'),
    Input('date-picker-range','end_date'),
    Input('game-type-select','value')
)
def update_table(start_date, end_date, game_type):

    team_schdule =  nhl_api.get_game_by_teams(start_date, end_date, game_type)
    teams = nhl_api.TEAM_ABBR
    team_ids = list(nhl_api.TEAM_ABBR.keys())
    data = [
        {
            'team': teams[str(team_id)], 
            'game_count': len(games)
        } 
        for team_id, games in team_schdule.items() 
        if str(team_id) in team_ids  # Avoid games with non-NHL teams
    ]

    table = 'No data retrieved...'
    if data:
        data.sort(key=lambda team: team['game_count'], reverse=True)
        highest_count = data[0]['game_count']
        lowest_count = data[len(data)-1]['game_count']
        table = DataTable(
            id='table',
            columns=[{'name': 'Team', 'id': 'team'},{'name': 'Game Count', 'id': 'game_count'}],
            data=data,
            style_cell={
                'textAlign': 'center',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'maxWidth': 0
            },
            sort_action='native',
            style_data_conditional=[
                {
                    'if': {'column_id': 'game_count'},
                    'fontWeight': 'bold'
                },
                {
                    'if': {
                        'filter_query': 
                            f"{{game_count}} = {highest_count}",
                        'column_id': 'game_count'
                    },
                    'backgroundColor': 'rgb(204, 255, 204)',
                    'color': 'rgb(64, 64, 64)',
                },
                {
                    'if': {
                        'filter_query': 
                            f"{{game_count}} = {lowest_count}",
                            'column_id': 'game_count'
                    },
                    'backgroundColor': 'rgb(255, 229, 204)',
                    'color': 'rgb(64, 64, 64)',
                },
            ]
        )

    return table

if __name__ == '__main__':
    app.run_server(debug=True, port=8080, host='0.0.0.0')
