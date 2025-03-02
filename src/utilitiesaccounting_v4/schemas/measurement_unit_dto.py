from pydantic import BaseModel


class MeasurementUnitAddDTO(BaseModel):
    value: str


class MeasurementUnitDTO(MeasurementUnitAddDTO):
    id: int
