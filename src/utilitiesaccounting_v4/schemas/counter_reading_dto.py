from datetime import date
from typing import Optional

from pydantic import BaseModel


class CounterReadingAddDTO(BaseModel):
    name: str
    value: Optional[int] = ''
    enter_date: date
    counter_id: int


class CounterReadingDTO(CounterReadingAddDTO):
    id: int


class CounterReadingRelDTO(CounterReadingDTO):
    ...
