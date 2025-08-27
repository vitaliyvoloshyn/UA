from datetime import date
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class Category(Base):
    __tablename__ = 'categories'
    # main fields
    name: Mapped[str] = mapped_column(unique=True)
    photo: Mapped[str] = mapped_column(nullable=True)
    # relationships
    provider: Mapped['Provider'] = relationship(back_populates='category', lazy='selectin')

    def __repr__(self):
        return f'{self.__class__.__name__}: (name={self.name})'


class MeasurementUnit(Base):
    __tablename__ = 'measurement_units'
    # main fields
    value: Mapped[str] = mapped_column(unique=True)
    # relationships
    counters: Mapped[List['Counter']] = relationship(back_populates='measurement_unit', lazy='selectin')


class CounterReading(Base):
    __tablename__ = 'counter_readings'
    # main fields
    value: Mapped[int]
    enter_date: Mapped[date]
    counter_id: Mapped[int] = mapped_column(ForeignKey('counters.id'))
    # relationships
    counter: Mapped['Counter'] = relationship(back_populates='counter_readings', lazy='selectin')


class Counter(Base):
    __tablename__ = 'counters'
    # main fields
    name: Mapped[str] = mapped_column(unique=True)
    is_active: Mapped[bool]
    measurement_unit_id: Mapped[int] = mapped_column(ForeignKey('measurement_units.id'), nullable=True)
    # relationships
    measurement_unit: Mapped['MeasurementUnit'] = relationship(back_populates='counters', lazy='selectin')
    counter_readings: Mapped[List['CounterReading']] = relationship(back_populates='counter', lazy='selectin')
    tariffs: Mapped[List['Tariff']] = relationship(back_populates='counter', lazy='selectin')


class Provider(Base):
    __tablename__ = 'providers'
    # main fields
    name: Mapped[str] = mapped_column(unique=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    # relationships
    category: Mapped['Category'] = relationship(back_populates='provider', lazy='selectin')
    tariffs: Mapped[List['Tariff']] = relationship(back_populates='provider', lazy='selectin')
    payments: Mapped[List['Payment']] = relationship(back_populates='provider', lazy='selectin')


class TariffType(Base):
    __tablename__ = 'tariff_types'
    # main fields
    name: Mapped[str] = mapped_column(unique=True)
    # relationships
    tariffs: Mapped[list['Tariff']] = relationship(back_populates='tariff_type', lazy='selectin')


class Tariff(Base):
    __tablename__ = 'tariffs'
    # main fields
    name: Mapped[str]
    value: Mapped[str]
    from_date: Mapped[date]
    to_date: Mapped[date] = mapped_column(nullable=True)
    tariff_type_id: Mapped[int] = mapped_column(ForeignKey('tariff_types.id'))
    provider_id: Mapped[int] = mapped_column(ForeignKey('providers.id'))
    counter_id: Mapped[int] = mapped_column(ForeignKey('counters.id'), nullable=True)
    # relationships
    tariff_type: Mapped['TariffType'] = relationship(back_populates='tariffs')
    counter: Mapped['Counter'] = relationship(back_populates='tariffs', lazy='selectin')
    provider: Mapped['Provider'] = relationship(back_populates='tariffs')


class Payment(Base):
    __tablename__='payments'
    # main fields
    value: Mapped[str]
    date: Mapped[date]
    provider_id: Mapped[int] = mapped_column(ForeignKey('providers.id'))
    # relationships
    provider: Mapped['Provider'] = relationship(back_populates='payments')

