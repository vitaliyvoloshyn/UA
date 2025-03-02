from typing import List, Optional

from pydantic import BaseModel

from src.utilitiesaccounting_v3.schemas.category_dto import CategoryDTO
from src.utilitiesaccounting_v3.schemas.counter_dto import CounterDTO


class ProviderAddDTO(BaseModel):
    name: str
    category_id: int


class ProviderDTO(ProviderAddDTO):
    id: int


class ProviderRelDTO(ProviderDTO):
    category: 'CategoryDTO'
    counters: Optional[List['CounterDTO']] = None
