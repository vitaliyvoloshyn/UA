from pydantic import BaseModel

from src.utilitiesaccounting_v4.schemas.provider_dto import ProviderDTO


class CategoryAddDTO(BaseModel):
    name: str


class CategoryDTO(CategoryAddDTO):
    id: int


class CategoryRelDTO(CategoryDTO):
    provider: 'ProviderDTO'
