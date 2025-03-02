from pydantic import BaseModel


class TariffTypeAddDTO(BaseModel):
    name: str


class TariffTypeDTO(TariffTypeAddDTO):
    id: int
