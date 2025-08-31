import calendar
from abc import ABC, abstractmethod
from datetime import datetime, date
from decimal import Decimal
from typing import List
from dateutil.relativedelta import *
from pydantic import BaseModel

from src.utilitiesaccounting.schemas.debt_dto import TypeTariff, SubscriptionTariff, OnTimeTariff, ConsumptionTariff, \
    ConsumptionTariffs, SubscriptionTariffs, OnTimeTariffs


class TariffManager[T](ABC):
    tariff_type: int
    debt_dto: TypeTariff
    debts_dto: BaseModel

    @abstractmethod
    def calculate(self, schema: List[T]) -> TypeTariff:
        ...


class SubscriptionTariffManager[T](TariffManager):
    """
    Вытащить тариф
    """
    tariff_type = 1
    debt_dto = SubscriptionTariff
    debts_dto = SubscriptionTariffs

    def calculate(self, tariffs: List[T]) -> SubscriptionTariffs:
        return self.debts_dto(
            tariffs=[self.calc_one_tariff(tariff) for tariff in tariffs],
        )

    def calc_one_tariff(self, tariff: T) -> TypeTariff:
        """Возвращает SubscriptionTariff DTO Model по одному тарифу"""
        sum_: Decimal = Decimal('0')
        start_date: datetime.date = tariff.from_date
        final_date = date(date.today().year, date.today().month, 1) - relativedelta(days=1)
        inc_date: date = start_date
        active: bool = False
        while inc_date <= final_date:
            if not tariff.to_date:
                tariff.to_date = date(datetime.today().year, datetime.today().month, datetime.today().day)
                active = True
            if tariff.from_date <= inc_date < tariff.to_date:
                sum_ += Decimal(str(tariff.value))
            inc_date += relativedelta(months=1)
        return self.debt_dto(
            value=tariff.value,
            debt_value=str(sum_),
            is_active=active,
            tariff_type_name=tariff.name,
        )


class ConsumptionVolumeTariffManager[T](TariffManager):
    tariff_type = 2
    debt_dto = ConsumptionTariff
    debts_dto = ConsumptionTariffs

    def calculate(self, tariffs: List[T]) -> ConsumptionTariffs:
        return self.debts_dto(
            tariffs=[self.calc_one_tariff(tariff) for tariff in tariffs],
        )

    def calc_one_tariff(self, tariff: T) -> TypeTariff:
        """Возвращает ConsumptionTariff DTO Model по одному тарифу"""
        sum_: Decimal = Decimal('0')
        active = False
        if not tariff.to_date:
            tariff.to_date = date.today()
            active = True
        if len(tariff.counter.counter_readings) > 1:
            for index, cr in enumerate(tariff.counter.counter_readings):
                if index != 0:
                    check_date: date = cr.enter_date
                    if tariff.from_date <= check_date <= tariff.to_date:
                        diff = cr.value - tariff.counter.counter_readings[index - 1].value
                        sum_ += Decimal(str(diff)) * Decimal(str(tariff.value))
        cur_readings = tariff.counter.counter_readings[-1].value if tariff.counter.counter_readings else None
        prev_readings = tariff.counter.counter_readings[-2].value if len(
                tariff.counter.counter_readings) > 1 else None
        diff = cur_readings - prev_readings if cur_readings and prev_readings else None
        res = self.debt_dto(
            value=tariff.value,
            debt_value=str(sum_),
            tariff_type_name=tariff.name,
            is_active=active,
            cur_readings=cur_readings,
            prev_readings=prev_readings,
            diff=diff,
        )
        return res


class OnTimeChargeTariffManager[T](TariffManager):
    tariff_type = 3
    debt_dto = OnTimeTariff
    debts_dto = OnTimeTariffs

    def calculate(self, tariffs: List[T]) -> OnTimeTariffs:
        return self.debts_dto(
            tariffs=[self.calc_one_tariff(tariff) for tariff in tariffs],
        )

    def calc_one_tariff(self, tariff: T) -> OnTimeTariff:
        """Возвращает OneTimeTariff DTO Model по одному тарифу"""
        is_active: bool = False
        start_date_check = date(date.today().year, date.today().month, 1)-relativedelta(months=1)
        end_date_check = date(date.today().year, date.today().month, 1) - relativedelta(days=1)

        if start_date_check <= tariff.from_date <= end_date_check:
            is_active = True

        res: OnTimeTariff = self.debt_dto(
            value=tariff.value,
            debt_value=tariff.value,
            tariff_type_name=tariff.name,
            is_active=is_active,
        )
        return res
