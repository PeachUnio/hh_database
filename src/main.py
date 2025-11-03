from src.api import HhApi
from src.db_creator import DBCreator
from src.db_manger import DBManger


def main():
    """Функция для взаимодействия с пользователем"""

    print("1. Получение данных с HH.ru...")
    api = HhApi()
    companies_data = api.get_all_companies_data()

    print("2. Создание базы данных...")
    db_creator = DBCreator()
    db_creator.create_database()
    db_creator.create_tables()
    db_creator.fill_database(companies_data)

    print("3. Инициализация менеджера базы данных...")
    db_manager = DBManger()

    while True:
        print("\n" + "~" * 50)
        print("МЕНЮ:")
        print("1. Список компаний и количество вакансий")
        print("2. Список всех вакансий")
        print("3. Средняя зарплата по вакансиям")
        print("4. Вакансии с зарплатой выше средней")
        print("5. Поиск вакансий по ключевому слову")
        print("0. Выход")
        print("~" * 50)

        choice = input("Выберите пункт меню: ").strip()

        if choice == "1":
            print("\nКомпании и количество вакансий")
            companies = db_manager.get_companies_and_vacancies_count()
            for company, count in companies:
                print(f"{company}: {count} вакансий")

        elif choice == "2":
            print("\nВсе вакансии")
            vacancies = db_manager.get_all_vacancies()
            for company, name, salary_from, salary_to, currency, url in vacancies:
                salary_info = f"{salary_from} - {salary_to} {currency}" if salary_from or salary_to else "Не указана"
                print(f"{company}: {name}\nЗарплата: {salary_info}\nСсылка: {url}")

        elif choice == "3":
            print("\nСредняя зарплата")
            avg_salary = db_manager.get_avg_salary()
            print(f"Средняя зарплата по всем вакансиям: {avg_salary} руб.")

        elif choice == "4":
            print("\n--- Вакансии с зарплатой выше средней ---")
            high_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
            if high_salary_vacancies:
                for company, name, salary_from, salary_to, currency, url in high_salary_vacancies:
                    salary_info = f"{salary_from} - {salary_to} {currency}"
                    print(f"{company}: {name} | Зарплата: {salary_info} | Ссылка: {url}")
            else:
                print("Вакансий с зарплатой выше средней не найдено")

        elif choice == "5":
            keyword = input("Введите ключевое слово для поиска: ").strip()
            if keyword:
                print(f"\n--- Результаты поиска по '{keyword}' ---")
                found_vacancies = db_manager.get_vacancies_with_keyword(keyword)
                if found_vacancies:
                    for company, name, salary_from, salary_to, currency, url in found_vacancies:
                        salary_info = (
                            f"{salary_from} - {salary_to} {currency}" if salary_from or salary_to else "Не указана"
                        )
                        print(f"{company}: {name} | Зарплата: {salary_info} | Ссылка: {url}")
                else:
                    print(f"Вакансии по запросу '{keyword}' не найдены")
            else:
                print("Ключевое слово не может быть пустым")

        elif choice == "0":
            print("Выход из программы...")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
