from abc import ABC, abstractmethod


class BaseLoadVacancies(ABC):
    """Базовый класс для получения вакансий из hh_api"""
    @abstractmethod
    def __init__(self):
        pass
