from db.db import Database
from dotenv import load_dotenv
import os

load_dotenv()
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

db_connection = Database(dbname=POSTGRES_DB, user=POSTGRES_USER, password=POSTGRES_PASSWORD, host="localhost")
# db_connection.create_table()
