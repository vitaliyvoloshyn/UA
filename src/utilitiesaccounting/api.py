from typing import List

import loguru
from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from src.auth.service import check_user_permissions_api
from src.utilitiesaccounting.schemas.counter_reading_dto import CounterReadingAddDTO, CounterReadingDTO
from src.utilitiesaccounting.schemas.payment_dto import PaymentAddDTO, PaymentDTO
from src.utilitiesaccounting.schemas.result_content import SuccessResultContent, ErrorResultContent
from src.utilitiesaccounting.schemas.tariff_dto import TariffDTO, TariffAddDTO
from src.utilitiesaccounting.utils import validate_counter_readings, validate_payments
from src.core.uow import StorageManager

api_router = APIRouter(
    prefix='/api',
    tags=['API'],
    dependencies=[Depends(check_user_permissions_api)]
)


@api_router.post('/add_counterreading', name='add_counterreading')
def add_counter_reading(records: List[CounterReadingAddDTO]):
    """Пост-запрос на добавление показателей счетчиков"""
    attrs = {
        'header': 'Внесення нових показників',
        'back_ref': 'addcounterreadings',
        'back_ref_text': 'Повернутися на сторінку внесення показників',
    }
    try:
        validate_counter_readings(records)
    except ValueError as e:
        attrs['message_operation'] = str(e)
        res_cont = ErrorResultContent(**attrs)
        loguru.logger.error(f"Add new counter readings - {e}")
        return JSONResponse(content=res_cont.model_dump(),
                            status_code=400)
    with StorageManager() as sm:
        sm.counterreadingrepository.add_all(records)
        attrs['message_operation'] = 'Нові показники успішно збережені'
        res_cont = SuccessResultContent(**attrs)
    loguru.logger.info(f"Added new counter readings")
    return JSONResponse(content=res_cont.model_dump(), status_code=200)


@api_router.get('/counter_readings', name='crs')
def get_crs() -> List[CounterReadingDTO]:
    with StorageManager() as sm:
        crs = sm.counterreadingrepository.get()
    return crs


@api_router.get('/counter_readings/{pk}', name='cr')
def get_cr_by_id(pk: int) -> CounterReadingDTO:
    with StorageManager() as sm:
        cr = sm.counterreadingrepository.get_by_id(id=pk)
    return cr


@api_router.put('/counter_readings/{pk}', name='cr_put')
def put_cr_by_id(pk: int, data: CounterReadingDTO):
    with StorageManager() as sm:
        sm.counterreadingrepository.update(pk=pk, **data.model_dump())
    return JSONResponse(content='OK', status_code=200)


@api_router.delete('/counter_readings/{pk}', name='cr_del')
def del_cr_by_id(pk: int):
    with StorageManager() as sm:
        sm.counterreadingrepository.remove(pk)
    return JSONResponse(content='OK', status_code=200)


@api_router.post('/payments', name='add_payments')
def form_add_payments(data: List[PaymentAddDTO]):
    """POST REQUEST ВНЕСЕНИЯ ОПЛАТЫ"""
    attrs = {
        'header': 'Сплата рахунків',
        'back_ref': 'payments',
        'back_ref_text': 'Повернутися на сторінку сплати рахунків',
    }

    try:
        data = validate_payments(data)
    except ValueError as e:
        attrs['message_operation'] = str(e)
        res_cont = ErrorResultContent(**attrs)
        return JSONResponse(content=res_cont.model_dump(),
                            status_code=400)
    with StorageManager() as sm:
        sm.paymentrepository.add_all(data)
        attrs['message_operation'] = 'Рахунки успішно сплачені'
        res_cont = SuccessResultContent(**attrs)
    return JSONResponse(content=res_cont.model_dump(), status_code=200)


@api_router.get('/payments')
def get_payments() -> List[PaymentDTO]:
    with StorageManager() as sm:
        payments = sm.paymentrepository.get()
    return payments


@api_router.get('/payments/{item_id}')
def get_payment(item_id: int) -> List[PaymentDTO]:
    with StorageManager() as sm:
        payments = sm.paymentrepository.get(id=item_id)
    return payments


@api_router.put('/payments/{item_id}')
def put_payment(item_id: int, pymnt: PaymentAddDTO):
    data = pymnt.model_dump()
    with StorageManager() as sm:
        sm.paymentrepository.update(item_id,
                           **data,
                           )
    return JSONResponse(content='OK', status_code=200)


@api_router.delete('/payments/{pk}', name='pymnt_del')
def del_pymnt_by_id(pk: int):
    with StorageManager() as sm:
        sm.paymentrepository.remove(pk)
    return JSONResponse(content='OK', status_code=200)


@api_router.get('/tariffs', name='tariffs')
def get_tariffs() -> List[TariffDTO]:
    with StorageManager() as sm:
        tariffs = sm.tariffrepository.get()
    return tariffs


@api_router.get('/tariffs/{item_id}', name='tariff')
def get_tariff_by_id(item_id: int):
    with StorageManager() as sm:
        tariff = sm.tariffrepository.get(id=item_id)
        if not tariff:
            return JSONResponse(content="Resource does not exist")
    return tariff[0]


@api_router.delete('/tariffs/{item_id}', name='tariff_del')
def del_tariff_by_id(item_id: int):
    with StorageManager() as sm:
        sm.tariffrepository.remove(pk=item_id)
    return JSONResponse(content='OK', status_code=200)


@api_router.put('/tariffs/{item_id}', name='tariff_update')
def update_tariff_by_id(item_id: int, data: TariffAddDTO):
    with StorageManager() as sm:
        sm.tariffrepository.update(pk=item_id, **data.model_dump())
    return JSONResponse(content='OK', status_code=200)


@api_router.post('/tariffs/', name='tariff_add')
def add_tariff_by_id(data: TariffAddDTO):
    attrs = {
        'header': 'Зміна тарифу',
        'back_ref': 'tariffs',
        'back_ref_text': 'Повернутися на сторінку перегляду тарифів',
    }
    try:
        with StorageManager() as sm:
            sm.tariffrepository.add(data)
    except Exception as e:
        loguru.logger.error(e)
        attrs['message_operation'] = str(e)
        res_cont = ErrorResultContent(**attrs)
        return JSONResponse(content=res_cont.model_dump(),
                            status_code=400)
    loguru.logger.info(f'Request for add tariff {data.name}')
    attrs['message_operation'] = 'Тариф успішно доданий'
    res_cont = SuccessResultContent(**attrs)

    return JSONResponse(content=res_cont.model_dump(), status_code=200)


@api_router.post('/tariffs/{tariff_id}', name='tariff_change')
def change_tariff(new_tariff: TariffAddDTO, tariff_id: int):
    """Пост-запит на зміну тарифа"""
    attrs = {
        'header': 'Зміна тарифу',
        'back_ref': 'tariffs',
        'back_ref_text': 'Повернутися на сторінку перегляду тарифів',
    }

    with StorageManager() as sm:
        try:
            sm.tariffrepository.change_tariff(new_tariff, tariff_id)
        except Exception as e:
            loguru.logger.error(e)
            attrs['message_operation'] = str(e)
            res_cont = ErrorResultContent(**attrs)
            return JSONResponse(content=res_cont.model_dump(),
                                status_code=400)
    loguru.logger.info(f'Request for change tariff id = {tariff_id}')
    attrs['message_operation'] = 'Тариф успішно змінений'
    res_cont = SuccessResultContent(**attrs)

    return JSONResponse(content=res_cont.model_dump(), status_code=200)
