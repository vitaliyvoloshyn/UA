import decimal
from abc import ABC, abstractmethod
from datetime import datetime, timedelta, date
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
        sum: int = 0
        while inc_date < today:
            for tariff in schema:
                if not tariff.to_date:
                    tariff.to_date = date(datetime.today().year, datetime.today().month, datetime.today().day)
                if tariff.from_date <= inc_date < tariff.to_date and inc_date.month != today.month:
                    sum += decimal.Decimal(tariff.value)
            inc_date += relativedelta(months=1)
        print("sum: ", sum)
        return sum
