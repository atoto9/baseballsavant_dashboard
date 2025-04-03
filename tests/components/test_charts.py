"""
Tests for chart component functionality.
"""
import pytest
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from components.charts import (
    create_pitch_type_chart,
    create_velocity_vs_hardHit_chart,
    create_batting_results_chart,
    create_pitcher_comparison_radar,
    create_pitch_distribution_pie
)


def test_create_pitch_type_chart(sample_pitcher_data):
    """Test pitch type distribution chart creation."""
    fig = create_pitch_type_chart(sample_pitcher_data)
    
    # Verify the figure was created and has the correct type
    assert isinstance(fig, go.Figure)
    
    # Check chart properties
    assert fig.layout.title.text == 'Pitcher Pitch Type Distribution (Average Percentage)'
    assert fig.layout.xaxis.title.text == 'Pitch Type'
    assert fig.layout.yaxis.title.text == 'Usage Rate (%)'
    
    # Check that we have the expected number of data points (7 pitch types)
    assert len(fig.data) == 1
    assert len(fig.data[0].x) == 7  # 7 pitch types
    assert len(fig.data[0].y) == 7  # 7 pitch types


def test_create_velocity_vs_hardHit_chart(sample_pitcher_data):
    """Test velocity vs hard-hit chart creation."""
    fig = create_velocity_vs_hardHit_chart(sample_pitcher_data)
    
    # Verify the figure was created and has the correct type
    assert isinstance(fig, go.Figure)
    
    # Check chart properties
    assert fig.layout.title.text == 'Velocity vs Hard-Hit Rate Relationship'
    assert fig.layout.xaxis.title.text == 'Max Velocity (mph)'
    assert fig.layout.yaxis.title.text == 'Hard-Hit Rate (%)'
    
    # Check that we have the expected number of traces (scatter + trend line)
    assert len(fig.data) == 2
    
    # Check scatter plot data points match our sample data
    assert len(fig.data[0].x) == len(sample_pitcher_data)
    assert len(fig.data[0].y) == len(sample_pitcher_data)


def test_create_batting_results_chart(sample_pitcher_data):
    """Test batting results chart creation."""
    fig = create_batting_results_chart(sample_pitcher_data)
    
    # Verify the figure was created and has the correct type
    assert isinstance(fig, go.Figure)
    
    # Check chart properties
    assert fig.layout.title.text == 'Pitcher Average Batting Results Distribution'
    
    # Check that we have the expected number of data points (5 batting result types)
    assert len(fig.data) == 1
    assert len(fig.data[0].x) == 5  # 5 result types


def test_create_pitcher_comparison_radar(sample_pitcher_data):
    """Test pitcher comparison radar chart creation."""
    # Test with one pitcher
    fig = create_pitcher_comparison_radar(sample_pitcher_data, 1)
    
    # Verify the figure was created and has the correct type
    assert isinstance(fig, go.Figure)
    
    # Check chart properties
    assert fig.layout.title.text == 'Pitcher Ability Comparison'
    
    # Check that we have the expected number of traces (one pitcher)
    assert len(fig.data) == 1
    
    # Test with two pitchers
    fig = create_pitcher_comparison_radar(sample_pitcher_data, 1, 2)
    
    # Check that we have the expected number of traces (two pitchers)
    assert len(fig.data) == 2
    
    # Ensure each trace has 5 metrics
    assert len(fig.data[0].r) == 5
    assert len(fig.data[1].r) == 5


def test_create_pitch_distribution_pie(sample_pitcher_data):
    """Test pitcher pitch distribution pie chart creation."""
    fig = create_pitch_distribution_pie(sample_pitcher_data, 1)
    
    # Verify the figure was created and has the correct type
    assert isinstance(fig, go.Figure)
    
    # Check chart properties
    assert 'Pitch Distribution' in fig.layout.title.text
    
    # Check that we have the expected number of data points (7 pitch types)
    assert len(fig.data) == 1
    assert len(fig.data[0].values) == 7  # 7 pitch types
    assert len(fig.data[0].labels) == 7  # 7 pitch names