from typing import Optional

from pydantic import BaseModel

from src.utilitiesaccounting_v4.schemas.provider_dto import ProviderRelDTO


class CategoryAddDTO(BaseModel):
    name: str
    photo: Optional[str] = None


class CategoryDTO(CategoryAddDTO):
    id: int


class CategoryRelDTO(CategoryDTO):
    provider: 'ProviderRelDTO'
