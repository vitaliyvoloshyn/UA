from typing import List

from pydantic import BaseModel

from src.utilitiesaccounting.schemas.tariff_dto import TariffDTO, TariffRelDTO


class ProviderAddDTO(BaseModel):
    name: str
    category_id: int


class ProviderDTO(ProviderAddDTO):
    id: int


class ProviderRelDTO(ProviderDTO):
    tariffs: List['TariffRelDTO']
