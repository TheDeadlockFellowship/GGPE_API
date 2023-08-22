# config.py

# Database connection details
DATABASE = {
    'NAME': 'GravityGuy',
    'USER': 'postgres',
    'PASSWORD': 'monopolino1',
    'HOST': 'localhost',
    'PORT': '5432'
}

SERVER = {
    'version': '1.0.0'
}

TABLES = {
    'query': '''CREATE TABLE IF NOT EXISTS RUNS (
            PLAYER_NAME VARCHAR(255),
            RUN_START TIMESTAMP,
            RUN_END TIMESTAMP,
            SCORE BIGINT,
            SEED INT,
            PRIMARY KEY(PLAYER_NAME, RUN_START)
        );
        CREATE TABLE IF NOT EXISTS INPUTS (
            player_name VARCHAR(255),
            run_start TIMESTAMP,
            fixed_frame BIGINT,
            raycast_0 FLOAT,
            raycast_30 FLOAT,
            raycast_45 FLOAT,
            raycast_315 FLOAT,
            raycast_330 FLOAT,
            collect_angle FLOAT,
            collect_length FLOAT,
            gravity_dir FLOAT,
            on_ground_top BOOLEAN,
            on_ground_bot BOOLEAN,
            switch_gravity BOOLEAN,
            PRIMARY KEY (player_name, run_start, fixed_frame)
        );
        CREATE TABLE IF NOT EXISTS MODELS (
            PLAYER_NAME VARCHAR(255) PRIMARY KEY,
            TRAIN_START TIMESTAMP,
            TRAIN_END TIMESTAMP,
            PARAMETERS BYTEA
        );'''
}