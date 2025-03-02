from abc import ABC, abstractmethod
from typing import TypeVar, Type, List, Sequence

from pydantic import BaseModel
from sqlalchemy import select, update, delete, Row
from sqlalchemy.orm import Session

from src.utilitiesaccounting_v3.models import Base, Category, Provider, MeasurementUnit, Counter, CounterReading, \
    TariffType, Tariff
from src.utilitiesaccounting_v3.schemas.category_dto import CategoryDTO, CategoryAddDTO, CategoryRelDTO
from src.utilitiesaccounting_v3.schemas.counter_dto import CounterDTO, CounterAddDTO, CounterRelDTO
from src.utilitiesaccounting_v3.schemas.counter_reading_dto import CounterReadingDTO, CounterReadingAddDTO
from src.utilitiesaccounting_v3.schemas.measurement_unit_dto import MeasurementUnitDTO, MeasurementUnitAddDTO
from src.utilitiesaccounting_v3.schemas.provider_dto import ProviderDTO, ProviderAddDTO, ProviderRelDTO
from src.utilitiesaccounting_v3.schemas.tariff_dto import TariffRelDTO, TariffAddDTO, TariffDTO
from src.utilitiesaccounting_v3.schemas.tariff_type_dto import TariffTypeDTO, TariffTypeAddDTO

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
        sql = self._convert_schema_to_sql(record)
        self.session.add(sql)
        return sql

    def remove(self, pk: int):

        stmt = delete(self.model).where(self.model.id == pk)
        self.session.execute(stmt)

    def get(self, relation: bool = False, convert: bool = True, **filter_) -> List[SchemaModel] | Sequence[Row]:
        query = select(self.model).filter_by(**filter_)
        sql_data = self.session.execute(query).scalars().all()
        if not convert:
            return sql_data
        schemas = self._convert_sql_to_schema(sql_data, relation)
        return schemas

    def update(self, pk: int, **data) -> Sequence[Row]:
        stmt = update(self.model).where(self.model.id == pk).values(**data).returning(self.model)
        res = self.session.execute(stmt).scalars().all()
        return res

    def _convert_schema_to_sql(self, schema: SchemaModel) -> SQLModel:
        """Конвертирует схему в SQL-модель"""
        sql = schema.model_dump()
        return self.model(**sql)

    def _convert_sql_to_schema(self, sql: Sequence[Row], relation: bool = False) -> List[SchemaModel]:
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


class TariffTypeRepository(SqlRepository):
    model = TariffType
    dto = TariffTypeDTO
    dto_add = TariffTypeAddDTO


class TariffRepository(SqlRepository):
    model = Tariff
    dto = TariffDTO
    dto_add = TariffAddDTO
    dto_rel = TariffRelDTO
