from datetime import date
from decimal import Decimal
from typing import List

from loguru import logger

from src.utilitiesaccounting_v4.schemas.counter_reading_dto import CounterReadingAddDTO
from src.utilitiesaccounting_v4.schemas.payment_dto import PaymentAddDTO
from src.utilitiesaccounting_v4.uow import UnitOfWork


def get_cr_last_position(counter_id: int):
    with UnitOfWork() as uow:
        return uow.counter.get(relation=True, id=counter_id)


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
    logger.error(mes)
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



