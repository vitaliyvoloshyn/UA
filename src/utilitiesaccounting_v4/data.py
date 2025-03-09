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
    CategoryAddDTO(name="Водопостачання"),  # id = 2
    CategoryAddDTO(name="Теплопостачання"),  # id = 3
    CategoryAddDTO(name="Газопостачання"),  # id = 4
    CategoryAddDTO(name="Розподіл газу"),  # id = 5
    CategoryAddDTO(name="Вивіз сміття"),  # id = 6
    CategoryAddDTO(name="Обслуговування житла"),  # id = 7
    CategoryAddDTO(name="Інтернет"),  # id = 8
    # CategoryAddDTO(name="Електропостачання"),       # id = 9
    # CategoryAddDTO(name="Електропостачання"),       # id = 10
    # CategoryAddDTO(name="Електропостачання"),       # id = 11
    # CategoryAddDTO(name="Електропостачання"),       # id = 12
    # CategoryAddDTO(name="Електропостачання"),       # id = 13
    # CategoryAddDTO(name="Електропостачання"),       # id = 14
    # CategoryAddDTO(name="Електропостачання"),       # id = 15
]

providers = [
    ProviderAddDTO(name='ТОВ "КИЇВСЬКА ОБЛАСНА ЕК"', category_id=1),  # id = 1
    ProviderAddDTO(name='Українське ВКП', category_id=2),  # id = 2
    ProviderAddDTO(name='ПАТ "Центренерго" Трипільська ТЕС', category_id=3),  # id = 3
    ProviderAddDTO(name='Нафтогаз', category_id=4),  # id = 4
    ProviderAddDTO(name='ГАЗМЕРЕЖІ Київська філія', category_id=5),  # id = 5
    ProviderAddDTO(name='Профпереробка', category_id=6),  # id = 6
    ProviderAddDTO(name='ПОЖ', category_id=7),  # id = 7
    ProviderAddDTO(name='Євролінк', category_id=8),  # id = 8
    # ProviderAddDTO(name='', category_id=9),  # id = 9
    # ProviderAddDTO(name='', category_id=10),  # id = 10
    # ProviderAddDTO(name='', category_id=11),  # id = 11
    # ProviderAddDTO(name='', category_id=12),  # id = 12
    # ProviderAddDTO(name='', category_id=13),  # id = 13
    # ProviderAddDTO(name='', category_id=14),  # id = 14
    # ProviderAddDTO(name='', category_id=15),  # id = 15
]

counters = [
    CounterAddDTO(name="Лічильник електроенергії", measurement_unit_id=1),  # id = 1
    CounterAddDTO(name="Лічильник електроенергії денний тариф", measurement_unit_id=1),  # id = 2
    CounterAddDTO(name="Лічильник електроенергії нічний тариф", measurement_unit_id=1),  # id = 3
    CounterAddDTO(name="Лічильник газу", measurement_unit_id=2),  # id = 4
    CounterAddDTO(name="Лічильник гарячої води", measurement_unit_id=2),  # id = 5
    CounterAddDTO(name="Лічильник холодної води", measurement_unit_id=2),  # id = 6
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
        from_date=datetime.date(2024, 1, 1),
        to_date=None,
        tariff_type_id=2,
        provider_id=1,
        counter_id=2
    ),
    TariffAddDTO(
        name='Нічний тариф',  # id = 4
        value='2.16',
        from_date=datetime.date(2024, 1, 1),
        to_date=None,
        tariff_type_id=2,
        provider_id=1,
        counter_id=3
    ),
    TariffAddDTO(
        name='Споживання газу',  # id = 5
        value='7.95689',
        from_date=datetime.date(2024, 1, 1),
        to_date=None,
        tariff_type_id=2,
        provider_id=4,
        counter_id=4
    ),
    TariffAddDTO(
        name='Підігрів гарячої води',  # id = 6
        value='39.51',
        from_date=datetime.date(2024, 1, 1),
        to_date=None,
        tariff_type_id=2,
        provider_id=3,
        counter_id=5
    ),
    TariffAddDTO(
        name='Абонплата',  # id = 7   ЦЕНТРЕНЕРГО
        value='25.88',
        from_date=datetime.date(2024, 1, 1),
        to_date=datetime.date(2024, 9, 30),
        tariff_type_id=1,
        provider_id=3,
        counter_id=None
    ),
    TariffAddDTO(
        name='Абонплата',  # id = 8   ЦЕНТРЕНЕРГО
        value='28.32',
        from_date=datetime.date(2024, 1, 1),
        to_date=None,
        tariff_type_id=1,
        provider_id=3,
        counter_id=None
    ),
    TariffAddDTO(
        name='Абонплата',  # id = 9   УВКП
        value='34.70',
        from_date=datetime.date(2024, 1, 1),
        to_date=datetime.date(2024, 2, 29),
        tariff_type_id=1,
        provider_id=2,
        counter_id=None
    ),
    TariffAddDTO(
        name='Абонплата',  # id = 10   УВКП
        value='19.10',
        from_date=datetime.date(2024, 3, 1),
        to_date=datetime.date(2024, 12, 31),
        tariff_type_id=1,
        provider_id=2,
        counter_id=None
    ),
    TariffAddDTO(
        name='Абонплата',  # id = 11   УВКП
        value='16.54',
        from_date=datetime.date(2025, 1, 1),
        to_date=None,
        tariff_type_id=1,
        provider_id=2,
        counter_id=None
    ),
    TariffAddDTO(
        name='Споживання холодної води',  # id = 12   УВКП
        value='62.68',
        from_date=datetime.date(2024, 1, 1),
        to_date=datetime.date(2024, 2, 29),
        tariff_type_id=2,
        provider_id=2,
        counter_id=6
    ),
    TariffAddDTO(
        name='Споживання холодної води',  # id = 13   УВКП
        value='78.62',
        from_date=datetime.date(2024, 3, 1),
        to_date=None,
        tariff_type_id=2,
        provider_id=2,
        counter_id=6
    ),
    TariffAddDTO(
        name='Споживання гарячої води',  # id = 14   УВКП
        value='62.68',
        from_date=datetime.date(2024, 1, 1),
        to_date=datetime.date(2024, 2, 29),
        tariff_type_id=2,
        provider_id=2,
        counter_id=5
    ),
    TariffAddDTO(
        name='Споживання гарячої води',  # id = 15   УВКП
        value='78.62',
        from_date=datetime.date(2024, 3, 1),
        to_date=None,
        tariff_type_id=2,
        provider_id=2,
        counter_id=5
    ),
]

counter_readings = [
    # electric
    CounterReadingAddDTO(name="-", value=4763, enter_date=datetime.date(2023, 12, 31), counter_id=1),
    CounterReadingAddDTO(name="-", value=4898, enter_date=datetime.date(2024, 1, 31), counter_id=1),
    CounterReadingAddDTO(name="-", value=5023, enter_date=datetime.date(2024, 2, 29), counter_id=1),
    CounterReadingAddDTO(name="-", value=5156, enter_date=datetime.date(2024, 3, 31), counter_id=1),
    CounterReadingAddDTO(name="-", value=5305, enter_date=datetime.date(2024, 4, 30), counter_id=1),
    CounterReadingAddDTO(name="-", value=5649, enter_date=datetime.date(2024, 5, 31), counter_id=1),
    CounterReadingAddDTO(name="-", value=5757, enter_date=datetime.date(2024, 6, 30), counter_id=1),
    CounterReadingAddDTO(name="-", value=5980, enter_date=datetime.date(2024, 7, 31), counter_id=1),
    CounterReadingAddDTO(name="-", value=6214, enter_date=datetime.date(2024, 8, 31), counter_id=1),
    CounterReadingAddDTO(name="-", value=6433, enter_date=datetime.date(2024, 9, 30), counter_id=1),
    CounterReadingAddDTO(name="-", value=6773, enter_date=datetime.date(2024, 10, 31), counter_id=1),
    CounterReadingAddDTO(name="-", value=6918, enter_date=datetime.date(2024, 11, 30), counter_id=1),
    CounterReadingAddDTO(name="-", value=7131, enter_date=datetime.date(2024, 12, 31), counter_id=1),
    CounterReadingAddDTO(name="-", value=7312, enter_date=datetime.date(2025, 1, 31), counter_id=1),
    CounterReadingAddDTO(name="-", value=7480, enter_date=datetime.date(2025, 2, 28), counter_id=1),
    # cold water
    CounterReadingAddDTO(name="-", value=1172, enter_date=datetime.date(2023, 12, 31), counter_id=6),
    CounterReadingAddDTO(name="-", value=1176, enter_date=datetime.date(2024, 1, 31), counter_id=6),
    CounterReadingAddDTO(name="-", value=1181, enter_date=datetime.date(2024, 2, 29), counter_id=6),
    CounterReadingAddDTO(name="-", value=1185, enter_date=datetime.date(2024, 3, 31), counter_id=6),
    CounterReadingAddDTO(name="-", value=1189, enter_date=datetime.date(2024, 4, 30), counter_id=6),
    CounterReadingAddDTO(name="-", value=1195, enter_date=datetime.date(2024, 5, 31), counter_id=6),
    CounterReadingAddDTO(name="-", value=1201, enter_date=datetime.date(2024, 6, 30), counter_id=6),
    CounterReadingAddDTO(name="-", value=1208, enter_date=datetime.date(2024, 7, 31), counter_id=6),
    CounterReadingAddDTO(name="-", value=1215, enter_date=datetime.date(2024, 8, 31), counter_id=6),
    CounterReadingAddDTO(name="-", value=1215, enter_date=datetime.date(2024, 9, 30), counter_id=6),
    CounterReadingAddDTO(name="-", value=1229, enter_date=datetime.date(2024, 10, 31), counter_id=6),
    CounterReadingAddDTO(name="-", value=1233, enter_date=datetime.date(2024, 11, 30), counter_id=6),
    CounterReadingAddDTO(name="-", value=1238, enter_date=datetime.date(2024, 12, 31), counter_id=6),
    CounterReadingAddDTO(name="-", value=1243, enter_date=datetime.date(2025, 1, 31), counter_id=6),
    CounterReadingAddDTO(name="-", value=1247, enter_date=datetime.date(2025, 2, 28), counter_id=6),
    # hot water
    CounterReadingAddDTO(name="-", value=574, enter_date=datetime.date(2023, 12, 31), counter_id=5),
    CounterReadingAddDTO(name="-", value=577, enter_date=datetime.date(2024, 1, 31), counter_id=5),
    CounterReadingAddDTO(name="-", value=580, enter_date=datetime.date(2024, 2, 29), counter_id=5),
    CounterReadingAddDTO(name="-", value=583, enter_date=datetime.date(2024, 3, 31), counter_id=5),
    CounterReadingAddDTO(name="-", value=584, enter_date=datetime.date(2024, 4, 30), counter_id=5),
    CounterReadingAddDTO(name="-", value=584, enter_date=datetime.date(2024, 5, 31), counter_id=5),
    CounterReadingAddDTO(name="-", value=584, enter_date=datetime.date(2024, 6, 30), counter_id=5),
    CounterReadingAddDTO(name="-", value=584, enter_date=datetime.date(2024, 7, 31), counter_id=5),
    CounterReadingAddDTO(name="-", value=584, enter_date=datetime.date(2024, 8, 31), counter_id=5),
    CounterReadingAddDTO(name="-", value=584, enter_date=datetime.date(2024, 9, 30), counter_id=5),
    CounterReadingAddDTO(name="-", value=584, enter_date=datetime.date(2024, 10, 31), counter_id=5),
    CounterReadingAddDTO(name="-", value=586, enter_date=datetime.date(2024, 11, 30), counter_id=5),
    CounterReadingAddDTO(name="-", value=588, enter_date=datetime.date(2024, 12, 31), counter_id=5),
    CounterReadingAddDTO(name="-", value=590, enter_date=datetime.date(2025, 1, 31), counter_id=5),
    CounterReadingAddDTO(name="-", value=591, enter_date=datetime.date(2025, 2, 28), counter_id=5),
    # gas
    CounterReadingAddDTO(name="-", value=431, enter_date=datetime.date(2023, 12, 31), counter_id=4),
    CounterReadingAddDTO(name="-", value=438, enter_date=datetime.date(2024, 1, 31), counter_id=4),
    CounterReadingAddDTO(name="-", value=446, enter_date=datetime.date(2024, 2, 29), counter_id=4),
    CounterReadingAddDTO(name="-", value=456, enter_date=datetime.date(2024, 3, 31), counter_id=4),
    CounterReadingAddDTO(name="-", value=466, enter_date=datetime.date(2024, 4, 30), counter_id=4),
    CounterReadingAddDTO(name="-", value=473, enter_date=datetime.date(2024, 5, 31), counter_id=4),
    CounterReadingAddDTO(name="-", value=408, enter_date=datetime.date(2024, 6, 30), counter_id=4),
    CounterReadingAddDTO(name="-", value=488, enter_date=datetime.date(2024, 7, 31), counter_id=4),
    CounterReadingAddDTO(name="-", value=498, enter_date=datetime.date(2024, 8, 31), counter_id=4),
    CounterReadingAddDTO(name="-", value=507, enter_date=datetime.date(2024, 9, 30), counter_id=4),
    CounterReadingAddDTO(name="-", value=516, enter_date=datetime.date(2024, 10, 31), counter_id=4),
    CounterReadingAddDTO(name="-", value=523, enter_date=datetime.date(2024, 11, 30), counter_id=4),
    CounterReadingAddDTO(name="-", value=530, enter_date=datetime.date(2024, 12, 31), counter_id=4),
    CounterReadingAddDTO(name="-", value=536, enter_date=datetime.date(2025, 1, 31), counter_id=4),
    CounterReadingAddDTO(name="-", value=541, enter_date=datetime.date(2025, 2, 28), counter_id=4),

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
