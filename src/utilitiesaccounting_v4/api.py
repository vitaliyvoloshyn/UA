from typing import List

import loguru
from fastapi import APIRouter
from starlette.responses import JSONResponse

from src.utilitiesaccounting_v4.schemas.counter_reading_dto import CounterReadingAddDTO, CounterReadingDTO
from src.utilitiesaccounting_v4.schemas.payment_dto import PaymentAddDTO, PaymentDTO
from src.utilitiesaccounting_v4.schemas.tariff_dto import TariffDTO, TariffAddDTO
from src.utilitiesaccounting_v4.uow import UnitOfWork
from src.utilitiesaccounting_v4.utils import validate_counter_readings, validate_payments

api_router = APIRouter(
    prefix='/api',
    tags=['API']
)


@api_router.post('/add_counterreading', name='add_counterreading')
def add_counter_reading(records: List[CounterReadingAddDTO]):
    """Пост-запрос на добавление показателей счетчиков"""
    try:
        validate_counter_readings(records)
    except ValueError as e:
        return JSONResponse(content=str(e),
                            status_code=400)
    with UnitOfWork() as uow:
        uow.counter_reading.add_all(records)
    loguru.logger.info(f"Added new counter readings")
    return JSONResponse(content='OK', status_code=200)


@api_router.get('/counter_readings', name='crs')
def get_crs() -> List[CounterReadingDTO]:
    with UnitOfWork() as uow:
        crs = uow.counter_reading.get()
    return crs


@api_router.get('/counter_readings/{pk}', name='cr')
def get_cr_by_id(pk: int) -> CounterReadingDTO:
    with UnitOfWork() as uow:
        cr = uow.counter_reading.get(id=pk)
    return cr


@api_router.put('/counter_readings/{pk}', name='cr_put')
def put_cr_by_id(pk: int, data: CounterReadingDTO):
    with UnitOfWork() as uow:
        uow.counter_reading.update(pk=pk, **data.model_dump())
    return JSONResponse(content='OK', status_code=200)


@api_router.delete('/counter_readings/{pk}', name='cr_del')
def del_cr_by_id(pk: int):
    with UnitOfWork() as uow:
        uow.counter_reading.remove(pk)
    return JSONResponse(content='OK', status_code=200)


@api_router.post('/payments', name='add_payments')
def form_add_payments(data: List[PaymentAddDTO]):
    """POST REQUEST ВНЕСЕНИЯ ОПЛАТЫ"""
    loguru.logger.debug(data)
    try:
        data = validate_payments(data)
    except ValueError as e:
        return JSONResponse(content=str(e),
                            status_code=400)
    with UnitOfWork() as uow:
        uow.payment.add_all(data)
    return JSONResponse(content='OK', status_code=200)


@api_router.get('/payments')
def get_payments() -> List[PaymentDTO]:
    with UnitOfWork() as uow:
        payments = uow.payment.get()
    return payments


@api_router.get('/payments/{item_id}')
def get_payment(item_id: int) -> List[PaymentDTO]:
    with UnitOfWork() as uow:
        payments = uow.payment.get(id=item_id)
    return payments


@api_router.put('/payments/{item_id}')
def put_payment(item_id: int, pymnt: PaymentAddDTO):
    data = pymnt.model_dump()
    with UnitOfWork() as uow:
        uow.payment.update(item_id,
                           **data,
                           )
    return JSONResponse(content='OK', status_code=200)


@api_router.delete('/payments/{pk}', name='pymnt_del')
def del_pymnt_by_id(pk: int):
    with UnitOfWork() as uow:
        uow.payment.remove(pk)
    return JSONResponse(content='OK', status_code=200)


@api_router.get('/tariffs', name='tariffs')
def get_tariffs() -> List[TariffDTO]:
    with UnitOfWork() as uow:
        tariffs = uow.tariff.get()
    return tariffs


@api_router.get('/tariffs/{item_id}', name='tariff')
def get_tariff_by_id(item_id: int) -> TariffDTO:
    with UnitOfWork() as uow:
        tariff = uow.tariff.get(id=item_id)
        if not tariff:
            return JSONResponse(content="Resource does not exist")
    return tariff[0]


@api_router.delete('/tariffs/{item_id}', name='tariff_del')
def del_tariff_by_id(item_id: int):
    with UnitOfWork() as uow:
        uow.tariff.remove(pk=item_id)
    return JSONResponse(content='OK', status_code=200)


@api_router.put('/tariffs/{item_id}', name='tariff_update')
def update_tariff_by_id(item_id: int, data: TariffAddDTO):
    with UnitOfWork() as uow:
        uow.tariff.update(pk=item_id, **data.model_dump())
    return JSONResponse(content='OK', status_code=200)


@api_router.post('/tariffs/', name='tariff_add')
def add_tariff_by_id(data: TariffAddDTO):
    with UnitOfWork() as uow:
        uow.tariff.add(data)
    return JSONResponse(content='OK', status_code=200)
