from datetime import date

from pydantic import BaseModel


class CounterReadingAddDTO(BaseModel):
    name: str
    value: int
    enter_date: date
    counter_id: int

class CounterReadingDTO(CounterReadingAddDTO):
    id: int
