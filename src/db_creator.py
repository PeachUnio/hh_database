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
            conn = psycopg2.connect(**self.conn_params)
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()

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

    def create_tables(self) -> None:
        """Метод для создания таблицы в базе данных"""
        try:
            # Подключаемся к нашей БД
            conn_params_with_db = self.conn_params.copy()
            conn_params_with_db["database"] = os.getenv("DB_NAME")
            conn = psycopg2.connect(**conn_params_with_db)
            cursor = conn.cursor()

            # таблица employers
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employers (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    description TEXT,
                    area VARCHAR(100),
                    site_url VARCHAR(255),
                    alternate_url VARCHAR(255),
                    open_vacancies INTEGER
                )
            """)

            # таблица vacancies
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                    id INTEGER PRIMARY KEY,
                    employer_id INTEGER REFERENCES employers(id) ON DELETE CASCADE,
                    name VARCHAR(255) NOT NULL,
                    salary_from INTEGER,
                    salary_to INTEGER,
                    currency VARCHAR(10),
                    url VARCHAR(255),
                    requirement TEXT,
                    experience VARCHAR(100)
                )
            """)

            conn.commit()
            print("Таблицы созданы успешно")

            cursor.close()
            conn.close()

        except Exception as e:
            print(f"Ошибка при создании таблиц: {e}")
