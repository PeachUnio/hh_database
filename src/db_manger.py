import psycopg2
import os
from dotenv import load_dotenv


class DBManger:
    """Класс для управления базой данных"""
    def __init__(self):
        load_dotenv()
        self.conn_params = {
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "host": os.getenv("DB_HOST"),
            "port": os.getenv("DB_PORT")
        }

    def _execute_query(self, query, params=None):
        """Метод для отправки sql запроса"""
        try:
            with psycopg2.connect(**self.conn_params) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    return cursor.fetchall()
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return []

    def get_companies_and_vacancies_count(self):
        """Метод для получения списков всех компаний и количество вакансий у каждой компании"""
        query = """
                    SELECT e.name, COUNT(v.id) as vacancy_count
                    FROM employers e
                    LEFT JOIN vacancies v ON e.id = v.employer_id
                    GROUP BY e.id, e.name
                    ORDER BY vacancy_count DESC
                """
        return self._execute_query(query)

    def get_all_vacancies(self):
        """
        Метод для получения списков всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию
        """
        query = """
                    SELECT 
                        e.name as company_name,
                        v.name as vacancy_name,
                        COALESCE(v.salary_from, 0) as salary_from,
                        COALESCE(v.salary_to, 0) as salary_to,
                        v.currency,
                        v.url
                    FROM vacancies v
                    JOIN employers e ON v.employer_id = e.id
                    ORDER BY e.name, (COALESCE(v.salary_from, 0) + COALESCE(v.salary_to, 0)) / 2 DESC
                """
        return self._execute_query(query)

    def get_avg_salary(self):
        """Метод для получения средней зарплаты по вакансиям"""
        query = """
                    SELECT AVG((COALESCE(salary_from, 0) + COALESCE(salary_to, 0)) / 2) as avg_salary
                    FROM vacancies
                    WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL
                """
        result = self._execute_query(query)
        return round(result[0][0], 2) if result and result[0][0] else 0.0

    def get_vacancies_with_keyword(self, keyword):
        """Метод для получения списка всех вакансий, в названии которых содержатся переданные слова"""
        query = """
            SELECT 
                e.name as company_name,
                v.name as vacancy_name,
                COALESCE(v.salary_from, 0) as salary_from,
                COALESCE(v.salary_to, 0) as salary_to,
                v.currency,
                v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.id
            WHERE LOWER(v.name) LIKE LOWER(%s)
            ORDER BY e.name, (COALESCE(v.salary_from, 0) + COALESCE(v.salary_to, 0)) / 2 DESC
        """
        return self._execute_query(query, (f'%{keyword}%',))
