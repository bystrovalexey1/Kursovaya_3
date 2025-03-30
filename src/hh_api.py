import requests

from src.base_hh_api import BaseLoadVacancies
from src.config import COMPANY_ID


class HeadHunterAPI(BaseLoadVacancies):
    """Класс получает информацию о вакансиях с сайта HeadHunter"""

    def __init__(self):
        """Конструктор обьекта запроса инфо через API сервис"""

        self.__url = "https://api.hh.ru/"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = None
        self.employers = COMPANY_ID


    def load_vacancies(self):
        """Метод загрузки данных вакансий из API сервиса"""

        emp_params = {"sort_by": "by_vacancies_open"}
        employers = []
        for employer_id in self.employers:
            emp_url = f"{self.__url}employers/{employer_id}"
            response = requests.get(
                emp_url, headers=self.__headers, params=emp_params
            )
            if response.status_code == 200:
                employer_info = response.json()
                employers.append(employer_info)
            else:
                raise Exception(f"Ошибка {response.status_code}: {response.text}")

        return employers


    def correct_vacancy(self, num_vac):
        """Метод преобразования вакансий в корректный формат"""
        vac_url = f"{self.__url}vacancies"
        vacancies = []
        for emp in self.employers:
            vacancy_params = {
                "employer_id": emp,
                "per_page": num_vac,
                "only_with_salary": True,
            }
            response = requests.get(
                vac_url, headers=self.__headers, params=vacancy_params
            )
            if response.status_code == 200:
                vac = response.json()["items"]
                vacancies.extend(vac)
            else:
                raise Exception(f"Ошибка {response.status_code}: {response.text}")
        return vacancies


if __name__ == "__main__":
    hh = HeadHunterAPI()  # Создаем экземпляр класса
    hh_employers = hh.load_vacancies()  # список компаний id и name
    hh_vacancy = hh.correct_vacancy(1)
    print(hh_vacancy)