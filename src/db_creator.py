import psycopg2
import os
from dotenv import load_dotenv


class DBCreator:
    """Класс для создания базы данных"""
    def __init__(self):
        load_dotenv()
        self.conn_params = {
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT")
        }
