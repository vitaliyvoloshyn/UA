from datetime import date

from pydantic import BaseModel

from src.utilitiesaccounting_v4.schemas.provider_dto import ProviderDTO


class PaymentAddDTO(BaseModel):
    value: str
    date: date
    provider_id: int


class PaymentDTO(PaymentAddDTO):
    id: int


class PaymentRelDTO(PaymentDTO):
    provider: 'ProviderDTO'
