class Vacancy:
    """Класс для работы с вакансиями"""
    def __init__(self, vacancy_data, employer_id):
        self.id = vacancy_data.get("id")
        self.name = vacancy_data.get("name", "")
        self.employer_id = employer_id
        self.salary_from = self._get_salary(vacancy_data.get("salary"), "from")
        self.salary_to = self._get_salary(vacancy_data.get("salary"), "to")
        self.currency = self._get_currency(vacancy_data.get("salary"))
        self.url = vacancy_data.get("alternate_url", "")
        self.requirement = vacancy_data.get("snippet", {}).get("requirement", "")
        self.experience = vacancy_data.get("experience", {}).get("name", "")

    def _get_salary(self, salary_data, key):
        """Извлекает зарплату из данных"""
        if salary_data and salary_data.get(key):
            return salary_data[key]
        return None

    def _get_currency(self, salary_data):
        """Извлекает валюту из данных о зарплате"""
        if salary_data and salary_data.get("currency"):
            return salary_data["currency"]
        return None

