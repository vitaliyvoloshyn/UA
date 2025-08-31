from datetime import date
from typing import Optional, Any, Self

import loguru
from fastapi import HTTPException
from pydantic import BaseModel, model_validator, ValidationError, field_validator

from src.utilitiesaccounting.models import Base
from src.utilitiesaccounting.schemas.counter_dto import CounterRelDTO
from src.utilitiesaccounting.schemas.tariff_type_dto import TariffTypeDTO


class TariffAddDTO(BaseModel):
    name: str
    value: str
    from_date: date
    to_date: Optional[date] = None
    tariff_type_id: int
    provider_id: int
    counter_id: Optional[int] = None

    @model_validator(mode='before')
    @classmethod
    def counter_validate(cls, data: Any) -> Any:
        """При tariff_type_id 2 має поле id лічильника не може бути порожнім (None)"""
        if not data:
            raise ValueError('Помилка валідаціі TarifAddDTO - пустий масив даних')
        if isinstance(data, Base):
            return data
        if int(data['tariff_type_id']) == 2:
            if not data.get('counter_id'):
                raise ValueError('Для обраного типу тарифа має бути вказаний лічильник')
        else:
            data['counter_id'] = None
        return data

    @field_validator('counter_id', mode='before')
    @classmethod
    def check_counter_id(cls, counter_id: Any):
        x = None
        try:
            x = int(counter_id)
        except TypeError:
            pass
        if x == 0:
            raise ValueError('ID ідентифікатор лічильника не може дорівнювати 0')
        return counter_id


class TariffDTO(TariffAddDTO):
    id: int


class TariffRelDTO(TariffDTO):
    tariff_type: 'TariffTypeDTO'
    counter: Optional['CounterRelDTO'] = None
