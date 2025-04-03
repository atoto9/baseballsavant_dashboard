"""
Tests for data processing utility functions.
"""
import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock

from utils.data_processing import (
    load_data,
    generate_sample_data,
    process_pitcher_data,
    connect_to_database
)


def test_generate_sample_data():
    """Test that sample data is generated correctly."""
    # Test with default size
    df = generate_sample_data()
    assert len(df) == 30
    assert set(df.columns) == {
        'player_id', 'name', 'team', 'pitches', 'max_velo', 'min_velo',
        'ff_pct', 'si_pct', 'fc_pct', 'fs_pct', 'ch_pct', 'sl_pct', 'cu_pct',
        'max_ev', 'hard_hit', 'hard_hit_pct', 'barrels', 'barrel_pct',
        'ab', 'avg', 'hits', 'singles', 'doubles', 'triples', 'home_runs',
        'strikeouts', 'bip'
    }
    
    # Test with custom size
    df = generate_sample_data(n=10)
    assert len(df) == 10


def test_load_data(tmp_path, monkeypatch):
    """Test data loading functionality."""
    # Create a temporary CSV file
    csv_file = tmp_path / "test_data.csv"
    test_df = pd.DataFrame({
        'player_id': [1, 2],
        'name': ['Test Pitcher 1', 'Test Pitcher 2'],
        'team': ['Test Team 1', 'Test Team 2']
    })
    test_df.to_csv(csv_file, index=False)
    
    # Test loading from file
    result_df = load_data(csv_file)
    pd.testing.assert_frame_equal(result_df, test_df)
    
    # Test fallback to sample data
    with patch('utils.data_processing.generate_sample_data') as mock_generate:
        mock_df = pd.DataFrame({'test': [1, 2, 3]})
        mock_generate.return_value = mock_df
        
        # Test with non-existent file
        result_df = load_data('non_existent_file.csv')
        mock_generate.assert_called_once()
        pd.testing.assert_frame_equal(result_df, mock_df)


def test_process_pitcher_data(sample_pitcher_data):
    """Test pitcher data processing functionality."""
    processed_df = process_pitcher_data(sample_pitcher_data)
    
    # Check that the original dataframe is not modified
    assert id(processed_df) != id(sample_pitcher_data)
    
    # Check that additional stats are calculated correctly
    assert 'k_rate' in processed_df.columns
    assert 'total_bases' in processed_df.columns
    assert 'primary_pitch' in processed_df.columns
    
    # Check specific calculations for k_rate
    expected_k_rate = (sample_pitcher_data['strikeouts'] / sample_pitcher_data['ab'] * 100).round(1)
    pd.testing.assert_series_equal(processed_df['k_rate'], expected_k_rate)
    
    # Check specific calculations for total_bases
    expected_total_bases = (
        sample_pitcher_data['singles'] + 
        2 * sample_pitcher_data['doubles'] + 
        3 * sample_pitcher_data['triples'] + 
        4 * sample_pitcher_data['home_runs']
    )
    pd.testing.assert_series_equal(processed_df['total_bases'], expected_total_bases)


@patch('utils.data_processing.psycopg2.connect')
@patch('utils.data_processing.create_engine')
def test_connect_to_database_success(mock_create_engine, mock_connect, mock_db_connection_string):
    """Test successful database connection."""
    # Set up mocks
    mock_conn = MagicMock()
    mock_connect.return_value = mock_conn
    
    mock_engine = MagicMock()
    mock_create_engine.return_value = mock_engine
    
    # Mock the pandas read_sql to return a dataframe
    expected_df = pd.DataFrame({'test': [1, 2, 3]})
    mock_engine.execute.return_value = expected_df
    
    with patch('pandas.read_sql', return_value=expected_df):
        result_df = connect_to_database(mock_db_connection_string)
    
    # Check that the connection was made
    mock_connect.assert_called_once()
    mock_create_engine.assert_called_once_with(mock_db_connection_string)
    
    # Check that the result is as expected
    pd.testing.assert_frame_equal(result_df, expected_df)


@patch('utils.data_processing.psycopg2.connect')
def test_connect_to_database_failure(mock_connect, mock_db_connection_string):
    """Test database connection failure with fallback to sample data."""
    # Make the connection raise an exception
    mock_connect.side_effect = Exception("Connection failed")
    
    # Mock generate_sample_data to return a known dataframe
    expected_df = pd.DataFrame({'test': [1, 2, 3]})
    
    with patch('utils.data_processing.generate_sample_data', return_value=expected_df):
        result_df = connect_to_database(mock_db_connection_string)
    
    # Check that the connection was attempted
    mock_connect.assert_called_once()
    
    # Check that the result is the sample data
    pd.testing.assert_frame_equal(result_df, expected_df)