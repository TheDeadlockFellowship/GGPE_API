from psycopg2 import pool
from config import DATABASE, TABLES


class Database:
    def __init__(self):
        self.connection_pool = None
    def initialize(self):
        try:
            self.connection_pool = pool.SimpleConnectionPool(
                1,  # Minimum number of connections
                20, # Maximum number of connections
                database=DATABASE['NAME'],
                user=DATABASE['USER'],
                password=DATABASE['PASSWORD'],
                host=DATABASE['HOST'],
                port=DATABASE['PORT']
            )
        except Exception as e:
            print(f"Error initializing database connection pool: {e}")
            raise

    def get_connection(self):
        try:
            return self.connection_pool.getconn()
        except Exception as e:
            print(f"Error getting connection from pool: {e}")
            raise

    def release_connection(self, conn):
        try:
            self.connection_pool.putconn(conn)
        except Exception as e:
            print(f"Error releasing connection back to pool: {e}")
            raise

    def close_all_connections(self):
        try:
            self.connection_pool.closeall()
        except Exception as e:
            print(f"Error closing all connections: {e}")
            raise







