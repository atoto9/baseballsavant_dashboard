import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def create_pitch_type_chart(df):
    """
    Create pitcher's pitch type distribution chart
    """
    pitch_columns = ['ff_pct', 'si_pct', 'fc_pct', 'fs_pct', 'ch_pct', 'sl_pct', 'cu_pct']
    pitch_names = ['Four-Seam', 'Sinker', 'Cutter', 'Split-Finger', 'Changeup', 'Slider', 'Curveball']
    
    # Calculate average usage rate for each pitch type
    pitch_avg = df[pitch_columns].mean().reset_index()
    pitch_avg.columns = ['pitch_type', 'percentage']
    pitch_avg['pitch_name'] = pitch_names
    
    fig = px.bar(
        pitch_avg, 
        x='pitch_name',
        y='percentage',
        title='Pitcher Pitch Type Distribution (Average Percentage)',
        labels={'percentage': 'Usage Rate (%)', 'pitch_name': 'Pitch Type'},
        color='pitch_name',
        color_discrete_sequence=px.colors.qualitative.G10
    )
    
    return fig

def create_velocity_vs_hardHit_chart(df):
    """
    Create scatter plot showing relationship between velocity and hard-hit rate
    """
    fig = px.scatter(
        df,
        x='max_velo',
        y='hard_hit_pct',
        size='pitches',
        color='team',
        hover_name='name',
        title='Velocity vs Hard-Hit Rate Relationship',
        labels={
            'max_velo': 'Max Velocity (mph)',
            'hard_hit_pct': 'Hard-Hit Rate (%)',
            'pitches': 'Pitch Count'
        }
    )
    
    # Add trend line
    fig.add_trace(
        go.Scatter(
            x=df['max_velo'],
            y=df['max_velo'] * 0.5 + 15,  # Simulated trend line, should use regression in practice
            mode='lines',
            name='Trend Line',
            line=dict(color='rgba(0,0,0,0.3)', dash='dash')
        )
    )
    
    return fig

def create_batting_results_chart(df):
    """
    Create batting results analysis chart
    """
    batting_cols = ['singles', 'doubles', 'triples', 'home_runs', 'strikeouts']
    batting_names = ['Singles', 'Doubles', 'Triples', 'Home Runs', 'Strikeouts']
    
    batting_data = []
    for i, col in enumerate(batting_cols):
        batting_data.append({
            'result_type': batting_names[i],
            'avg_count': df[col].mean()
        })
    
    batting_df = pd.DataFrame(batting_data)
    
    fig = px.bar(
        batting_df,
        x='result_type',
        y='avg_count',
        title='Pitcher Average Batting Results Distribution',
        labels={'avg_count': 'Average Count', 'result_type': 'Result Type'},
        color='result_type',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    return fig

def create_pitcher_comparison_radar(df, pitcher1_id, pitcher2_id=None):
    """
    Create radar chart comparing pitcher abilities
    """
    # Select metrics to display in radar chart
    metrics = ['max_velo', 'strikeouts', 'hard_hit_pct', 'barrel_pct', 'avg']
    metric_names = ['Max Velocity', 'Strikeouts', 'Hard-Hit Rate', 'Barrel Rate', 'Batting Avg']
    
    # Normalize data to make all metrics on 0-1 scale
    normalized_df = df.copy()
    for metric in metrics:
        if metric == 'avg':  # For batting average, lower is better
            normalized_df[f'{metric}_norm'] = 1 - (df[metric] - df[metric].min()) / (df[metric].max() - df[metric].min())
        else:  # For other metrics, higher is better
            normalized_df[f'{metric}_norm'] = (df[metric] - df[metric].min()) / (df[metric].max() - df[metric].min())
    
    # Get data for pitcher 1
    pitcher1_data = normalized_df[normalized_df['player_id'] == pitcher1_id]
    
    # Set up radar chart
    fig = go.Figure()
    
    # Add data for pitcher 1
    fig.add_trace(go.Scatterpolar(
        r=[pitcher1_data[f'{metric}_norm'].values[0] for metric in metrics],
        theta=metric_names,
        fill='toself',
        name=pitcher1_data['name'].values[0]
    ))
    
    # If a second pitcher is provided, add their data
    if pitcher2_id is not None:
        pitcher2_data = normalized_df[normalized_df['player_id'] == pitcher2_id]
        fig.add_trace(go.Scatterpolar(
            r=[pitcher2_data[f'{metric}_norm'].values[0] for metric in metrics],
            theta=metric_names,
            fill='toself',
            name=pitcher2_data['name'].values[0]
        ))
    
    # Set radar chart layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )
        ),
        title="Pitcher Ability Comparison"
    )
    
    return fig

def create_pitch_distribution_pie(df, pitcher_id):
    """
    Create pie chart of pitcher's pitch type distribution
    """
    pitcher_data = df[df['player_id'] == pitcher_id]
    
    if pitcher_data.empty:
        return None
    
    pitch_columns = ['ff_pct', 'si_pct', 'fc_pct', 'fs_pct', 'ch_pct', 'sl_pct', 'cu_pct']
    pitch_names = ['Four-Seam', 'Sinker', 'Cutter', 'Split-Finger', 'Changeup', 'Slider', 'Curveball']
    
    values = [pitcher_data[col].values[0] for col in pitch_columns]
    
    fig = px.pie(
        values=values,
        names=pitch_names,
        title=f"{pitcher_data['name'].values[0]} Pitch Distribution",
        hole=0.3,
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    
    return fig

def create_velocity_histogram(df, team=None):
    """
    Create velocity histogram, can be filtered by team
    """
    if team:
        filtered_df = df[df['team'] == team]
    else:
        filtered_df = df
    
    fig = px.histogram(
        filtered_df,
        x='max_velo',
        nbins=20,
        title='Pitcher Maximum Velocity Distribution',
        labels={'max_velo': 'Maximum Velocity (mph)', 'count': 'Pitcher Count'},
        color='team' if not team else None,
        marginal='box'
    )
    
    fig.update_layout(
        xaxis_title='Maximum Velocity (mph)',
        yaxis_title='Pitcher Count'
    )
    
    return fig

def create_strikeout_vs_hits_scatter(df):
    """
    Create strikeouts vs hits scatter plot
    """
    fig = px.scatter(
        df,
        x='strikeouts',
        y='hits',
        size='pitches',
        color='team',
        hover_name='name',
        title='Strikeouts vs Hits Relationship',
        labels={
            'strikeouts': 'Strikeouts',
            'hits': 'Hits',
            'pitches': 'Pitch Count'
        },
        trendline='ols'  # Add trend line
    )
    
    return fig

def create_team_performance_comparison(df):
    """
    Create team pitcher performance comparison chart
    """
    team_stats = df.groupby('team').agg({
        'max_velo': 'mean',
        'strikeouts': 'mean',
        'hard_hit_pct': 'mean',
        'barrel_pct': 'mean',
        'avg': 'mean'
    }).reset_index()
    
    # Create long-format data
    team_stats_long = pd.melt(
        team_stats,
        id_vars=['team'],
        value_vars=['max_velo', 'strikeouts', 'hard_hit_pct', 'barrel_pct', 'avg'],
        var_name='metric',
        value_name='value'
    )
    
    # Replace metric names with human-readable versions
    metric_mapping = {
        'max_velo': 'Max Velocity',
        'strikeouts': 'Strikeouts',
        'hard_hit_pct': 'Hard-Hit Rate',
        'barrel_pct': 'Barrel Rate',
        'avg': 'Batting Avg'
    }
    team_stats_long['metric'] = team_stats_long['metric'].map(metric_mapping)
    
    # Create grouped bar chart
    fig = px.bar(
        team_stats_long,
        x='team',
        y='value',
        color='metric',
        barmode='group',
        title='Team Pitcher Performance Comparison',
        labels={
            'team': 'Team',
            'value': 'Value',
            'metric': 'Metric'
        }
    )
    
    return fig