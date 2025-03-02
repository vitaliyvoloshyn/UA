from pydantic import BaseModel


class CategoryAddDTO(BaseModel):
    name: str


class CategoryDTO(CategoryAddDTO):
    id: int


class CategoryRelDTO(CategoryDTO):
    provider: 'ProviderDTO'
