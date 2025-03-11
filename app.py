import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# Import data processing tools
from utils.data_processing import connect_to_database, process_pitcher_data, generate_sample_data
# Import reusable chart components
from components.charts import (
    create_pitch_type_chart,
    create_velocity_vs_hardHit_chart,
    create_batting_results_chart
)

# Get database connection string from environment variables (set in Docker Compose environment)
# If not found, use default connection string
db_url = os.environ.get('DATABASE_URL', 'postgresql://baseball_user:baseball_password@postgres:5432/baseball_db')

# Try to connect to the database and fetch data
try:
    print("Attempting to connect to database...")
    df = connect_to_database(db_url)
    print(f"Successfully retrieved data from database, {len(df)} records in total")
    
    # Perform additional data processing
    df = process_pitcher_data(df)
except Exception as e:
    print(f"Database connection failed: {e}")
    print("Using sample data instead")
    # If connection fails, use sample data
    df = generate_sample_data()
    df = process_pitcher_data(df)

# Initialize Dash application
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # For production deployment

# Define application layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Baseball Pitcher Data Visualization Dashboard", className="text-center my-4")
        ], width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Filter Options"),
                dbc.CardBody([
                    html.H5("Select Team"),
                    dcc.Dropdown(
                        id='team-dropdown',
                        options=[{'label': team, 'value': team} for team in sorted(df['team'].unique())],
                        multi=True,
                        placeholder="Select teams...",
                    ),
                    html.Hr(),
                    html.H5("Pitch Count Range"),
                    dcc.RangeSlider(
                        id='pitches-slider',
                        min=df['pitches'].min(),
                        max=df['pitches'].max(),
                        step=5,
                        marks={i: str(i) for i in range(int(df['pitches'].min()), int(df['pitches'].max())+1, 10)},
                        value=[df['pitches'].min(), df['pitches'].max()]
                    )
                ])
            ])
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Pitch Type Distribution"),
                dbc.CardBody([
                    dcc.Graph(id='pitch-type-chart')
                ])
            ])
        ], width=9)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Velocity vs Hard-Hit Analysis"),
                dbc.CardBody([
                    dcc.Graph(id='velo-hardHit-chart')
                ])
            ])
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Batting Results Analysis"),
                dbc.CardBody([
                    dcc.Graph(id='batting-results-chart')
                ])
            ])
        ], width=6)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Pitcher Data Details"),
                dbc.CardBody([
                    dash_table.DataTable(
                        id='pitcher-data-table',
                        columns=[
                            {'name': 'Name', 'id': 'name'},
                            {'name': 'Team', 'id': 'team'},
                            {'name': 'Pitches', 'id': 'pitches'},
                            {'name': 'Max Velocity', 'id': 'max_velo'},
                            {'name': 'Strikeouts', 'id': 'strikeouts'},
                            {'name': 'Hard-Hit %', 'id': 'hard_hit_pct', 'type': 'numeric', 'format': {'specifier': '.1f'}},
                            {'name': 'Batting Avg', 'id': 'avg', 'type': 'numeric', 'format': {'specifier': '.3f'}}
                        ],
                        page_size=10,
                        style_table={'overflowX': 'auto'},
                        style_cell={
                            'textAlign': 'center',
                            'padding': '8px',
                        },
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(248, 248, 248)'
                            }
                        ]
                    )
                ])
            ])
        ], width=12)
    ])
], fluid=True)

# Define callback functions
@app.callback(
    [
        Output('pitch-type-chart', 'figure'),
        Output('velo-hardHit-chart', 'figure'),
        Output('batting-results-chart', 'figure'),
        Output('pitcher-data-table', 'data')
    ],
    [
        Input('team-dropdown', 'value'),
        Input('pitches-slider', 'value')
    ]
)
def update_charts(selected_teams, pitches_range):
    # Filter data
    filtered_df = df.copy()
    
    if selected_teams and len(selected_teams) > 0:
        filtered_df = filtered_df[filtered_df['team'].isin(selected_teams)]
    
    filtered_df = filtered_df[(filtered_df['pitches'] >= pitches_range[0]) & 
                            (filtered_df['pitches'] <= pitches_range[1])]
    
    # Create charts using imported chart components
    pitch_fig = create_pitch_type_chart(filtered_df)
    velo_hardHit_fig = create_velocity_vs_hardHit_chart(filtered_df)
    batting_fig = create_batting_results_chart(filtered_df)
    
    # Table data
    table_data = filtered_df[['name', 'team', 'pitches', 'max_velo', 'strikeouts', 'hard_hit_pct', 'avg']].to_dict('records')
    
    return pitch_fig, velo_hardHit_fig, batting_fig, table_data

# Launch application
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)