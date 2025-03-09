import requests

from src.base_hh_api import BaseLoadVacancies


class HeadHunterAPI(BaseLoadVacancies):
    """Класс получает информацию о вакансиях с сайта HeadHunter"""

    def __init__(self, file_worker: str = "data/json_vacancies.json"):
        """Конструктор обьекта запроса инфо через API сервис"""

        self.__url = 'https://api.hh.ru/'
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = None
        self.employers = [3529, 1740, 1122462, 2870783, 6093775, 1781300, 4181, 80, 67611, 2180]
        super().__init__(file_worker)

    def load_vacancies(self):
        """Метод загрузки данных вакансий из API сервиса"""

        emp_params = {
            "sort_by": "by_vacancies_open"
        }
        employers = []
        for employer_id in self.employers:
            emp_url = f"{self.__url}employers/{employer_id}"
            employer_info = requests.get(emp_url, headers=self.__headers, params=emp_params).json()
            employers.append(employer_info)

        return employers

    def correct_vacancy(self, num_vac):
        """Метод преобразования вакансий в корректный формат"""
        vac_url = f"{self.__url}vacancies"
        vacancies = []
        for emp in self.employers:
            vacancy_params = {
                "employer_id": emp,
                "per_page": num_vac,
                "only_with_salary": True
            }
            response = requests.get(vac_url, headers=self.__headers, params=vacancy_params)
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
