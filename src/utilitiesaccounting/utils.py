from datetime import date
from decimal import Decimal
from typing import List

from src.core.uow import StorageManager
from src.utilitiesaccounting.schemas.counter_reading_dto import CounterReadingAddDTO
from src.utilitiesaccounting.schemas.debt_dto import DebtDTO
from src.utilitiesaccounting.schemas.payment_dto import PaymentAddDTO
from src.utilitiesaccounting.schemas.tariff_dto import TariffDTO


def get_cr_last_position(counter_id: int):
    with StorageManager() as sm:
        return sm.counterrepository.get(relation=True, id=counter_id)


def validate_data(counter_id: int, value: int, date_: date) -> bool:
    """
    Валідує дані при внесені показників:
    - значення показників має бути більшою за попередні показники;
    - дата внесення показників має бути більшою за дату вненсення попередніх показників.
    :return: bool
    """
    mes = None
    counter = get_cr_last_position(counter_id)
    cr_last = counter[0].counter_readings[-1]
    if cr_last.value >= value:
        mes = f"""Помилка внесення показників по лічильнику {counter[0].name} - внесені показники {value} менші за попередні {cr_last.value}"""
    if cr_last.enter_date >= date_:
        mes = f"""Помилка внесення показників по лічильнику {counter[0].name} - дата внесених показників {date_} менша за дату внесення попередніх показників {cr_last.enter_date}"""
    if mes is None:
        return True
    raise ValueError(mes)


def validate_counter_readings(records: List[CounterReadingAddDTO]) -> bool:
    """
    Валідує дані при внесені показників:
    - значення показників має бути більшою за попередні показники;
    - дата внесення показників має бути більшою за дату вненсення попередніх показників.
    :return: bool
    """
    for rec in records:
        validate_data(rec.counter_id, rec.value, rec.enter_date)


def validate_payments(payments: List[PaymentAddDTO]) -> List[PaymentAddDTO]:
    """Валідує дані по оплаті
        - прибирає зі списку всі оплати, які менші або дорівнюють 0
    """
    block = Decimal('0')
    res_list = []
    for index, value in enumerate(payments):
        if Decimal(payments[index].value) > block:
            res_list.append(payments[index])
    if not res_list:
        raise ValueError('Перевірте внесені значення по оплаті')
    return res_list


def get_begin_current_month() -> date:
    return date(year=date.today().year,
                month=date.today().month,
                day=1)


def get_total_debt_value(debts: List[DebtDTO]):
    res = Decimal('0')
    for debt in debts:
        if float(debt.total_debt) > 0:
            res += Decimal(debt.total_debt)
    return res


def remove_inactive_tariffs(tariffs: List[TariffDTO]) -> List[TariffDTO]:
    """идаляє зі списку тарифів тільки ті тарифи, в яких кінцева дата не порожня"""
    tariffs_copy = []
    for tariff in tariffs:
        if tariff.to_date is None:
            tariffs_copy.append(tariff)
    return tariffs_copy


def remove_tariff_type_3_tariffs(tariffs: List[TariffDTO]) -> List[TariffDTO]:
    """Видаляє зі списку тарифів тільки ті тарифи, в яких tariff_type_id вказано 3 ('Разове нарахування')"""
    tariffs_copy = []
    for tariff in tariffs:
        if tariff.tariff_type_id != 3:
            tariffs_copy.append(tariff)
    return tariffs_copy
