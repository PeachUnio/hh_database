import requests
from data import COMPANIES


class HhApi:
    """Класс для работы с API hh.ru"""
    def __init__(self):
        self.base_url = "https://api.hh.ru/"

    def get_employer_info(self, employer_id):
        """Метод для получения информации о компании по id"""
        employer_id = int(employer_id)
        url = f"{self.base_url}employers/{employer_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Произошла ошибка при получении данных о работодателе с id {employer_id}: {e}")
            return None

    def get_employer_vac(self, employer_id):
        """Метод для получения вакансий от работодателя"""
        employer_id = int(employer_id)
        url = f"{self.base_url}vacancies"
        params = {
            "employer_id": employer_id,
            "per_page": 100,
            "page": 0
        }
        vac = []
        try:
            while True:
                response = requests.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                vac.extend(data.get("items", []))

                if params["page"] >= data.get("pages", 1) - 1:
                    break
                params["page"] += 1

        except requests.exceptions.RequestException as e:
            print(f"Произошла ошибка при получении данных о работодателе с id {employer_id}: {e}")
        return vac

    def get_all_companies_data(self):
        """Получение данных обо всех компаниях из списка и их вакансиях"""
        companies_data = {}

        for company in COMPANIES:
            # информация о компании
            employer_info  = self.get_employer_info(company["id"])
            if not employer_info:
                continue

            # информация о вакансиях компании
            vac = self.get_employer_vac(company["id"])

            companies_data[company["id"]] = {
                "employer_info": employer_info,
                "vacancies": vac
            }

        return companies_data

print(HhApi().get_all_companies_data())