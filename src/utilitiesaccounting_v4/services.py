from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List, TypeVar, Self

from src.utilitiesaccounting_v4.repository import SqlRepository
from src.utilitiesaccounting_v4.schemas.debt_dto import DebtDTO, TypeTariff
from src.utilitiesaccounting_v4.tariff_manager import TariffManager, ConsumptionVolumeTariffManager, \
    SubscriptionTariffManager
from src.utilitiesaccounting_v4.uow import UnitOfWork

REPO = TypeVar('REPO', bound=SqlRepository)
T = TypeVar("T", bound=TariffManager)


class BaseService[T](ABC):
    category_name: str
    tariff_managers: List[TariffManager] = []
    instances: List[Self] = []
    storage_manager: type[UnitOfWork] = UnitOfWork
    a: int = 0

    def __init__(self):
        self._add_instance(self)

    def calc_all_services(self):
        return [s.calc() for s in self.instances]

    def calc(self):
        dept = []
        for tm in self.tariff_managers:
            tariffs = self._get_tariffs(category_name=self.category_name,
                                        tariff_type=tm.tariff_type)
            dept.extend(tm.calculate(tariffs))
        return DebtDTO(
            category_name=self.category_name,
            debt=dept,
            total_debt=self._get_total_debt(dept)
        )

    @staticmethod
    def _get_total_debt(type_tariffs: List[TypeTariff]) -> str:
        total: Decimal = Decimal('0')
        for type_tariff in type_tariffs:
            total = type_tariff + total

        return str(total)

    def add_tariff_manager(self, tm: T):
        self.tariff_managers.append(tm)

    def _get_tariffs(self, category_name: str, tariff_type: int):
        with self.storage_manager() as sm:
            tariffs = sm.tariff.get_tariffs_by_category_tariff_type(category_name, tariff_type)
            return tariffs

    def _add_instance(self, instance_: Self):
        if instance_.__class__.__name__ not in [o.__class__.__name__ for o in self.instances]:
            self.instances.append(instance_)


class ElectricService[T](BaseService):
    category_name = 'Електропостачання'

    tariff_managers = [
        ConsumptionVolumeTariffManager()
    ]


class WaterService[T](BaseService):
    category_name = 'Водопостачання'

    tariff_managers = [
        ConsumptionVolumeTariffManager(),
        SubscriptionTariffManager(),
    ]


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
