from datetime import date
from typing import Optional

from pydantic import BaseModel

from src.utilitiesaccounting_v4.schemas.counter_dto import CounterRelDTO
from src.utilitiesaccounting_v4.schemas.tariff_type_dto import TariffTypeDTO


class TariffAddDTO(BaseModel):
    name: str
    value: str
    from_date: date
    to_date: Optional[date] = None
    tariff_type_id: int
    provider_id: int
    counter_id: Optional[int] = None


class TariffDTO(TariffAddDTO):
    id: int


class TariffRelDTO(TariffDTO):
    tariff_type: 'TariffTypeDTO'
    counter: Optional['CounterRelDTO'] = None
