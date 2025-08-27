from decimal import Decimal
from typing import List, Union, Optional

from pydantic import BaseModel, ConfigDict

from src.utilitiesaccounting_v4.schemas.tariff_dto import TariffRelDTO


class DebtDTO(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    header: str = 'debt'
    category_name: str
    category_photo: Optional[str] = None
    provider_id: int
    total_accrued: str
    total_payment: str
    total_debt: str
    debt: List[Union['ConsumptionTariffs', 'SubscriptionTariffs', 'OnTimeTariffs']]
    # debt: List['TariffRelDTO']


class TypeTariff(BaseModel):
    header: str = 'tariff_type'
    value: str
    debt_value: str
    tariff_type_name: str
    is_active: bool

    def __add__(self, other) -> str:
        if isinstance(other, (Decimal, str)):
            res = str(Decimal(self.value) + Decimal(other))
        else:
            res = str(Decimal(self.value) + Decimal(other.value))
        return str(res)


class SubscriptionTariffs(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    tariffs: List['SubscriptionTariff']


class SubscriptionTariff(TypeTariff):
    tariff_type: str = 'Щомісячне нарахування'
    tariff_type_name: str


class ConsumptionTariffs(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    tariffs: List['ConsumptionTariff']


class ConsumptionTariff(TypeTariff):
    tariff_type: str = "За спожитий об'єм"
    tariff_type_name: str
    cur_readings: Optional[int] = None
    prev_readings: Optional[int] = None
    diff: Optional[int] = None


class OnTimeTariffs(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    tariffs: List['OnTimeTariff']


class OnTimeTariff(TypeTariff):
    tariff_type: str = 'Одноразове нарахування'
    tariff_type_name: str
