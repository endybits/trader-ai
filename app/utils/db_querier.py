import sys
import mariadb

from app.config.fconfig import get_db_credentials as DB

db = DB()
HOST = db.get("host")
USER = db.get("user")
PASSWORD = db.get("password")
DATABASE = db.get("database")
TARGET_TABLE = db.get("target_table")

def get_db_connection():
    try:
        conn = mariadb.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            database=DATABASE,
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)
    return conn

def exec_query(query: str):
    cursor = get_db_connection().cursor()
    cursor.execute(query)
    db_response = cursor.fetchall()
    return db_response