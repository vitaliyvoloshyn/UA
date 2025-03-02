"""Добавление тестовых данных в БД"""
import datetime
from typing import TypeVar

from pydantic import BaseModel

from src.utilitiesaccounting_v4.models import Base
from src.utilitiesaccounting_v4.services import MeasurementUnitService, BaseService, CategoryService, TariffTypeService, \
    ProviderService, CounterService, CounterReadingService, TariffService

"""Порядок добавления сущностей в БД
- единицы измерения;
- типы тарифов;
- счетчики;
- категория;
- оператор;
"""
from src.utilitiesaccounting_v4.schemas.category_dto import CategoryAddDTO
from src.utilitiesaccounting_v4.schemas.counter_dto import CounterAddDTO
from src.utilitiesaccounting_v4.schemas.counter_reading_dto import CounterReadingAddDTO
from src.utilitiesaccounting_v4.schemas.measurement_unit_dto import MeasurementUnitAddDTO
from src.utilitiesaccounting_v4.schemas.provider_dto import ProviderAddDTO
from src.utilitiesaccounting_v4.schemas.tariff_dto import TariffAddDTO
from src.utilitiesaccounting_v4.schemas.tariff_type_dto import TariffTypeAddDTO


T = TypeVar("T", bound=BaseService)
S = TypeVar("S", bound=Base)
B = TypeVar("B", bound=BaseModel)

measurement_unit_electric = MeasurementUnitAddDTO(value="кВт*год")
measurement_unit_volume = MeasurementUnitAddDTO(value="м3")

subscription = TariffTypeAddDTO(name='Щомісячне нарахування')
consumption_volume = TariffTypeAddDTO(name="За спожитий об'єм")
one_time_charge = TariffTypeAddDTO(name='Разове нарахування')

category_electric = CategoryAddDTO(name="Електропостачання")


class TestData:
    def __init__(self):
        self.measurement_unit_service = MeasurementUnitService()
        self.category_service = CategoryService()
        self.tariff_type_service = TariffTypeService()
        self.tariff_service = TariffService()
        self.provider_service = ProviderService()
        self.counter_service = CounterService()
        self.counter_reading_service = CounterReadingService()

        self.add_main_data()
        self.add_secondary_data()

    def add_main_data(self):
        self.measurement_unit_volume = self.add_record(service=self.measurement_unit_service,
                                                       repository='measurement_unit',
                                                       schema=measurement_unit_volume)
        self.measurement_unit_electric = self.add_record(service=self.measurement_unit_service,
                                                         repository='measurement_unit',
                                                         schema=measurement_unit_electric)
        self.tariff_type_subscription = self.add_record(service=self.tariff_type_service,
                                                        repository='tariff_type',
                                                        schema=subscription)
        self.tariff_type_consumption_volume = self.add_record(service=self.tariff_type_service,
                                                              repository='tariff_type',
                                                              schema=consumption_volume)
        self.tariff_type_one_time_charge = self.add_record(service=self.tariff_type_service,
                                                           repository='tariff_type',
                                                           schema=one_time_charge)
        self.category_electric = self.add_record(service=self.category_service,
                                                 repository='category',
                                                 schema=category_electric)

    def add_secondary_data(self):
        # Providers
        self.provider_electric_schema = ProviderAddDTO(name='ДТЕК',
                                                       category_id=self.get_id(service=self.category_service,
                                                                               repository='category',
                                                                               name='Електропостачання'))

        self.provider_electric = self.add_record(service=self.provider_service,
                                                 repository='provider',
                                                 schema=self.provider_electric_schema)

        # TARIFFS
        self.tariff_jan25_schema = TariffAddDTO(name='Однозонний тариф',
                                                value='4.32',
                                                from_date=datetime.date(2024, 11, 1),
                                                to_date=None,
                                                tariff_type_id=self.get_id(service=self.tariff_type_service,
                                                                           repository='tariff_type',
                                                                           name="За спожитий об'єм"),
                                                provider_id=self.get_id(service=self.provider_service,
                                                                       repository='provider',
                                                                       name="ДТЕК"))
        self.tariff_jan25_day_schema = TariffAddDTO(name='Денний тариф',
                                                value='4.32',
                                                from_date=datetime.date(2024, 11, 1),
                                                to_date=None,
                                                tariff_type_id=self.get_id(service=self.tariff_type_service,
                                                                           repository='tariff_type',
                                                                           name="За спожитий об'єм"),
                                                provider_id=self.get_id(service=self.provider_service,
                                                                        repository='provider',
                                                                        name="ДТЕК"))
        self.tariff_jan25_night_schema = TariffAddDTO(name='Нічний тариф',
                                                value='4.32',
                                                from_date=datetime.date(2024, 11, 1),
                                                to_date=None,
                                                tariff_type_id=self.get_id(service=self.tariff_type_service,
                                                                           repository='tariff_type',
                                                                           name="За спожитий об'єм"),
                                                provider_id=self.get_id(service=self.provider_service,
                                                                        repository='provider',
                                                                        name="ДТЕК")
                                                )
        self.add_record(service=self.tariff_service,
                        repository='tariff',
                        schema=self.tariff_jan25_schema)
        self.add_record(service=self.tariff_service,
                        repository='tariff',
                        schema=self.tariff_jan25_day_schema)
        self.add_record(service=self.tariff_service,
                        repository='tariff',
                        schema=self.tariff_jan25_night_schema)

        # COUNTERS
        self.counter_electric_schema = CounterAddDTO(name="Лічильник електроенергії",
                                                     measurement_unit_id=self.get_id(
                                                         service=self.measurement_unit_service,
                                                         repository='measurement_unit',
                                                         value="кВт*год"),
                                                     tariff_id=self.get_id(
                                                         service=self.tariff_service,
                                                         repository='tariff',
                                                         name='Однозонний тариф'))
        self.counter_electric_day_schema = CounterAddDTO(name="Лічильник електроенергії денний тариф",
                                                         measurement_unit_id=self.get_id(
                                                             service=self.measurement_unit_service,
                                                             repository='measurement_unit',
                                                             value="кВт*год"),
                                                         tariff_id=self.get_id(
                                                             service=self.tariff_service,
                                                             repository='tariff',
                                                             name='Денний тариф'))
        self.counter_electric_night_schema = CounterAddDTO(name="Лічильник електроенергії нічний тариф",
                                                           measurement_unit_id=self.get_id(
                                                               service=self.measurement_unit_service,
                                                               repository='measurement_unit',
                                                               value="кВт*год"),
                                                           tariff_id=self.get_id(
                                                               service=self.tariff_service,
                                                               repository='tariff',
                                                               name='Нічний тариф'))
        self.counter_electric = self.add_record(service=self.counter_service,
                                                repository='counter',
                                                schema=self.counter_electric_schema)
        self.counter_electric_day = self.add_record(service=self.counter_service,
                                                    repository='counter',
                                                    schema=self.counter_electric_day_schema)
        self.counter_electric_night = self.add_record(service=self.counter_service,
                                                      repository='counter',
                                                      schema=self.counter_electric_night_schema)

        # COUNTER READINGS
        self.counter_reading_jan25_schema = CounterReadingAddDTO(name="Споживання",
                                                                 value=7280,
                                                                 enter_date=datetime.date(2025, 2, 1),
                                                                 counter_id=self.get_id(service=self.counter_service,
                                                                                        repository='counter',
                                                                                        name="Лічильник електроенергії"))
        self.counter_reading_feb25_day_schema = CounterReadingAddDTO(name="Денний тариф",
                                                                     value=7300,
                                                                     enter_date=datetime.date(2025, 3, 1),
                                                                     counter_id=self.get_id(
                                                                         service=self.counter_service,
                                                                         repository='counter',
                                                                         name="Лічильник електроенергії денний тариф"))
        self.counter_reading_feb25_night_schema = CounterReadingAddDTO(name="Нічний тариф",
                                                                       value=7312,
                                                                       enter_date=datetime.date(2025, 3, 1),
                                                                       counter_id=self.get_id(
                                                                           service=self.counter_service,
                                                                           repository='counter',
                                                                           name="Лічильник електроенергії нічний тариф"))
        self.counter_reading_jan25 = self.add_record(service=self.counter_reading_service,
                                                     repository='counter_reading',
                                                     schema=self.counter_reading_jan25_schema)
        self.counter_reading_feb25_day = self.add_record(service=self.counter_reading_service,
                                                         repository='counter_reading',
                                                         schema=self.counter_reading_feb25_day_schema)
        self.counter_reading_feb25_night = self.add_record(service=self.counter_reading_service,
                                                           repository='counter_reading',
                                                           schema=self.counter_reading_feb25_night_schema)


    def add_record(self, service: T, repository: str, schema: B) -> S:
        with service.storage_manager() as sm:
            return sm.__getattribute__(repository).add(schema)

    def get_id(self, service: T, repository: str, **filter_) -> int:
        with service.storage_manager() as sm:
            data = sm.__getattribute__(repository).get(**filter_)
            return data[0].id
