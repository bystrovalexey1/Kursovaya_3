from src.config import config
from typing import Any
import psycopg2

from src.hh_api import HeadHunterAPI


def get_hh_vac_data(top_n=1) -> list[dict[str, Any]]:
    """Получение базы данных вакансий с api HH.ru"""
    hh = HeadHunterAPI()
    data_vacancy = hh.correct_vacancy(top_n)
    return data_vacancy


def get_hh_comp_data() -> list[dict[str, Any]]:
    """Получение базы данных компаний с api HH.ru"""
    hh = HeadHunterAPI()
    data_company = hh.load_vacancies()
    return data_company


def create_database(database_name: str, params: dict) -> None:
    """Создание базы данных и таблиц для сохранения данных о компаниях и вакансиях"""
    params = config()
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f'DROP DATABASE {database_name}')
    cur.execute(f'CREATE DATABASE {database_name}')

    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE company (
                    id SERIAL UNIQUE,
                    company_id INT PRIMARY KEY,
                    company_name VARCHAR(255) NOT NULL);
        """)

    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE vacancy (
                    vacancy_id SERIAL PRIMARY KEY,
                    company_id INT REFERENCES company(company_id),
                    vacancy_name VARCHAR(255) NOT NULL,
                    salary_from INT DEFAULT(0),
                    salary_to INT DEFAULT(0),
                    salary_currency VARCHAR(50),
                    url VARCHAR(255),
                    description TEXT)
        """)

    conn.commit()
    conn.close()


def save_data_to_database(data_company: list[dict[str, Any]], data_vacancy: list[dict[str, Any]],  database_name: str, params: dict) -> None:
    """Сохранение данных о компаниях и вакансиях в базу данных"""
    params = config()
    conn = psycopg2.connect(dbname=database_name, **params)

    for emp in data_company:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO company (company_id, company_name)
                VALUES (%s, %s)
                RETURNING company_id
                """,
                vars=(emp['id'], emp["name"]),
            )

            company_id = cur.fetchone()[0]

            for vacancy in data_vacancy:
                if int(vacancy['employer']['id']) == int(company_id):
                    cur.execute(
                        """
                        INSERT INTO vacancy (company_id, vacancy_name, salary_from, salary_to, 
                        salary_currency, url, description)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            company_id,
                            vacancy["name"],
                            vacancy["salary"]["from"],
                            vacancy["salary"]["to"],
                            vacancy["salary"]["currency"],
                            vacancy["url"],
                            vacancy["snippet"]['responsibility'],
                        ),
                    )
                else:
                    continue

    conn.commit()
    conn.close()

