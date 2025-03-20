from abc import ABC, abstractmethod
from datetime import datetime, date
from decimal import Decimal
from typing import List
from dateutil.relativedelta import relativedelta

from src.utilitiesaccounting_v4.schemas.debt_dto import TypeTariff, SubscriptionTariff, OnTimeTariff, ConsumptionTariff


class TariffManager[T](ABC):
    tariff_type: int
    debt_dto: TypeTariff

    @abstractmethod
    def calculate(self, schema: List[T]) -> TypeTariff:
        ...


class SubscriptionTariffManager[T](TariffManager):
    """
    Вытащить тариф
    """
    tariff_type = 1
    debt_dto = SubscriptionTariff

    def calculate(self, schema: List[T]) -> List[TypeTariff]:
        res: List[TypeTariff] = []
        start_date: datetime.date = schema[0].from_date
        inc_date: date = start_date
        final_date = date(date.today().year, date.today().month, 1) - relativedelta(days=1)
        sum_: Decimal = Decimal('0')
        res_tariffs = {}
        while inc_date <= final_date:
            for tariff in schema:
                if not tariff.to_date:
                    tariff.to_date = date(datetime.today().year, datetime.today().month, datetime.today().day)
                if tariff.from_date <= inc_date < tariff.to_date:
                    sum_ += Decimal(str(tariff.value))
                res_tariffs[tariff.name] = res_tariffs.setdefault(tariff.name, 0) + sum_
            inc_date += relativedelta(months=1)
        for key, value in res_tariffs.items():
            res.append(self.debt_dto(
                value=str(value),
                tariff_type_name=key
            ))
        return res


class ConsumptionVolumeTariffManager[T](TariffManager):
    tariff_type = 2
    debt_dto = ConsumptionTariff

    def calculate(self, tariffs: List[T]) -> TypeTariff:
        sum_: Decimal = Decimal('0')
        res: List[TypeTariff] = []
        res_tariffs = {}

        for tariff in tariffs:
            if len(tariff.counter.counter_readings) > 1:
                for index, cr in enumerate(tariff.counter.counter_readings):
                    if index != 0:
                        check_date: date = cr.enter_date
                        if not tariff.to_date:
                            tariff.to_date = date.today()
                        if tariff.from_date <= check_date <= tariff.to_date:
                            diff = cr.value - tariff.counter.counter_readings[index - 1].value
                            sum_ += Decimal(str(diff)) * Decimal(str(tariff.value))
            res_tariffs[tariff.name] = res_tariffs.setdefault(tariff.name, 0) + sum_
        for key, value in res_tariffs.items():
            res.append(self.debt_dto(
                value=str(value),
                tariff_type_name=key
            ))
        return res


class OnTimeChargeTariffManager[T](TariffManager):
    debt_dto = OnTimeTariff

    def calculate(self, tariffs: List[T]):
        sum_: Decimal = Decimal('0')
        res: List[TypeTariff] = []

        for tariff in tariffs:
            sum_ += Decimal(str(tariff.value))
            res.append(self.debt_dto(
                value=str(sum_),
                tariff_type_name=tariff.name
            ))
        return res
