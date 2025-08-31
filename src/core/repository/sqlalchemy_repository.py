from typing import Type, Sequence

from loguru import logger
from pydantic import BaseModel
from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session

from .base_repository import RepositoryBase


class SqlRepository(RepositoryBase):
    model = None
    dto = None
    dto_add = None
    dto_rel = None

    def __init__(self, session: Session):
        super().__init__(session)

    def add(self, record: BaseModel):
        logger.debug(f'Запрос в БД -> добавление одной записи')
        sql = self._convert_schema_to_sql(record)
        self.session.add(sql)
        return sql

    def add_all(self, records: Sequence[BaseModel]):
        logger.debug(f'Запрос в БД -> добавление нескольких записей')
        objects = map(self.add, records)
        return list(objects)

    def remove(self, pk: int):
        logger.debug(f'Запрос в БД -> удаление данных')
        stmt = delete(self.model).where(self.model.id == pk)
        self.session.execute(stmt)

    def get(self, relation: bool = False, convert: bool = True, query = None,
            **filter_):
        if query is None:
            query = select(self.model).filter_by(**filter_)
        sql_data = self.session.execute(query).scalars().all()
        logger.debug(f'Запрос в БД -> выборка данных')
        if not convert:
            return sql_data
        schemas = self._convert_sql_to_schema(sql_data, relation)
        return schemas

    def get_by_id(self, id: int, relation: bool = False, convert: bool = True):
        query = select(self.model).where(id=id)
        res = self.get(relation, convert, query)
        if res:
            return res[0]

    def update(self, pk: int, **data):
        logger.debug(f'Запрос в БД -> обновление данных')
        stmt = update(self.model).where(self.model.id == pk).values(**data)
        self.session.execute(stmt)

    def _convert_schema_to_sql(self, schema):
        """Конвертирует схему в SQL-модель"""
        sql = schema.model_dump()
        return self.model(**sql)

    def _convert_sql_to_schema(self, sql, relation: bool = False):
        """Конвертирует SQL-модель в схему. Возвращает список схем"""
        dto: SchemaModel = self.dto
        if relation:
            dto = self.dto_rel
        schema = [dto.model_validate(sch, from_attributes=True) for sch in sql]
        return schema
