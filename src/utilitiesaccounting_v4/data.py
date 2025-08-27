"""Добавление тестовых данных в БД"""
import datetime
from dataclasses import dataclass
from typing import TypeVar, Sequence

from pydantic import BaseModel

from src.utilitiesaccounting_v4.schemas.payment_dto import PaymentAddDTO
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
    CategoryAddDTO(name="Електропостачання", photo='/asset/img/electricity-612x612.jpg'),  # id = 1
    CategoryAddDTO(name="Водопостачання", photo='/asset/img/water.webp'),  # id = 2
    CategoryAddDTO(name="Теплопостачання", photo='/asset/img/heat.jpg'),  # id = 3
    CategoryAddDTO(name="Газопостачання", photo='/asset/img/gaz-1024x740.jpg'),  # id = 4
    CategoryAddDTO(name="Розподіл газу", photo='/asset/img/transport_gas.jpg'),  # id = 5
    CategoryAddDTO(name="Вивіз сміття", photo='/asset/img/rubbish.jpg'),  # id = 6
    CategoryAddDTO(name="Обслуговування житла", photo='/asset/img/poz.jpg'),  # id = 7
    CategoryAddDTO(name="Інтернет", photo='/asset/img/internet.jpg'),  # id = 8
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
]

counters = [
    CounterAddDTO(name="Лічильник електроенергії", measurement_unit_id=1, is_active=False),  # id = 1
    CounterAddDTO(name="Лічильник електроенергії денний тариф", measurement_unit_id=1),  # id = 2
    CounterAddDTO(name="Лічильник електроенергії нічний тариф", measurement_unit_id=1),  # id = 3
    CounterAddDTO(name="Лічильник газу", measurement_unit_id=2),  # id = 4
    CounterAddDTO(name="Лічильник гарячої води", measurement_unit_id=2),  # id = 5
    CounterAddDTO(name="Лічильник холодної води", measurement_unit_id=2),  # id = 6
]

tariffs = [
    TariffAddDTO(
        name='Однозонний тариф',  # id = 1
        value='1.44',
        from_date=datetime.date(2022, 10, 1),
        to_date=datetime.date(2023, 5, 31),
        tariff_type_id=2,
        provider_id=1,
        counter_id=1
    ),
    TariffAddDTO(
        name='Однозонний тариф',  # id = 1
        value='2.64',
        from_date=datetime.date(2023, 6, 1),
        to_date=datetime.date(2024, 5, 31),
        tariff_type_id=2,
        provider_id=1,
        counter_id=1
    ),
    TariffAddDTO(
        name='Однозонний тариф',  # id = 2
        value='4.32',
        from_date=datetime.date(2024, 6, 1),
        to_date=datetime.date(2025, 3, 31),
        tariff_type_id=2,
        provider_id=1,
        counter_id=1
    ),
    TariffAddDTO(
        name='Денний тариф',  # id = 3
        value='4.32',
        from_date=datetime.date(2025, 4, 1),
        to_date=None,
        tariff_type_id=2,
        provider_id=1,
        counter_id=2
    ),
    TariffAddDTO(
        name='Нічний тариф',  # id = 4
        value='2.16',
        from_date=datetime.date(2025, 1, 1),
        to_date=None,
        tariff_type_id=2,
        provider_id=1,
        counter_id=3
    ),
    TariffAddDTO(
        name='Споживання газу',  # id = 5
        value='7.95689',
        from_date=datetime.date(2022, 10, 1),
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
        from_date=datetime.date(2024, 6, 1),
        to_date=datetime.date(2024, 9, 30),
        tariff_type_id=1,
        provider_id=3,
        counter_id=None
    ),
    TariffAddDTO(
        name='Опалення',  # id = 7   ЦЕНТРЕНЕРГО
        value='88.69',
        from_date=datetime.date(2024, 10, 31),
        to_date=None,
        tariff_type_id=3,
        provider_id=3,
        counter_id=None
    ),
    TariffAddDTO(
        name='Опалення',  # id = 7   ЦЕНТРЕНЕРГО
        value='838.22',
        from_date=datetime.date(2024, 11, 30),
        to_date=None,
        tariff_type_id=3,
        provider_id=3,
        counter_id=None
    ),
    TariffAddDTO(
        name='Опалення',  # id = 7   ЦЕНТРЕНЕРГО
        value='1091.41',
        from_date=datetime.date(2024, 12, 30),
        to_date=None,
        tariff_type_id=3,
        provider_id=3,
        counter_id=None
    ),
    TariffAddDTO(
        name='Опалення',  # id = 7   ЦЕНТРЕНЕРГО
        value='718.91',
        from_date=datetime.date(2025, 1, 30),
        to_date=None,
        tariff_type_id=3,
        provider_id=3,
        counter_id=None
    ),
    TariffAddDTO(
        name='Опалення',  # id = 7   ЦЕНТРЕНЕРГО
        value='1137.32',
        from_date=datetime.date(2025, 2, 28),
        to_date=None,
        tariff_type_id=3,
        provider_id=3,
        counter_id=None
    ),
    TariffAddDTO(
        name='Опалення',  # id = 7   ЦЕНТРЕНЕРГО
        value='893.16',
        from_date=datetime.date(2025, 3, 31),
        to_date=None,
        tariff_type_id=3,
        provider_id=3,
        counter_id=None
    ),
    TariffAddDTO(
        name='Абонплата',  # id = 8   ЦЕНТРЕНЕРГО
        value='28.32',
        from_date=datetime.date(2024, 10, 1),
        to_date=None,
        tariff_type_id=1,
        provider_id=3,
        counter_id=None
    ),
    TariffAddDTO(
        name='Абонплата',  # id = 10   УВКП
        value='19.10',
        from_date=datetime.date(2024, 8, 1),
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
    TariffAddDTO(
        name='Доставка газу',  # transport gas
        value='14.01',
        from_date=datetime.date(2025, 1, 1),
        to_date=None,
        tariff_type_id=1,
        provider_id=5,
        counter_id=None
    ),
]

tariff_POZ = [

    TariffAddDTO(
        name='Абонплата',  # id = 15   ПОЖ
        value='447.58',
        from_date=datetime.date(2025, 4, 1),
        to_date=None,
        tariff_type_id=1,
        provider_id=7,
    ),
    TariffAddDTO(
        name='Абонплата',  # id = 15   ВИВІЗ СМІТТЯ
        value='14.46',
        from_date=datetime.date(2024, 12, 1),
        to_date=None,
        tariff_type_id=1,
        provider_id=6,
    ),
    TariffAddDTO(
        name='Плата за послуги',  # id = 15   ВИВІЗ СМІТТЯ
        value='293.34',
        from_date=datetime.date(2024, 12, 1),
        to_date=None,
        tariff_type_id=1,
        provider_id=6,
    ),
    TariffAddDTO(
        name='Інтернет',
        value='250.00',
        from_date=datetime.date(2025, 6, 1),
        to_date=None,
        tariff_type_id=1,
        provider_id=8,
    ),
]

counter_readings = [
    # electric
    CounterReadingAddDTO(value=3104, enter_date=datetime.date(2022, 9, 30), counter_id=1),
    CounterReadingAddDTO(value=3135, enter_date=datetime.date(2022, 10, 30), counter_id=1),
    CounterReadingAddDTO(value=3285, enter_date=datetime.date(2022, 11, 30), counter_id=1),
    CounterReadingAddDTO(value=3372, enter_date=datetime.date(2022, 12, 30), counter_id=1),
    CounterReadingAddDTO(value=3483, enter_date=datetime.date(2023, 1, 30), counter_id=1),
    CounterReadingAddDTO(value=3593, enter_date=datetime.date(2023, 2, 28), counter_id=1),
    CounterReadingAddDTO(value=3683, enter_date=datetime.date(2023, 3, 30), counter_id=1),
    CounterReadingAddDTO(value=3791, enter_date=datetime.date(2023, 4, 30), counter_id=1),
    CounterReadingAddDTO(value=3893, enter_date=datetime.date(2023, 5, 30), counter_id=1),
    CounterReadingAddDTO(value=4008, enter_date=datetime.date(2023, 6, 30), counter_id=1),
    CounterReadingAddDTO(value=4120, enter_date=datetime.date(2023, 7, 30), counter_id=1),
    CounterReadingAddDTO(value=4252, enter_date=datetime.date(2023, 8, 30), counter_id=1),
    CounterReadingAddDTO(value=4380, enter_date=datetime.date(2023, 9, 30), counter_id=1),
    CounterReadingAddDTO(value=4509, enter_date=datetime.date(2023, 10, 30), counter_id=1),
    CounterReadingAddDTO(value=4631, enter_date=datetime.date(2023, 11, 30), counter_id=1),
    CounterReadingAddDTO(value=4763, enter_date=datetime.date(2023, 12, 31), counter_id=1),
    CounterReadingAddDTO(value=4898, enter_date=datetime.date(2024, 1, 31), counter_id=1),
    CounterReadingAddDTO(value=5023, enter_date=datetime.date(2024, 2, 29), counter_id=1),
    CounterReadingAddDTO(value=5156, enter_date=datetime.date(2024, 3, 31), counter_id=1),
    CounterReadingAddDTO(value=5305, enter_date=datetime.date(2024, 4, 30), counter_id=1),
    CounterReadingAddDTO(value=5649, enter_date=datetime.date(2024, 5, 31), counter_id=1),
    CounterReadingAddDTO(value=5757, enter_date=datetime.date(2024, 6, 30), counter_id=1),
    CounterReadingAddDTO(value=5980, enter_date=datetime.date(2024, 7, 31), counter_id=1),
    CounterReadingAddDTO(value=6214, enter_date=datetime.date(2024, 8, 31), counter_id=1),
    CounterReadingAddDTO(value=6433, enter_date=datetime.date(2024, 9, 30), counter_id=1),
    CounterReadingAddDTO(value=6773, enter_date=datetime.date(2024, 10, 31), counter_id=1),
    CounterReadingAddDTO(value=6918, enter_date=datetime.date(2024, 11, 30), counter_id=1),
    CounterReadingAddDTO(value=7131, enter_date=datetime.date(2024, 12, 31), counter_id=1),
    CounterReadingAddDTO(value=7312, enter_date=datetime.date(2025, 1, 31), counter_id=1),
    CounterReadingAddDTO(value=7480, enter_date=datetime.date(2025, 2, 28), counter_id=1),
    CounterReadingAddDTO(value=7695, enter_date=datetime.date(2025, 3, 31), counter_id=1),
    # electric day tariff
    CounterReadingAddDTO(value=5883, enter_date=datetime.date(2025, 3, 31), counter_id=2),
    CounterReadingAddDTO(value=6135, enter_date=datetime.date(2025, 4, 30), counter_id=2),
    CounterReadingAddDTO(value=6334, enter_date=datetime.date(2025, 5, 30), counter_id=2),
    CounterReadingAddDTO(value=6526, enter_date=datetime.date(2025, 6, 30), counter_id=2),
    CounterReadingAddDTO(value=6662, enter_date=datetime.date(2025, 8, 1), counter_id=2),
    # electric night tariff
    CounterReadingAddDTO(value=1811, enter_date=datetime.date(2025, 3, 31), counter_id=3),
    CounterReadingAddDTO(value=1907, enter_date=datetime.date(2025, 4, 30), counter_id=3),
    CounterReadingAddDTO(value=1996, enter_date=datetime.date(2025, 5, 30), counter_id=3),
    CounterReadingAddDTO(value=2070, enter_date=datetime.date(2025, 6, 30), counter_id=3),
    CounterReadingAddDTO(value=2107, enter_date=datetime.date(2025, 8, 1), counter_id=3),
    # cold water
    CounterReadingAddDTO(value=1208, enter_date=datetime.date(2024, 7, 31), counter_id=6),
    CounterReadingAddDTO(value=1215, enter_date=datetime.date(2024, 8, 31), counter_id=6),
    CounterReadingAddDTO(value=1215, enter_date=datetime.date(2024, 9, 30), counter_id=6),
    CounterReadingAddDTO(value=1229, enter_date=datetime.date(2024, 10, 31), counter_id=6),
    CounterReadingAddDTO(value=1233, enter_date=datetime.date(2024, 11, 30), counter_id=6),
    CounterReadingAddDTO(value=1238, enter_date=datetime.date(2024, 12, 31), counter_id=6),
    CounterReadingAddDTO(value=1243, enter_date=datetime.date(2025, 1, 31), counter_id=6),
    CounterReadingAddDTO(value=1247, enter_date=datetime.date(2025, 2, 28), counter_id=6),
    CounterReadingAddDTO(value=1254, enter_date=datetime.date(2025, 3, 30), counter_id=6),
    CounterReadingAddDTO(value=1257, enter_date=datetime.date(2025, 4, 30), counter_id=6),
    CounterReadingAddDTO(value=1263, enter_date=datetime.date(2025, 5, 30), counter_id=6),
    CounterReadingAddDTO(value=1269, enter_date=datetime.date(2025, 6, 30), counter_id=6),
    CounterReadingAddDTO(value=1274, enter_date=datetime.date(2025, 8, 1), counter_id=6),
    CounterReadingAddDTO(value=1278, enter_date=datetime.date(2025, 8, 20), counter_id=6),
    # hot water
    CounterReadingAddDTO(value=584, enter_date=datetime.date(2024, 7, 31), counter_id=5),
    CounterReadingAddDTO(value=584, enter_date=datetime.date(2024, 8, 31), counter_id=5),
    CounterReadingAddDTO(value=584, enter_date=datetime.date(2024, 9, 30), counter_id=5),
    CounterReadingAddDTO(value=584, enter_date=datetime.date(2024, 10, 31), counter_id=5),
    CounterReadingAddDTO(value=586, enter_date=datetime.date(2024, 11, 30), counter_id=5),
    CounterReadingAddDTO(value=588, enter_date=datetime.date(2024, 12, 31), counter_id=5),
    CounterReadingAddDTO(value=590, enter_date=datetime.date(2025, 1, 31), counter_id=5),
    CounterReadingAddDTO(value=591, enter_date=datetime.date(2025, 2, 28), counter_id=5),
    CounterReadingAddDTO(value=591, enter_date=datetime.date(2025, 3, 30), counter_id=5),
    CounterReadingAddDTO(value=593, enter_date=datetime.date(2025, 4, 30), counter_id=5),
    CounterReadingAddDTO(value=594, enter_date=datetime.date(2025, 5, 30), counter_id=5),
    CounterReadingAddDTO(value=594, enter_date=datetime.date(2025, 6, 30), counter_id=5),
    CounterReadingAddDTO(value=596, enter_date=datetime.date(2025, 8, 1), counter_id=5),
    CounterReadingAddDTO(value=597, enter_date=datetime.date(2025, 8, 20), counter_id=5),
    # gas
    CounterReadingAddDTO(value=312, enter_date=datetime.date(2022, 11, 30), counter_id=4),
    CounterReadingAddDTO(value=323, enter_date=datetime.date(2022, 12, 30), counter_id=4),
    CounterReadingAddDTO(value=329, enter_date=datetime.date(2023, 1, 30), counter_id=4),
    CounterReadingAddDTO(value=336, enter_date=datetime.date(2023, 2, 28), counter_id=4),
    CounterReadingAddDTO(value=343, enter_date=datetime.date(2023, 3, 30), counter_id=4),
    CounterReadingAddDTO(value=352, enter_date=datetime.date(2023, 4, 30), counter_id=4),
    CounterReadingAddDTO(value=362, enter_date=datetime.date(2023, 5, 30), counter_id=4),
    CounterReadingAddDTO(value=374, enter_date=datetime.date(2023, 6, 30), counter_id=4),
    CounterReadingAddDTO(value=387, enter_date=datetime.date(2023, 7, 30), counter_id=4),
    CounterReadingAddDTO(value=397, enter_date=datetime.date(2023, 8, 30), counter_id=4),
    CounterReadingAddDTO(value=405, enter_date=datetime.date(2023, 9, 30), counter_id=4),
    CounterReadingAddDTO(value=414, enter_date=datetime.date(2023, 10, 30), counter_id=4),
    CounterReadingAddDTO(value=423, enter_date=datetime.date(2023, 11, 30), counter_id=4),
    CounterReadingAddDTO(value=431, enter_date=datetime.date(2023, 12, 31), counter_id=4),
    CounterReadingAddDTO(value=438, enter_date=datetime.date(2024, 1, 31), counter_id=4),
    CounterReadingAddDTO(value=446, enter_date=datetime.date(2024, 2, 29), counter_id=4),
    CounterReadingAddDTO(value=456, enter_date=datetime.date(2024, 3, 31), counter_id=4),
    CounterReadingAddDTO(value=466, enter_date=datetime.date(2024, 4, 30), counter_id=4),
    CounterReadingAddDTO(value=473, enter_date=datetime.date(2024, 5, 31), counter_id=4),
    CounterReadingAddDTO(value=408, enter_date=datetime.date(2024, 6, 30), counter_id=4),
    CounterReadingAddDTO(value=488, enter_date=datetime.date(2024, 7, 31), counter_id=4),
    CounterReadingAddDTO(value=498, enter_date=datetime.date(2024, 8, 31), counter_id=4),
    CounterReadingAddDTO(value=507, enter_date=datetime.date(2024, 9, 30), counter_id=4),
    CounterReadingAddDTO(value=516, enter_date=datetime.date(2024, 10, 31), counter_id=4),
    CounterReadingAddDTO(value=523, enter_date=datetime.date(2024, 11, 30), counter_id=4),
    CounterReadingAddDTO(value=530, enter_date=datetime.date(2024, 12, 31), counter_id=4),
    CounterReadingAddDTO(value=536, enter_date=datetime.date(2025, 1, 31), counter_id=4),
    CounterReadingAddDTO(value=541, enter_date=datetime.date(2025, 2, 28), counter_id=4),
    CounterReadingAddDTO(value=548, enter_date=datetime.date(2025, 3, 30), counter_id=4),
    CounterReadingAddDTO(value=554, enter_date=datetime.date(2025, 4, 30), counter_id=4),
    CounterReadingAddDTO(value=560, enter_date=datetime.date(2025, 5, 30), counter_id=4),
    CounterReadingAddDTO(value=567, enter_date=datetime.date(2025, 6, 30), counter_id=4),
    CounterReadingAddDTO(value=576, enter_date=datetime.date(2025, 8, 1), counter_id=4),
]

payments = [
    # electric
    PaymentAddDTO(value='260.64', date=datetime.date(2022, 12, 22), provider_id=1),
    PaymentAddDTO(value='285.12', date=datetime.date(2023, 2, 19), provider_id=1),
    PaymentAddDTO(value='350.00', date=datetime.date(2023, 3, 29), provider_id=1),
    PaymentAddDTO(value='93.52', date=datetime.date(2023, 5, 21), provider_id=1),
    PaymentAddDTO(value='312.48', date=datetime.date(2023, 7, 23), provider_id=1),
    PaymentAddDTO(value='782.16', date=datetime.date(2023, 9, 9), provider_id=1),
    PaymentAddDTO(value='337.92', date=datetime.date(2023, 9, 30), provider_id=1),
    PaymentAddDTO(value='662.64', date=datetime.date(2023, 12, 9), provider_id=1),
    PaymentAddDTO(value='348.48', date=datetime.date(2024, 1, 17), provider_id=1),
    PaymentAddDTO(value='356.40', date=datetime.date(2024, 2, 14), provider_id=1),
    PaymentAddDTO(value='330.00', date=datetime.date(2024, 3, 13), provider_id=1),
    PaymentAddDTO(value='351.12', date=datetime.date(2024, 4, 20), provider_id=1),
    PaymentAddDTO(value='1211.28', date=datetime.date(2024, 5, 31), provider_id=1),
    PaymentAddDTO(value='600.00', date=datetime.date(2024, 7, 4), provider_id=1),
    PaymentAddDTO(value='920.16', date=datetime.date(2024, 8, 12), provider_id=1),
    PaymentAddDTO(value='1510.88', date=datetime.date(2024, 9, 27), provider_id=1),
    PaymentAddDTO(value='1914.88', date=datetime.date(2024, 11, 14), provider_id=1),
    PaymentAddDTO(value='2328.48', date=datetime.date(2025, 2, 14), provider_id=1),
    PaymentAddDTO(value='114.19', date=datetime.date(2025, 3, 14), provider_id=1),
    PaymentAddDTO(value='1540.37', date=datetime.date(2025, 4, 29), provider_id=1),
    PaymentAddDTO(value='2347.92', date=datetime.date(2025, 6, 14), provider_id=1),
    # POZ
    
    PaymentAddDTO(value='1342.76', date=datetime.date(2025, 6, 27), provider_id=7),
    # GAS
    PaymentAddDTO(value='135.27', date=datetime.date(2023, 2, 19), provider_id=4),
    PaymentAddDTO(value='100.00', date=datetime.date(2023, 3, 29), provider_id=4),
    PaymentAddDTO(value='83.01', date=datetime.date(2023, 5, 21), provider_id=4),
    PaymentAddDTO(value='175.05', date=datetime.date(2023, 7, 23), provider_id=4),
    PaymentAddDTO(value='183.01', date=datetime.date(2023, 9, 9), provider_id=4),
    PaymentAddDTO(value='63.65', date=datetime.date(2023, 9, 30), provider_id=4),
    PaymentAddDTO(value='143.22', date=datetime.date(2023, 12, 9), provider_id=4),
    PaymentAddDTO(value='63.66', date=datetime.date(2024, 1, 17), provider_id=4),
    PaymentAddDTO(value='55.70', date=datetime.date(2024, 2, 14), provider_id=4),
    PaymentAddDTO(value='63.65', date=datetime.date(2024, 3, 13), provider_id=4),
    PaymentAddDTO(value='79.57', date=datetime.date(2024, 4, 20), provider_id=4),
    PaymentAddDTO(value='135.27', date=datetime.date(2024, 5, 31), provider_id=4),
    PaymentAddDTO(value='119.35', date=datetime.date(2024, 8, 12), provider_id=4),
    PaymentAddDTO(value='151.18', date=datetime.date(2024, 9, 27), provider_id=4),
    PaymentAddDTO(value='71.62', date=datetime.date(2024, 11, 13), provider_id=4),
    PaymentAddDTO(value='159.13', date=datetime.date(2025, 2, 15), provider_id=4),
    PaymentAddDTO(value='39.79', date=datetime.date(2025, 3, 14), provider_id=4),
    PaymentAddDTO(value='55.70', date=datetime.date(2025, 4, 29), provider_id=4),
    PaymentAddDTO(value='95.48', date=datetime.date(2025, 6, 16), provider_id=4),
    # RUBBISH
    PaymentAddDTO(value='615.60', date=datetime.date(2025, 1, 30), provider_id=6),
    PaymentAddDTO(value='152.27', date=datetime.date(2025, 4, 1), provider_id=6),
    PaymentAddDTO(value='463.33', date=datetime.date(2025, 4, 29), provider_id=6),
    PaymentAddDTO(value='923.40', date=datetime.date(2025, 6, 27), provider_id=6),
    # WATER
    PaymentAddDTO(value='1708.32', date=datetime.date(2024, 11, 14), provider_id=2),
    PaymentAddDTO(value='1469.66', date=datetime.date(2025, 2, 9), provider_id=2),
    PaymentAddDTO(value='347.56', date=datetime.date(2025, 4, 29), provider_id=2),
    PaymentAddDTO(value='2015.12', date=datetime.date(2025, 6, 27), provider_id=2),
    # heat
    PaymentAddDTO(value='51.76', date=datetime.date(2024, 8, 12), provider_id=3),
    PaymentAddDTO(value='168.77', date=datetime.date(2024, 11, 13), provider_id=3),
    PaymentAddDTO(value='1022.04', date=datetime.date(2024, 12, 16), provider_id=3),
    PaymentAddDTO(value='1948.52', date=datetime.date(2025, 2, 9), provider_id=3),
    PaymentAddDTO(value='2058.80', date=datetime.date(2025, 4, 29), provider_id=3),
    PaymentAddDTO(value='107.34', date=datetime.date(2025, 5, 10), provider_id=3),
    PaymentAddDTO(value='41.58', date=datetime.date(2025, 6, 16), provider_id=3),
    PaymentAddDTO(value='122.40', date=datetime.date(2025, 6, 27), provider_id=3),
    # transport gas
    PaymentAddDTO(value='28.02', date=datetime.date(2025, 2, 10), provider_id=5),
    PaymentAddDTO(value='14.01', date=datetime.date(2025, 3, 10), provider_id=5),
    PaymentAddDTO(value='14.01', date=datetime.date(2025, 4, 10), provider_id=5),
    PaymentAddDTO(value='28.02', date=datetime.date(2025, 6, 10), provider_id=5),
    # internet
    PaymentAddDTO(value='250.00', date=datetime.date(2025, 6, 30), provider_id=8),
    PaymentAddDTO(value='250.00', date=datetime.date(2025, 7, 29), provider_id=8),
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
    pymnt: str = 'payment'


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
    add_(tariff_POZ, Repositories.t)
    add_(counter_readings, Repositories.cr)
    add_(payments, Repositories.pymnt)


if __name__ == '__main__':
    add_(tariff_types, Repositories.tt)
