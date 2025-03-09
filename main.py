import os

from src.config import config
from src.dbmanager import DBManager
from src.utils import create_database, save_data_to_database, get_hh_vac_data, get_hh_comp_data


def main():

    params = config()
    top_n = int(input('Выберите количество вакансий в каждой компании: '))
    data_company = get_hh_comp_data()
    data_vacancy = get_hh_vac_data(top_n)
    create_database('hh', params)
    save_data_to_database(data_company, data_vacancy, 'hh', params)

    db_company = DBManager('hh', params)

    user_choise = input("""Выберите необходимое действие:
    1. Получить количество вакансий по каждой компании?
    2. Получить все вакансии по каждой компании?
    3. Получить среднюю зарплату по всем компаниям?
    4. Вывести вакансии, у которых зарплата больше чем средняя по всем компаниям?
    5. Вывести вакансии по ключевому слову в названии вакансии? 
    """)

    if user_choise == '1':
        result = db_company.get_companies_and_vacancies_count()
        for res in result:
            print(f"{res[0]} - {res[1]} вакансий.")

    elif user_choise == '2':
        result = db_company.get_all_vacancies()
        for res in result:
            print(f"Компания: {res[0]}, Вакансия: {res[1]}, Зарплата: от {res[2]} до {res[3]} руб., Ссылка: {res[5]}")

    elif user_choise == '3':
        print(db_company.get_avg_salary())

    elif user_choise == '4':
        result = db_company.get_vacancies_with_higher_salary()
        for res in result:
            print(f"{res[2]}, зарплата: от {res[3]} до {res[4]} руб., ссылка: {res[6]}, описание: {res[7]}")

    elif user_choise == '5':
        keyword = input("Введите ключевое слово:\n").title()
        result = db_company.get_vacancies_with_keyword(f"{keyword}")

        for res in result:
            print(f"{res[2]}, зарплата: от {res[3]} до {res[4]} руб., ссылка: {res[6]}, описание: {res[7]}")

    else:
        print('Вы ввели некорректное значение')


if __name__ == '__main__':
    main()