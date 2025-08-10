from typing import Optional, List

from pydantic import BaseModel

from src.utilitiesaccounting_v4.schemas.counter_dto import CounterRelDTO


class CategoryCR(BaseModel):
    name: str
    id: int
    counters: Optional[List['CounterRelDTO']] = []
