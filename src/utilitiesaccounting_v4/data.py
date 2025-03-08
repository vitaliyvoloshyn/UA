"""Добавление тестовых данных в БД"""
import datetime
from dataclasses import dataclass
from typing import TypeVar, Sequence

from pydantic import BaseModel

from src.utilitiesaccounting_v4.uow import UnitOfWork

from src.utilitiesaccounting_v4.schemas.category_dto import CategoryAddDTO
from src.utilitiesaccounting_v4.schemas.counter_dto import CounterAddDTO
from src.utilitiesaccounting_v4.schemas.counter_reading_dto import CounterReadingAddDTO
from src.utilitiesaccounting_v4.schemas.measurement_unit_dto import MeasurementUnitAddDTO
from src.utilitiesaccounting_v4.schemas.provider_dto import ProviderAddDTO
from src.utilitiesaccounting_v4.schemas.tariff_dto import TariffAddDTO
from src.utilitiesaccounting_v4.schemas.tariff_type_dto import TariffTypeAddDTO

"""Порядок добавления сущностей в БД
- единицы измерения;
- типы тарифов;
- счетчики;
- категория;
- оператор;
"""

B = TypeVar("B", bound=BaseModel)

measurement_units = [
    MeasurementUnitAddDTO(value="кВт*год"),  # id = 1
    MeasurementUnitAddDTO(value="м3"),  # id = 2
]

tariff_types = [
    TariffTypeAddDTO(name='Щомісячне нарахування'),  # id = 1
    TariffTypeAddDTO(name="За спожитий об'єм"),  # id = 2
    TariffTypeAddDTO(name='Разове нарахування'),  # id = 3
]

categories = [
    CategoryAddDTO(name="Електропостачання"),  # id = 1
]

providers = [
    ProviderAddDTO(name="ДТЕК", category_id=1),  # id = 1
]

counters = [
    CounterAddDTO(name="Лічильник електроенергії", measurement_unit_id=1),  # id = 1
    CounterAddDTO(name="Лічильник електроенергії денний тариф", measurement_unit_id=1),  # id = 2
    CounterAddDTO(name="Лічильник електроенергії нічний тариф", measurement_unit_id=1),  # id = 3
]

tariffs = [
    TariffAddDTO(
        name='Однозонний тариф',  # id = 1
        value='2.64',
        from_date=datetime.date(2024, 1, 1),
        to_date=datetime.date(2024, 4, 30),
        tariff_type_id=2,
        provider_id=1,
        counter_id=1
    ),
    TariffAddDTO(
        name='Однозонний тариф',  # id = 2
        value='4.32',
        from_date=datetime.date(2024, 5, 1),
        to_date=datetime.date(2024, 12, 31),
        tariff_type_id=2,
        provider_id=1,
        counter_id=1
    ),
    TariffAddDTO(
        name='Денний тариф',  # id = 3
        value='4.32',
        from_date=datetime.date(2025, 1, 1),
        to_date=None,
        tariff_type_id=2,
        provider_id=1,
        counter_id=2
    ),
    TariffAddDTO(
        name='Денний тариф',  # id = 4
        value='2.16',
        from_date=datetime.date(2025, 1, 1),
        to_date=None,
        tariff_type_id=2,
        provider_id=1,
        counter_id=3
    ),
]

counter_readings = [
    CounterReadingAddDTO(name="Споживання", value=4763, enter_date=datetime.date(2023, 12, 31), counter_id=1),
    CounterReadingAddDTO(name="Споживання", value=4898, enter_date=datetime.date(2024, 1, 31), counter_id=1),
    CounterReadingAddDTO(name="Споживання", value=5023, enter_date=datetime.date(2024, 2, 29), counter_id=1),
    CounterReadingAddDTO(name="Споживання", value=5156, enter_date=datetime.date(2024, 3, 31), counter_id=1),
    CounterReadingAddDTO(name="Споживання", value=5305, enter_date=datetime.date(2024, 4, 30), counter_id=1),
    CounterReadingAddDTO(name="Споживання", value=5649, enter_date=datetime.date(2024, 5, 31), counter_id=1),
    CounterReadingAddDTO(name="Споживання", value=5757, enter_date=datetime.date(2024, 6, 30), counter_id=1),
    CounterReadingAddDTO(name="Споживання", value=5980, enter_date=datetime.date(2024, 7, 31), counter_id=1),
    CounterReadingAddDTO(name="Споживання", value=6214, enter_date=datetime.date(2024, 8, 31), counter_id=1),
    CounterReadingAddDTO(name="Споживання", value=6433, enter_date=datetime.date(2024, 9, 30), counter_id=1),
    CounterReadingAddDTO(name="Споживання", value=6773, enter_date=datetime.date(2024, 10, 31), counter_id=1),
    CounterReadingAddDTO(name="Споживання", value=6918, enter_date=datetime.date(2024, 11, 30), counter_id=1),
    CounterReadingAddDTO(name="Споживання", value=7131, enter_date=datetime.date(2024, 12, 31), counter_id=1),
    CounterReadingAddDTO(name="Споживання", value=7312, enter_date=datetime.date(2025, 1, 31), counter_id=1),
    CounterReadingAddDTO(name="Споживання", value=7480, enter_date=datetime.date(2025, 2, 28), counter_id=1),
    CounterReadingAddDTO(name="Денний тариф", value=7300, enter_date=datetime.date(2025, 3, 1), counter_id=2),
    CounterReadingAddDTO(name="Нічний тариф", value=7312, enter_date=datetime.date(2025, 3, 1), counter_id=3)
]


@dataclass
class Repositories:
    c: str = 'category'
    p: str = 'provider'
    m: str = 'measurement_unit'
    tt: str = 'tariff_type'
    t: str = 'tariff'
    cntr: str = 'counter'
    cr: str = 'counter_reading'


def add_(records: Sequence[B], repo: str) -> None:
    with UnitOfWork() as uow:
        uow.__getattribute__(repo).add_all(records)


def add_data():
    add_(tariff_types, Repositories.tt)
    add_(measurement_units, Repositories.m)
    add_(categories, Repositories.c)
    add_(providers, Repositories.p)
    add_(counters, Repositories.cntr)
    add_(tariffs, Repositories.t)
    add_(counter_readings, Repositories.cr)


if __name__ == '__main__':
    add_(tariff_types, Repositories.tt)
