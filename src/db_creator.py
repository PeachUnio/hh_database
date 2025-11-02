import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
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

    def create_database(self):
        """Метод для создания базы данных"""
        try:
            # Подключаемся к postgres БД для создания новой БД
            conn = psycopg2.connect(**self.conn_params)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()

            # Проверяем существование БД
            cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{os.getenv("DB_NAME")}'")
            exists = cursor.fetchone()

            if not exists:
                cursor.execute(f"CREATE DATABASE {os.getenv("DB_NAME")}")
                print(f"База данных {os.getenv("DB_NAME")} создана успешно")
            else:
                print(f"База данных {os.getenv("DB_NAME")} уже существует")

            cursor.close()
            conn.close()

        except Exception as e:
            print(f"Ошибка при создании базы данных: {e}")