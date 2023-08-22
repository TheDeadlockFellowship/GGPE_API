from utils.query_execution import execute_query
from config import TABLES

def create_tables():
    execute_query(TABLES['query'])