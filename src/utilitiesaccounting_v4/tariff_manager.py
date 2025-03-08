import decimal
from abc import ABC, abstractmethod
from datetime import datetime, date
from decimal import Decimal
from typing import List
from dateutil.relativedelta import relativedelta


class TariffManager[T](ABC):
    @abstractmethod
    def calculate(self, schema: List[T]):
        ...


class SubscriptionTariffManager[T](TariffManager):
    """
    Вытащить тариф
    """

    def calculate(self, schema: List[T]):
        start_date: datetime.date = schema[0].from_date
        inc_date: date = start_date
        today = date.today()
        sum_: int = 0
        while inc_date < today:
            for tariff in schema:
                if not tariff.to_date:
                    tariff.to_date = date(datetime.today().year, datetime.today().month, datetime.today().day)
                if tariff.from_date <= inc_date < tariff.to_date and inc_date.month != today.month:
                    sum_ += decimal.Decimal(tariff.value)
            inc_date += relativedelta(months=1)
        print("sum_: ", sum_)
        return sum_


class ConsumptionVolumeTariffManager[T](TariffManager):
    def calculate(self, tariffs: List[T]):
        sum_: Decimal = Decimal('0')

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
        return sum_
