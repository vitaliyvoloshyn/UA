from typing import Optional, List

from pydantic import BaseModel

from src.utilitiesaccounting_v4.schemas.counter_reading_dto import CounterReadingDTO
from src.utilitiesaccounting_v4.schemas.measurement_unit_dto import MeasurementUnitDTO


class CounterAddDTO(BaseModel):
    name: str
    measurement_unit_id: int
    is_active: bool = True


class CounterDTO(CounterAddDTO):
    id: int


class CounterRelDTO(CounterDTO):
    measurement_unit: 'MeasurementUnitDTO'
    counter_readings: Optional[List['CounterReadingDTO']]
