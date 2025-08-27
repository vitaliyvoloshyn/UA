from abc import ABC
from decimal import Decimal
from typing import List, TypeVar, Self, Sequence

import loguru
from sqlalchemy import Row

from src.utilitiesaccounting_v4.repository import SqlRepository, SchemaModel
from src.utilitiesaccounting_v4.schemas.debt_dto import DebtDTO, TypeTariff
from src.utilitiesaccounting_v4.tariff_manager import TariffManager, ConsumptionVolumeTariffManager, \
    SubscriptionTariffManager, OnTimeChargeTariffManager
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
        provider_id = None
        category_photo = None
        for tm in self.tariff_managers:
            tariffs = self._get_tariffs(category_name=self.category_name,
                                        tariff_type=tm.tariff_type)
            dept.append(tm.calculate(tariffs))
            provider_id = self._get_provider_id(self.category_name)
            category_photo = self._get_category_photo(self.category_name)
        total_accrued = self._get_total_debt(dept)
        total_payment = self._get_payment()
        total_debt = str(Decimal(total_accrued) - Decimal(total_payment))
        return DebtDTO(
            category_name=self.category_name,
            category_photo=category_photo,
            provider_id=provider_id,
            debt=dept,
            total_accrued=total_accrued,
            total_payment=total_payment,
            total_debt=total_debt,
        )

    def _get_provider_id(self, category_name: str) -> int:
        with UnitOfWork() as uow:
            provider_id = uow.category.get_provider_id_by_category_name(category_name)
        return provider_id

    def _get_category_photo(self, category_name: str) -> str:
        with UnitOfWork() as uow:
            category = uow.category.get(name=category_name)
            loguru.logger.debug(category)
            if category:
                category = category[0]
        return category.photo

    @staticmethod
    def _get_total_debt(type_tariffs: List[TypeTariff]) -> str:
        total: Decimal = Decimal('0')
        for type_tariff in type_tariffs:
            for tariff in type_tariff.tariffs:
                total = Decimal(tariff.debt_value) + total

        return str(total.quantize(Decimal('1.00')))

    def add_tariff_manager(self, tm: T):
        self.tariff_managers.append(tm)

    def _get_tariffs(self, category_name: str, tariff_type: int):
        with self.storage_manager() as sm:
            tariffs = sm.tariff.get_tariffs_by_category_tariff_type(category_name=category_name,
                                                                    tariff_type=tariff_type)
            return tariffs

    def _get_payment(self):
        with self.storage_manager() as sm:
            category = sm.category.get(relation=True, name=self.category_name)
            provider = category[0].provider.id
            payments = sm.payment.get(provider_id=provider)
        return self._calc_total_payments(payments)

    def _calc_total_payments(self, payments: List[SchemaModel] | Sequence[Row]):
        res = Decimal('0')
        for p in payments:
            res = res + Decimal(p.value)
        return str(res)

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


class GasService[T](BaseService):
    category_name = 'Газопостачання'

    tariff_managers = [
        ConsumptionVolumeTariffManager(),
    ]


class POZService[T](BaseService):
    category_name = 'Обслуговування житла'

    tariff_managers = [
        SubscriptionTariffManager(),
    ]


class RubbishService[T](BaseService):
    category_name = 'Вивіз сміття'

    tariff_managers = [
        SubscriptionTariffManager(),
    ]


class HeatService[T](BaseService):
    category_name = 'Теплопостачання'

    tariff_managers = [
        SubscriptionTariffManager(),
        ConsumptionVolumeTariffManager(),
        OnTimeChargeTariffManager(),
    ]


class TransportGasService[T](BaseService):
    category_name = 'Розподіл газу'

    tariff_managers = [
        SubscriptionTariffManager(),
    ]


class InternetService[T](BaseService):
    category_name = 'Інтернет'

    tariff_managers = [
        SubscriptionTariffManager(),
    ]


water_service = WaterService()
electric_service = ElectricService()
gas_service = GasService()
poz_service = POZService()
rubbish_service = RubbishService()
heat_service = HeatService()
transport_gas_service = TransportGasService()
internet_service = InternetService()

if __name__ == '__main__':
    ...
