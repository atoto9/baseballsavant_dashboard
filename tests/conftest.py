"""
Test fixtures and configuration for pytest.
"""
import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def sample_pitcher_data():
    """
    Create a small sample dataset for testing.
    """
    np.random.seed(42)  # For reproducible test data
    data = {
        'player_id': list(range(1, 6)),
        'name': ['Pitcher 1', 'Pitcher 2', 'Pitcher 3', 'Pitcher 4', 'Pitcher 5'],
        'team': ['Yankees', 'Red Sox', 'Dodgers', 'Giants', 'Cubs'],
        'pitches': [100, 95, 110, 85, 120],
        'max_velo': [95.5, 97.2, 94.1, 92.3, 98.7],
        'min_velo': [88.2, 89.5, 86.3, 85.9, 91.3],
        'ff_pct': [55.0, 45.0, 60.0, 50.0, 40.0],
        'si_pct': [10.0, 15.0, 5.0, 12.0, 20.0],
        'fc_pct': [8.0, 12.0, 10.0, 5.0, 15.0],
        'fs_pct': [2.0, 3.0, 5.0, 8.0, 0.0],
        'ch_pct': [10.0, 5.0, 8.0, 15.0, 10.0],
        'sl_pct': [15.0, 10.0, 12.0, 10.0, 5.0],
        'cu_pct': [0.0, 10.0, 0.0, 0.0, 10.0],
        'max_ev': [105.2, 107.5, 103.8, 102.1, 110.3],
        'hard_hit': [8, 10, 6, 5, 12],
        'hard_hit_pct': [35.0, 42.5, 30.0, 28.5, 45.0],
        'barrels': [3, 5, 2, 1, 6],
        'barrel_pct': [8.5, 10.2, 5.5, 4.8, 12.5],
        'ab': [30, 28, 32, 25, 35],
        'avg': [.250, .285, .220, .310, .195],
        'hits': [8, 8, 7, 8, 7],
        'singles': [5, 3, 4, 6, 3],
        'doubles': [2, 3, 2, 1, 2],
        'triples': [0, 1, 0, 0, 0],
        'home_runs': [1, 1, 1, 1, 2],
        'strikeouts': [12, 10, 15, 8, 18],
        'bip': [18, 18, 17, 17, 17],
    }
    return pd.DataFrame(data)


@pytest.fixture
def mock_db_connection_string():
    """
    Mock database connection string for testing.
    """
    return "postgresql://test_user:test_password@localhost:5432/test_db"