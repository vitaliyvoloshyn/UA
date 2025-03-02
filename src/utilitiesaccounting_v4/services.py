from abc import ABC, abstractmethod
from typing import List, TypeVar

from src.utilitiesaccounting_v4.repository import SqlRepository
from src.utilitiesaccounting_v4.uow import UnitOfWork

REPO = TypeVar('REPO', bound=SqlRepository)


class BaseService(ABC):
    tariff_managers: List = []

    def __init__(self):
        self.storage_manager: type[UnitOfWork] = UnitOfWork

    @abstractmethod
    def calc(self):
        ...


class CategoryService(BaseService):
    def calc(self):
        ...


class MeasurementUnitService(BaseService):
    def calc(self):
        ...


class TariffTypeService(BaseService):
    def calc(self):
        ...

class TariffService(BaseService):
    def calc(self):
        ...


class ProviderService(BaseService):
    def calc(self):
        ...


class CounterService(BaseService):
    def calc(self):
        ...


class CounterReadingService(BaseService):
    def calc(self):
        ...


if __name__ == '__main__':
    ...
