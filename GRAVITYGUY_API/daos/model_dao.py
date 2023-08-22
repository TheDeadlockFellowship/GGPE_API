from entities.model_entity import Model
from core.database import Database
from utils.query_execution import execute_query
from datetime import datetime

class ModelDao:

    def __init__(self, db: Database):
        self.db = db

    def get(self, player_name: str, train_start: datetime) -> Model:
        query = '''
            SELECT player_name, train_start, train_end, parameters
            FROM MODELS
            WHERE player_name = %s AND train_start = %s
        '''
        params = (player_name, train_start)
        try:
            result = execute_query(query, params, fetch=True)
            if not result:
                return None
            return Model(**result[0])
        except Exception as e:
            print(f"Error getting model: {e}")
            raise

