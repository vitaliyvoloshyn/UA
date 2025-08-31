from datetime import timedelta
from typing import List, Sequence, Optional

from pydantic import BaseModel
from sqlalchemy import select, Row, and_, Select, TextClause

from src.core.repository.sqlalchemy_repository import SqlRepository
from src.core.uow import StorageManager
from src.utilitiesaccounting.models import Category, Provider, MeasurementUnit, Counter, CounterReading, \
    TariffType, Tariff, Payment
from src.utilitiesaccounting.schemas.category_dto import CategoryDTO, CategoryAddDTO, CategoryRelDTO
from src.utilitiesaccounting.schemas.counter_dto import CounterDTO, CounterAddDTO, CounterRelDTO
from src.utilitiesaccounting.schemas.counter_reading_dto import CounterReadingDTO, CounterReadingAddDTO, \
    CounterReadingRelDTO
from src.utilitiesaccounting.schemas.measurement_unit_dto import MeasurementUnitDTO, MeasurementUnitAddDTO
from src.utilitiesaccounting.schemas.payment_dto import PaymentDTO, PaymentRelDTO, PaymentAddDTO
from src.utilitiesaccounting.schemas.provider_dto import ProviderDTO, ProviderAddDTO, ProviderRelDTO
from src.utilitiesaccounting.schemas.tariff_dto1 import TariffDTO, TariffRelDTO, TariffAddDTO
from src.utilitiesaccounting.schemas.tariff_type_dto import TariffTypeDTO, TariffTypeAddDTO


class CategoryRepository(SqlRepository):
    model = Category
    dto = CategoryDTO
    dto_add = CategoryAddDTO
    dto_rel = CategoryRelDTO

    def get(self, relation: bool = False, convert: bool = True, query: Optional[Select | TextClause] = None,
            **filter_) -> List[BaseModel] | Sequence[Row]:
        categories = super().get(relation, convert, **filter_)

        """Прибирає зі списку тарифи, в яких кінцева дата не порожня"""
        try:
            for category in categories:
                for tariff in category.provider.tariffs[::-1]:
                    if tariff.to_date is not None:
                        category.provider.tariffs.remove(tariff)
        except AttributeError:
            pass
        return categories

    def get_provider_id_by_category_name(self, category_name: str) -> int:
        category = super().get(relation=True, name=category_name)
        if category:
            return category[0].provider.id

    def get_by_category_name_tariff_type(self, **filter_) -> List[BaseModel] | Sequence[Row]:

        query = (select(Category)
                 .join(Provider)
                 .join(Tariff)
                 .join(TariffType)
                 .filter(Category.name == filter_['name']))
        res = self.session.execute(query).scalars().all()
        res = self._convert_sql_to_schema(res, relation=True)
        return self._filter_by_tariff_type(res, filter_['tariff_type'])

    @staticmethod
    def _filter_by_tariff_type(self, data_list: List, tariff_type: int):
        for category in data_list:
            for tariff in category.provider:
                if tariff.tariff_type_id != tariff_type:
                    tariff.pop()
        return data_list


class ProviderRepository(SqlRepository):
    model = Provider
    dto = ProviderDTO
    dto_add = ProviderAddDTO
    dto_rel = ProviderRelDTO


class MeasurementUnitRepository(SqlRepository):
    model = MeasurementUnit
    dto = MeasurementUnitDTO
    dto_add = MeasurementUnitAddDTO


class CounterRepository(SqlRepository):
    model = Counter
    dto = CounterDTO
    dto_add = CounterAddDTO
    dto_rel = CounterRelDTO


class CounterReadingRepository(SqlRepository):
    model = CounterReading
    dto = CounterReadingDTO
    dto_add = CounterReadingAddDTO
    dto_rel = CounterReadingRelDTO

    def get(self, relation: bool = False, convert: bool = True, **filter_) -> List[BaseModel] | Sequence[Row]:
        """"""
        """ Группировка по счетчикам с сортировкой по дате внесения показателей """
        query = select(self.model).filter_by(**filter_).order_by(self.model.counter_id, self.model.enter_date.asc())
        query = select(CounterReading).filter_by(**filter_).order_by(CounterReading.counter_id,
                                                                     CounterReading.enter_date)
        return super().get(relation, convert, query)


class TariffTypeRepository(SqlRepository):
    model = TariffType
    dto = TariffTypeDTO
    dto_add = TariffTypeAddDTO


class TariffRepository(SqlRepository):
    model = Tariff
    dto = TariffDTO
    dto_add = TariffAddDTO
    dto_rel = TariffRelDTO

    def get_tariffs_by_category_tariff_type(self, category_name: int, tariff_type: int):
        query = (select(Tariff)
                 .join(Provider)
                 .join(Category)
                 .join(TariffType)
                 .where(and_(Category.name == category_name, TariffType.id == tariff_type))
                 .order_by(Tariff.from_date))
        res = self.session.execute(query).scalars().all()
        res = self._convert_sql_to_schema(res, relation=True)
        return res

    def get_tariffs_by_category_id(self, category_id: int):
        query = (select(self.model)
                 .join(Provider)
                 .join(Category)
                 .where(Category.id == category_id))
        res = self.session.execute(query).scalars().all()
        res = self._convert_sql_to_schema(res, relation=True)
        return res

    def change_tariff(self, new_tariff: TariffAddDTO, old_tariff_id: int):
        old_tariff = self.get(convert=False, id=old_tariff_id)
        if old_tariff:
            old_tariff = old_tariff[0]
        if old_tariff.to_date is not None:
            raise ValueError(f'Не можливо змінити тариф. Даний тариф ({old_tariff.name}) позначений як не активний')
        end_date_old_tariff = new_tariff.from_date - timedelta(days=1)
        old_tariff.to_date = end_date_old_tariff
        self.add(new_tariff)


class PaymentRepository(SqlRepository):
    model = Payment
    dto = PaymentDTO
    dto_add = PaymentAddDTO
    dto_rel = PaymentRelDTO


StorageManager.register_repository([
    TariffRepository,
    CounterRepository,
    CounterReadingRepository,
    TariffTypeRepository,
    ProviderRepository,
    CategoryRepository,
    MeasurementUnitRepository,
    PaymentRepository,
])
print(StorageManager.__dict__)
