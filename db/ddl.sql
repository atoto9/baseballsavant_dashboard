CREATE TABLE IF NOT EXISTS players (
    player_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    birth_date DATE,
    position_primary VARCHAR(5),
    position_secondary VARCHAR(5),
    batting_hand VARCHAR(10),
    throwing_hand VARCHAR(10),
    height INTEGER,
    weight INTEGER,
    draft_year INTEGER,
    draft_round INTEGER,
    draft_position INTEGER,
    team_id INTEGER
);

CREATE TABLE IF NOT EXISTS teams (
    team_id SERIAL PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL,
    team_code VARCHAR(10) NOT NULL,
    league VARCHAR(5),
    division VARCHAR(10),
    city VARCHAR(50),
    stadium_id INTEGER,
    manager_id INTEGER
);

CREATE TABLE IF NOT EXISTS games (
    game_id SERIAL PRIMARY KEY,
    game_date DATE NOT NULL,
    game_time TIME,
    home_team_id INTEGER NOT NULL,
    away_team_id INTEGER NOT NULL,
    stadium_id INTEGER,
    weather_condition VARCHAR(50),
    temperature INTEGER,
    wind_speed INTEGER,
    wind_direction VARCHAR(20),
    attendance INTEGER,
    game_duration INTEGER,
    status VARCHAR(20) DEFAULT 'scheduled',
    FOREIGN KEY (home_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (away_team_id) REFERENCES teams(team_id)
);

CREATE TABLE IF NOT EXISTS pitch_events (
    pitch_id SERIAL PRIMARY KEY,
    game_id INTEGER NOT NULL,
    inning INTEGER NOT NULL,
    half_inning VARCHAR(10) NOT NULL,
    pitcher_id INTEGER NOT NULL,
    batter_id INTEGER NOT NULL,
    pitch_number INTEGER,
    pitch_type VARCHAR(5),
    pitch_velocity DECIMAL(5,1),
    pitch_spin_rate INTEGER,
    pitch_horizontal_movement DECIMAL(5,2),
    pitch_vertical_movement DECIMAL(5,2),
    pitch_location_x DECIMAL(5,2),
    pitch_location_y DECIMAL(5,2),
    balls_count INTEGER,
    strikes_count INTEGER,
    outs_count INTEGER,
    event_timestamp TIMESTAMP,
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (pitcher_id) REFERENCES players(player_id),
    FOREIGN KEY (batter_id) REFERENCES players(player_id)
);

CREATE TABLE IF NOT EXISTS batted_ball_events (
    batted_ball_id SERIAL PRIMARY KEY,
    pitch_id INTEGER NOT NULL,
    exit_velocity DECIMAL(5,1),
    launch_angle DECIMAL(5,1),
    distance INTEGER,
    hit_direction VARCHAR(20),
    hard_hit_flag BOOLEAN,
    barrel_flag BOOLEAN,
    hit_type VARCHAR(20),
    fielded_by_player_id INTEGER,
    is_out BOOLEAN,
    result_type VARCHAR(20),
    FOREIGN KEY (pitch_id) REFERENCES pitch_events(pitch_id),
    FOREIGN KEY (fielded_by_player_id) REFERENCES players(player_id)
);

CREATE TABLE IF NOT EXISTS pitcher_batter_outcomes (
    outcome_id SERIAL PRIMARY KEY,
    game_id INTEGER NOT NULL,
    pitcher_id INTEGER NOT NULL,
    batter_id INTEGER NOT NULL,
    at_bat_number INTEGER,
    final_pitch_id INTEGER,
    result VARCHAR(20),
    hit_type VARCHAR(20),
    rbi INTEGER,
    hard_hit_flag BOOLEAN,
    barrel_flag BOOLEAN,
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (pitcher_id) REFERENCES players(player_id),
    FOREIGN KEY (batter_id) REFERENCES players(player_id),
    FOREIGN KEY (final_pitch_id) REFERENCES pitch_events(pitch_id)
);

CREATE TABLE IF NOT EXISTS game_pitcher_performances (
    game_pitcher_perf_id SERIAL PRIMARY KEY,
    game_id INTEGER NOT NULL,
    pitcher_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    innings_pitched DECIMAL(3,1),
    batters_faced INTEGER,
    total_pitches INTEGER,
    pitches_by_type JSONB,
    pitch_velocity_min DECIMAL(5,1),
    pitch_velocity_max DECIMAL(5,1),
    pitch_velocity_avg DECIMAL(5,1),
    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (pitcher_id) REFERENCES players(player_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);

CREATE TABLE IF NOT EXISTS ads_game_pitcher_stats_f (
    player_id INTEGER NOT NULL,
    name VARCHAR(100),
    team VARCHAR(50),
    pitches INTEGER,
    max_velo DECIMAL(5,1),
    min_velo DECIMAL(5,1),
    ff_pct DECIMAL(5,1),  
    si_pct DECIMAL(5,1),  
    fc_pct DECIMAL(5,1),  
    fs_pct DECIMAL(5,1),  
    ch_pct DECIMAL(5,1),  
    sl_pct DECIMAL(5,1),  
    cu_pct DECIMAL(5,1),  
    max_ev DECIMAL(5,1), 
    hard_hit INTEGER,  
    hard_hit_pct DECIMAL(5,1),  
    barrels INTEGER,  
    barrel_pct DECIMAL(5,1),  
    ab INTEGER,  
    avg DECIMAL(5,3),  
    hits INTEGER,  
    singles INTEGER,  
    doubles INTEGER,  
    triples INTEGER,  
    home_runs INTEGER,  
    strikeouts INTEGER,  
    bip INTEGER 
);
