from abc import ABC, abstractmethod
from typing import TypeVar, Type, List, Sequence, Optional

import loguru
from pydantic import BaseModel
from sqlalchemy import select, update, delete, Row, and_, Select, text, TextClause, Column
from sqlalchemy.orm import Session

from src.utilitiesaccounting_v4.models import Base, Category, Provider, MeasurementUnit, Counter, CounterReading, \
    TariffType, Tariff, Payment
from src.utilitiesaccounting_v4.schemas.category_cr import CategoryCR
from src.utilitiesaccounting_v4.schemas.category_dto import CategoryDTO, CategoryAddDTO, CategoryRelDTO
from src.utilitiesaccounting_v4.schemas.counter_dto import CounterDTO, CounterAddDTO, CounterRelDTO
from src.utilitiesaccounting_v4.schemas.counter_reading_dto import CounterReadingDTO, CounterReadingAddDTO, \
    CounterReadingRelDTO
from src.utilitiesaccounting_v4.schemas.logger import logger
from src.utilitiesaccounting_v4.schemas.measurement_unit_dto import MeasurementUnitDTO, MeasurementUnitAddDTO
from src.utilitiesaccounting_v4.schemas.payment_dto import PaymentDTO, PaymentRelDTO, PaymentAddDTO
from src.utilitiesaccounting_v4.schemas.provider_dto import ProviderDTO, ProviderAddDTO, ProviderRelDTO
from src.utilitiesaccounting_v4.schemas.tariff_dto1 import TariffDTO, TariffRelDTO, TariffAddDTO
from src.utilitiesaccounting_v4.schemas.tariff_type_dto import TariffTypeDTO, TariffTypeAddDTO

SQLModel = TypeVar('SQLModel', bound=Base)
SchemaModel = TypeVar('SchemaModel', bound=BaseModel)


class RepositoryBase[Model](ABC):
    def __init__(self, session: Session):
        self.session = session

    @abstractmethod
    def add(self, record: SchemaModel):
        ...

    @abstractmethod
    def remove(self, pk: int):
        ...

    @abstractmethod
    def get(self):
        ...

    @abstractmethod
    def update(self, pk: int, **data):
        ...


class SqlRepository(RepositoryBase):
    model: Type[SQLModel]
    dto: Type[SchemaModel]
    dto_add: Type[SchemaModel]
    dto_rel: Type[SchemaModel]

    def __init__(self, session: Session):
        super().__init__(session)

    def add(self, record: SchemaModel) -> SQLModel:
        logger.debug(f'Запрос в БД -> добавление одной записи')
        sql = self._convert_schema_to_sql(record)
        self.session.add(sql)
        return sql

    def add_all(self, records: Sequence[SchemaModel]) -> Sequence[SQLModel]:
        logger.debug(f'Запрос в БД -> добавление нескольких записей')
        objects = map(self.add, records)
        return list(objects)

    def remove(self, pk: int):
        logger.debug(f'Запрос в БД -> удаление данных')
        stmt = delete(self.model).where(self.model.id == pk)
        self.session.execute(stmt)

    def get(self, relation: bool = False, convert: bool = True, query: Optional[Select | TextClause] = None,
            **filter_) -> List[SchemaModel] | Sequence[Row]:
        if query is None:
            query = select(self.model).filter_by(**filter_)
        sql_data = self.session.execute(query).scalars().all()
        logger.debug(f'Запрос в БД -> выборка данных')
        if not convert:
            return sql_data
        schemas = self._convert_sql_to_schema(sql_data, relation)
        return schemas

    def update(self, pk: int, **data):
        logger.debug(f'Запрос в БД -> обновление данных')
        stmt = update(self.model).where(self.model.id == pk).values(**data)
        self.session.execute(stmt)


    def _convert_schema_to_sql(self, schema: SchemaModel) -> SQLModel:
        """Конвертирует схему в SQL-модель"""
        sql = schema.model_dump()
        return self.model(**sql)

    def _convert_sql_to_schema(self, sql: Sequence[SQLModel], relation: bool = False) -> List[SchemaModel]:
        """Конвертирует SQL-модель в схему. Возвращает список схем"""
        dto: SchemaModel = self.dto
        if relation:
            dto = self.dto_rel
        schema = [dto.model_validate(sch, from_attributes=True) for sch in sql]
        return schema


class CategoryRepository(SqlRepository):
    model = Category
    dto = CategoryDTO
    dto_add = CategoryAddDTO
    dto_rel = CategoryRelDTO

    def get(self, relation: bool = False, convert: bool = True, query: Optional[Select | TextClause] = None,
            **filter_) -> List[SchemaModel] | Sequence[Row]:
        categories = super().get(relation, convert, **filter_)

        """Прибирає зі списку тарифи, в яких кінцева дата не порожня"""
        for category in categories:
            for tariff in category.provider.tariffs[::-1]:
                if tariff.to_date is not None:
                    category.provider.tariffs.remove(tariff)
        return categories

    def get_provider_id_by_category_name(self, category_name: str) -> int:
        category = super().get(relation=True, name=category_name)
        if category:
            return category[0].provider.id

    # def get_with_counters(self) -> List[SchemaModel] | Sequence[Row]:
    #     query = select(Category, CounterReading).join(Provider).join(Tariff).join(Counter).group_by(Category)
    #     categories = super().get(relation=True, convert=True, query=query)
    #     logger.debug(categories)
    #     return categories
    #
    #
    # def _convert_to_schema_category_cr(self, categories: List[SchemaModel] | Sequence[Row]):
    #     """В списку категорій залишає тільки показники поділені по категоріям"""
    #     res: List[CategoryCR]=[]
    #     cat: CategoryCR
    #     for category in categories:
    #         for tariff in category.provider.tariffs:
    #             c_name = category.name
    #             c_id = category.id
    #             t_c = tariff.counter
    #             cat=CategoryCR(name=c_name.name, id=c_id.id, counters=t_c)
    #             res.append(cat)
    #     return res

    def get_by_category_name_tariff_type(self, relation: bool = False, convert: bool = True,
                                         query: Optional[Select | TextClause] = None,
                                         **filter_) -> List[SchemaModel] | Sequence[Row]:

        query = (select(Category)
                 .join(Provider)
                 .join(Tariff)
                 .join(TariffType)
                 .filter(Category.name == filter_['name']))
        res = self.session.execute(query).scalars().all()
        res = self._convert_sql_to_schema(res, relation=True)
        return self._filter_by_tariff_type(res, filter_['tariff_type'])

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

    # def get(self, relation: bool = False, convert: bool = True, **filter_) -> List[SchemaModel] | Sequence[Row]:
    #     """С сортировкой по дате внесения показателей"""
    #     query = select(self.model).outerjoin(CounterReading).filter_by(**filter_).group_by(self.model.name)
    #     # query = select(text("* FROM counters c join counter_readings cr on c.id = cr.counter_id ORDER BY cr.enter_date;"))
    #
    #     return super().get(relation, convert, query)


class CounterReadingRepository(SqlRepository):
    model = CounterReading
    dto = CounterReadingDTO
    dto_add = CounterReadingAddDTO
    dto_rel = CounterReadingRelDTO

    def get(self, relation: bool = False, convert: bool = True, **filter_) -> List[SchemaModel] | Sequence[Row]:
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


class PaymentRepository(SqlRepository):
    model = Payment
    dto = PaymentDTO
    dto_add = PaymentAddDTO
    dto_rel = PaymentRelDTO
