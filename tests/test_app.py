"""
Tests for app functionality.
"""
import pytest
from dash.testing.application_runners import import_app
from dash.testing.browser_runners import Browser
from dash.testing.composite import DashComposite
import dash.testing.wait as wait
from unittest.mock import patch, MagicMock

# These tests require dash[testing] to be installed


@pytest.mark.integration
def test_app_initialization():
    """Test that the app initializes without errors."""
    with patch('utils.data_processing.connect_to_database') as mock_connect:
        # Set up the mock to return sample data
        mock_df = MagicMock()
        mock_df.__len__.return_value = 5
        mock_df.copy.return_value = mock_df
        mock_df.__getitem__.return_value.min.return_value = 0
        mock_df.__getitem__.return_value.max.return_value = 100
        mock_df.__getitem__.return_value.unique.return_value = ['Team1', 'Team2']
        mock_connect.return_value = mock_df
        
        with patch('utils.data_processing.process_pitcher_data', return_value=mock_df):
            # Import the app (this will trigger initialization)
            try:
                import app
                assert True, "App initialized without errors"
            except Exception as e:
                pytest.fail(f"App initialization failed: {e}")


@pytest.mark.integration
def test_update_charts_callback():
    """Test the update_charts callback function directly."""
    with patch('utils.data_processing.connect_to_database') as mock_connect:
        # Set up mocks with sample data
        from app import update_charts  # Import the callback function
        import pandas as pd
        
        # Create sample data
        mock_df = pd.DataFrame({
            'name': ['P1', 'P2', 'P3'],
            'team': ['Yankees', 'Red Sox', 'Dodgers'],
            'pitches': [80, 90, 100],
            'max_velo': [95, 97, 93],
            'strikeouts': [10, 12, 8],
            'hard_hit_pct': [35, 40, 30],
            'avg': [.250, .220, .270],
            'ff_pct': [50, 45, 55],
            'si_pct': [10, 15, 5],
            'fc_pct': [5, 10, 15],
            'fs_pct': [5, 0, 0],
            'ch_pct': [10, 5, 10],
            'sl_pct': [15, 20, 10],
            'cu_pct': [5, 5, 5],
            'singles': [5, 4, 6],
            'doubles': [2, 3, 1],
            'triples': [0, 1, 0],
            'home_runs': [1, 0, 2]
        })
        
        with patch('app.df', mock_df):
            # Test with no filters
            pitch_fig, velo_fig, batting_fig, table_data = update_charts(None, [0, 100])
            
            # Check that figures were created
            assert pitch_fig is not None
            assert velo_fig is not None
            assert batting_fig is not None
            
            # Check that table data has all rows
            assert len(table_data) == 3
            
            # Test with team filter
            pitch_fig, velo_fig, batting_fig, table_data = update_charts(['Yankees'], [0, 100])
            
            # Check that table data is filtered
            assert len(table_data) == 1
            assert table_data[0]['team'] == 'Yankees'
            
            # Test with pitch range filter
            pitch_fig, velo_fig, batting_fig, table_data = update_charts(None, [90, 100])
            
            # Check that table data is filtered
            assert len(table_data) == 2
            assert all(row['pitches'] >= 90 for row in table_data)


# This is a placeholder for browser-based testing which requires running a server
# In a real-world scenario, you would use pytest-dash for this or selenium
@pytest.mark.skip(reason="Requires a running server and browser")
def test_dashboard_rendering(dash_duo):
    """
    Test that the dashboard renders correctly in a browser.
    This test requires dash[testing] and a browser driver.
    """
    # Start the dash app
    dash_duo.start_server(import_app('app'))
    
    # Wait for the page to load
    dash_duo.wait_for_element('#team-dropdown')
    
    # Check that key elements are rendered
    dash_duo.wait_for_element('#pitch-type-chart')
    dash_duo.wait_for_element('#velo-hardHit-chart')
    dash_duo.wait_for_element('#batting-results-chart')
    dash_duo.wait_for_element('#pitcher-data-table')
    
    # Take a screenshot for visual verification
    # dash_duo.take_screenshot('dashboard-initial-load')