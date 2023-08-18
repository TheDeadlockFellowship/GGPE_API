from flask import Flask, request, jsonify
from psycopg2 import pool, sql
import psycopg2.extras

app = Flask(__name__)

# Replace with your database credentials and hostname
db_pool = pool.SimpleConnectionPool(
    1,  # Minimum number of connections
    20, # Maximum number of connections
    database='GravityGuy',
    user='postgres',
    password='****',
    host='localhost',
    port='5432'
)

def get_connection():
    return db_pool.getconn()

def release_connection(conn):
    db_pool.putconn(conn)

def execute_query(query, values=None):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, values)
            conn.commit()
            try:
                result = cursor.fetchall()
                return result
            except psycopg2.ProgrammingError:
                return None

@app.route('/add_run', methods=['POST'])
def add_run():
    data = request.json
    run_data = data.get('run_data')
    input_data_list = data.get('input_data')

    if run_data is None or input_data_list is None:
        return jsonify({'error': 'Missing run_data or input_data'}), 400

    try:
        # Insert data into the RUNS table
        run_query = '''
            INSERT INTO RUNS (PLAYER_NAME, RUN_START, RUN_END, SCORE)
            VALUES (%s, %s, %s, %s);
        '''
        run_values = (run_data['player_name'], run_data['run_start'], run_data['run_end'], run_data['score'])
        execute_query(run_query, run_values)

        # Insert data into the INPUTS table for each input
        for input_data in input_data_list:
            input_query = '''
                INSERT INTO INPUTS (
                    player_name, run_start, fixed_frame,
                    raycast_0, raycast_30, raycast_45, raycast_315, raycast_330,
                    collect_angle, collect_length, gravity_dir,
                    on_ground_top, on_ground_bot, switch_gravity
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                );
            '''
            input_values = (
                input_data['player_name'], input_data['run_start'], input_data['fixed_frame'],
                input_data['raycast_0'], input_data['raycast_30'], input_data['raycast_45'],
                input_data['raycast_315'], input_data['raycast_330'], input_data['collect_angle'],
                input_data['collect_length'], input_data['gravity_dir'], input_data['on_ground_top'],
                input_data['on_ground_bot'], input_data['switch_gravity']
            )
            execute_query(input_query, input_values)

        return jsonify({'message': 'Data added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_server_version', methods=['GET'])
def get_server_version():
    try:
        result = execute_query('SELECT version();')
        version = result[0][0]
        return jsonify({'server_version': version})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete_run/<string:player_name>/<string:run_start>', methods=['DELETE'])
def delete_run(player_name, run_start):
    try:
        delete_query = 'DELETE FROM RUNS WHERE PLAYER_NAME = %s AND RUN_START = %s'
        rows_affected = execute_query(delete_query, (player_name, run_start))
        if not rows_affected:
            return jsonify({'error': 'Run not found'}), 404
        return jsonify({'message': 'Run has been deleted'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_models/<string:player_name>', methods=['GET'])
def get_models(player_name):
    try:
        select_query = 'SELECT TRAIN_START, TRAIN_END, PARAMETERS FROM MODELS WHERE PLAYER_NAME = %s'
        model_data = execute_query(select_query, (player_name,))
        if not model_data:
            return jsonify({'error': 'Player not found'}), 404
        train_start, train_end, parameters = model_data[0]
        model = {
            'train_start': train_start.strftime('%Y-%m-%d %H:%M:%S'),
            'train_end': train_end.strftime('%Y-%m-%d %H:%M:%S'),
            'parameters': parameters.decode('utf-8')  # Assuming PARAMETERS is stored as bytes (BYTEA)
        }
        return jsonify({'player_name': player_name, 'model': model}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with get_connection() as conn:
        with conn.cursor() as cursor:
            # Create the tables if they don't exist
            cursor.execute('''CREATE TABLE IF NOT EXISTS RUNS (
            PLAYER_NAME VARCHAR(255),
            RUN_START TIMESTAMP,
            RUN_END TIMESTAMP,
            SCORE BIGINT,
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
        );''')  # Replace with your table creation SQL statements
            conn.commit()
    app.run(debug=True)






