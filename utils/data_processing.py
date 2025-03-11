import pandas as pd
import numpy as np
import os
import psycopg2
from sqlalchemy import create_engine

def load_data(file_path=None):
    """
    Load data, if file path is None, generate sample data
    """
    if file_path and os.path.exists(file_path):
        df = pd.read_csv(file_path)
        return df
    else:
        return generate_sample_data()

def generate_sample_data(n=30):
    """
    Generate simulated baseball data
    """
    np.random.seed(42)
    data = {
        'player_id': list(range(1, n+1)),
        'name': [f'Pitcher {i}' for i in range(1, n+1)],
        'team': np.random.choice(['Yankees', 'Red Sox', 'Dodgers', 'Giants', 'Cubs'], n),
        'pitches': np.random.randint(50, 120, n),
        'max_velo': np.random.uniform(90, 102, n),
        'min_velo': np.random.uniform(80, 90, n),
        'ff_pct': np.random.uniform(40, 60, n),
        'si_pct': np.random.uniform(5, 20, n),
        'fc_pct': np.random.uniform(5, 15, n),
        'fs_pct': np.random.uniform(0, 10, n),
        'ch_pct': np.random.uniform(5, 15, n),
        'sl_pct': np.random.uniform(10, 25, n),
        'cu_pct': np.random.uniform(0, 15, n),
        'max_ev': np.random.uniform(95, 115, n),
        'hard_hit': np.random.randint(2, 15, n),
        'hard_hit_pct': np.random.uniform(25, 50, n),
        'barrels': np.random.randint(0, 8, n),
        'barrel_pct': np.random.uniform(3, 12, n),
        'ab': np.random.randint(20, 35, n),
        'avg': np.random.uniform(.150, .350, n),
        'hits': np.random.randint(5, 15, n),
        'singles': np.random.randint(3, 10, n),
        'doubles': np.random.randint(1, 5, n),
        'triples': np.random.randint(0, 2, n),
        'home_runs': np.random.randint(0, 4, n),
        'strikeouts': np.random.randint(5, 20, n),
        'bip': np.random.randint(15, 25, n),
    }
    return pd.DataFrame(data)

def connect_to_database(connection_string):
    """
    Connect to database and get pitcher data, using PostgreSQL in Docker Compose environment
    
    Args:
        connection_string: Database connection string, e.g. postgresql://baseball_user:baseball_password@postgres:5432/baseball_db
    
    Returns:
        DataFrame containing pitcher data
    """
    try:
        print(f"Attempting to connect to database: {connection_string}")
        
        # Try native psycopg2 connection test
        conn_parts = connection_string.replace('postgresql://', '').split('@')
        user_pass = conn_parts[0].split(':')
        host_port_db = conn_parts[1].split('/')
        host_port = host_port_db[0].split(':')
        
        connection_params = {
            'user': user_pass[0],
            'password': user_pass[1],
            'host': host_port[0],
            'port': host_port[1] if len(host_port) > 1 else '5432',
            'database': host_port_db[1]
        }
        
        # Test connection
        conn = psycopg2.connect(**connection_params)
        print("Successfully connected to database!")
        conn.close()
        
        # Use SQLAlchemy to connect and read data
        engine = create_engine(connection_string)
        
        # Try to query the ads_game_pitcher_stats_f table
        try:
            query = """
            SELECT * FROM ads_game_pitcher_stats_f
            """
            df = pd.read_sql(query, engine)
            print(f"Successfully read ads_game_pitcher_stats_f table, {len(df)} records total")
            return df
        except Exception as table_error:
            print(f"Failed to read ads_game_pitcher_stats_f table: {table_error}")
            
            # Try to query the view
            try:
                query = """
                SELECT * FROM v_game_pitcher_stats
                """
                df = pd.read_sql(query, engine)
                print(f"Successfully read v_game_pitcher_stats view, {len(df)} records total")
                return df
            except Exception as view_error:
                print(f"Failed to read v_game_pitcher_stats view: {view_error}")
                raise Exception("Unable to get pitcher data from database")
    
    except Exception as e:
        print(f"Database connection or query failed: {e}")
        print("Returning sample data instead...")
        # If connection fails, return sample data
        return generate_sample_data()

def process_pitcher_data(df):
    """
    Process pitcher data, calculate additional statistics
    """
    # Copy dataframe to avoid modifying original data
    processed_df = df.copy()
    
    # Handle potential data type issues
    numeric_columns = ['pitches', 'max_velo', 'min_velo', 'ff_pct', 'si_pct', 
                      'fc_pct', 'fs_pct', 'ch_pct', 'sl_pct', 'cu_pct', 
                      'max_ev', 'hard_hit', 'hard_hit_pct', 'barrels', 
                      'barrel_pct', 'ab', 'avg', 'hits', 'singles', 
                      'doubles', 'triples', 'home_runs', 'strikeouts', 'bip']
    
    for col in numeric_columns:
        if col in processed_df.columns:
            processed_df[col] = pd.to_numeric(processed_df[col], errors='coerce')
    
    # Calculate additional statistics
    if 'strikeouts' in processed_df.columns and 'ab' in processed_df.columns:
        processed_df['k_rate'] = (processed_df['strikeouts'] / processed_df['ab'] * 100).round(1)
    
    if 'singles' in processed_df.columns and 'doubles' in processed_df.columns and \
       'triples' in processed_df.columns and 'home_runs' in processed_df.columns:
        processed_df['total_bases'] = (
            processed_df['singles'] + 
            2 * processed_df['doubles'] + 
            3 * processed_df['triples'] + 
            4 * processed_df['home_runs']
        )
    
    # Calculate primary pitch type for each pitcher
    pitch_columns = ['ff_pct', 'si_pct', 'fc_pct', 'fs_pct', 'ch_pct', 'sl_pct', 'cu_pct']
    pitch_names = ['Four-Seam', 'Sinker', 'Cutter', 'Split-Finger', 'Changeup', 'Slider', 'Curveball']
    
    if all(col in processed_df.columns for col in pitch_columns):
        for i, pitcher in processed_df.iterrows():
            try:
                max_pitch_idx = np.argmax([pitcher[col] for col in pitch_columns])
                processed_df.loc[i, 'primary_pitch'] = pitch_names[max_pitch_idx]
            except:
                processed_df.loc[i, 'primary_pitch'] = 'Unknown'
    
    return processed_df