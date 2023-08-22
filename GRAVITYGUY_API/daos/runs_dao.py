from entities.run_entity import Run
from core.database import Database
from utils.query_execution import execute_query
from datetime import datetime

class RunDao:

    def __init__(self, db: Database):
        self.db = db

    def add_run(self, run: Run):
        fields = run.dict()  # Convert Pydantic model to dictionary
        columns = ', '.join(fields.keys())  # Columns for the query
        placeholders = ', '.join(['%s'] * len(fields))  # Placeholders for the query
        query = f'''
            INSERT INTO RUNS ({columns}) VALUES ({placeholders})
        '''
        params = tuple(fields.values())  # Values for the query
        execute_query(query, params)

    def delete_run(self, player_name: str, run_start: datetime):
        query = '''
            DELETE FROM RUNS WHERE PLAYER_NAME = %s AND RUN_START = %s
        '''
        params = (player_name, run_start)
        execute_query(query, params)





