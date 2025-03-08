from typing import List

from pydantic import BaseModel

from src.utilitiesaccounting_v4.schemas.tariff_dto import TariffDTO


class ProviderAddDTO(BaseModel):
    name: str
    category_id: int


class ProviderDTO(ProviderAddDTO):
    id: int


class ProviderRelDTO(ProviderDTO):
    tariffs: List['TariffDTO']
