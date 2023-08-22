import psycopg2

from core.database import Database

db = Database()
db.initialize()
def execute_query(query, values=None):
    conn = db.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, values)
            conn.commit()
            try:
                result = cursor.fetchall()
                return result
            except psycopg2.ProgrammingError:
                return None
    finally:
        db.release_connection(conn)
