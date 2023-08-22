from entities.input_entity import InputData
from core.database import Database
from utils.query_execution import execute_query
from datetime import datetime

class InputDao:
    def __init__(self, db: Database):
        self.db = db

    def add_input(self, input: InputData):
        fields = input.dict()  # Convert Pydantic model to dictionary
        columns = ', '.join(fields.keys())  # Columns for the query
        placeholders = ', '.join(['%s'] * len(fields))  # Placeholders for the query
        query = f'''
            INSERT INTO INPUTS ({columns}) VALUES ({placeholders})
        '''
        params = tuple(fields.values())  # Values for the query
        execute_query(query, params)

    def delete_inputs_by_run(self, player_name: str, run_start: datetime):
        query = '''
            DELETE FROM INPUTS WHERE PLAYER_NAME = %s AND RUN_START = %s
        '''
        params = (player_name, run_start)
        execute_query(query, params)


