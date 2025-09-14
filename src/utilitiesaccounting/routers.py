import json
from typing import Annotated

from fastapi import APIRouter, Query, Depends
from starlette.requests import Request
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from src.auth.service import check_user_permissions
from src.core.uow import StorageManager
from src.core.logging import logger
from src.utilitiesaccounting.services import electric_service
from src.utilitiesaccounting.utils import get_total_debt_value, remove_tariff_type_3_tariffs, remove_inactive_tariffs

main_router = APIRouter()
templates = Jinja2Templates(directory="templates")


@main_router.get('/', response_class=HTMLResponse, name='home')
def index(request: Request, user=Depends(check_user_permissions)):
    """MAIN PAGE"""
    logger.info(f'GET-запит на головну сторінку host={request.client.host}')
    debt = electric_service.calc_all_services()
    total_debt = get_total_debt_value(debt)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            'debt': debt,
            'total_debt': total_debt,
            'user': user,
        },
    )


# @main_router.get('/erroraddcounterreadings', response_class=HTMLResponse, name='error_add_cr')
# def error_add_cr(request: Request, message: str):
#     """СТРАНИЦА ОШИБКИ ПРИ ВНЕСЕНИИ ПОКАЗАНИЙ СЧЕТЧИКОВ"""
#     return templates.TemplateResponse(
#         request=request,
#         name='error_add_counter_readings.html',
#         context={'message': message},
#     )


# @main_router.get('/successaddcounterreadings', response_class=HTMLResponse, name='success_add_cr')
# def success_add_cr(request: Request):
#     """СТРАНИЦА УДАЧНОГО ВНЕСЕНИЯ ПОКАЗАНИЙ СЧЕТЧИКОВ"""
#     return templates.TemplateResponse(
#         request=request,
#         name='success_add_counter_readings.html',
#     )
#

@main_router.get('/addcounterreadings', response_class=HTMLResponse, name='addcounterreadings')
def form_add_counter_readings(request: Request, user=Depends(check_user_permissions)):
    """СТРАНИЦА ВНЕСЕНИЯ ПОКАЗАНИЙ СЧЕТЧИКОВ"""
    with StorageManager() as uow:
        counters = uow.counterrepository.get(relation=True)
    return templates.TemplateResponse(
        request=request,
        name='formelement.html',
        context={'counters': counters,
                 'user': user}
    )


@main_router.get('/add_payment', response_class=HTMLResponse, name='payments')
def form_add_payments(request: Request, user=Depends(check_user_permissions)):
    """СТРАНИЦА ВНЕСЕНИЯ ОПЛАТЫ"""
    context = electric_service.calc_all_services()
    return templates.TemplateResponse(
        request=request,
        name='add_payment.html',
        context={'categories': context,
                 'user': user},
    )


# @main_router.get('/erroraddpayments', response_class=HTMLResponse, name='error_add_pymnt')
# def error_add_pymnt(request: Request, message: str):
#     """СТРАНИЦА ОШИБКИ ПРИ ВНЕСЕНИИ ПОКАЗАНИЙ СЧЕТЧИКОВ"""
#     return templates.TemplateResponse(
#         request=request,
#         name='error_add_payments.html',
#         context={'message': message},
#     )


@main_router.get('/resultoperation', response_class=HTMLResponse, name='result_operation')
def result_operation(request: Request, message: str, user=Depends(check_user_permissions)):
    """СТРАНИЦА ЕЗУЛЬТАТА ВЫПОЛНЕНИЯ ОПЕРАЦИИ (ДОБАВЛЕНИЯ ПОКАЗАТЕЛЕЙ, ОПЛАТЫ ...)"""
    message_dict = {}
    try:
        message_dict = json.loads(message)
    except Exception as e:
        pass
    return templates.TemplateResponse(
        request=request,
        name='result_operation.html',
        context={'message': message_dict,
                 'user': user},
    )


@main_router.get('/counterreadings', response_class=HTMLResponse, name='cr')
def get_cr(request: Request, user=Depends(check_user_permissions)):
    """СТОРІНКА ВІДОБРАЖЕННЯ ПОКАЗНИКІВ ЛІЧИЛЬНИКІВ"""
    with StorageManager() as uow:
        counters = uow.counterrepository.get(relation=True)
    return templates.TemplateResponse(
        request=request,
        name='counterreadings.html',
        context={
            'counters': counters,
            'user': user,
        }
    )


@main_router.get('/counterreadings/{counter_id}', response_class=HTMLResponse, name='cr_id')
def get_cr_by_id(request: Request, counter_id: int, user=Depends(check_user_permissions)):
    """СТОРІНКА ВІДОБРАЖЕННЯ ПОКАЗНИКІВ ЛІЧИЛЬНИКІВ"""
    with StorageManager() as uow:
        counters = uow.counterrepository.get(relation=True)
        counter = uow.counterrepository.get(relation=True, id=counter_id)
    return templates.TemplateResponse(
        request=request,
        name='counterreadings.html',
        context={
            'counters': counters,
            'counter': counter[0] if counter else [],
            'user': user
        }
    )


@main_router.get('/payments', response_class=HTMLResponse, name='pymnt')
def get_payments(request: Request, user=Depends(check_user_permissions)):
    """СТОРІНКА ВІДОБРАЖЕННЯ ІСТОРІЇ ПО ОПЛАТІ"""
    with StorageManager() as uow:
        providers = uow.providerrepository.get(relation=True)
    return templates.TemplateResponse(
        request=request,
        name='payments.html',
        context={
            'providers': providers,
            'user': user
        }
    )


@main_router.get('/payments/{provider_id}', response_class=HTMLResponse, name='pymnt_id')
def get_payment_by_id(request: Request, provider_id: int, user=Depends(check_user_permissions)):
    """СТОРІНКА ВІДОБРАЖЕННЯ ІСТОРІЇ ПО ОПЛАТІ ПО ВИЗНАЧЕНОМУ ПРОВАЙДЕРУ"""
    with StorageManager() as uow:
        providers = uow.providerrepository.get(relation=True)
        payments = uow.paymentrepository.get(relation=True, provider_id=provider_id)
    return templates.TemplateResponse(
        request=request,
        name='payments.html',
        context={
            'providers': providers,
            'payments': payments,
            'user': user
        }
    )


@main_router.get('/add_tariff/', name='add_tariff', response_class=HTMLResponse)
def page_add_tariff(request: Request, user=Depends(check_user_permissions)):
    """СТОРІНКА ВІДОБРАЖЕННЯ ФОРМИ ДЛЯ ДОДАННЯ НОВОГО ТАРИФУ"""
    with StorageManager() as uow:
        providers = uow.providerrepository.get()
        counters = uow.counterrepository.get(is_active=True)
        tariff_types = uow.tarifftyperepository.get()

    return templates.TemplateResponse(
        request=request,
        name='add_tariff.html',
        context={
            'providers': providers,
            'counters': counters,
            'tariff_types': tariff_types,
            'user': user
        }
    )


@main_router.get('/tariffs/', name='tariffs', response_class=HTMLResponse)
def get_all_tariffs(request: Request, user=Depends(check_user_permissions)):
    """Сторінка відображення всіх тарифів"""
    with StorageManager() as uow:
        categories = uow.categoryrepository.get()
    return templates.TemplateResponse(
        request=request,
        name='tariffs.html',
        context={
            'categories': categories,
            'user': user
        }
    )


@main_router.get('/tariffs/{category_id}', name='tariffs_id', response_class=HTMLResponse)
def get_all_tariffs(request: Request,
                    category_id: int,
                    is_active: Annotated[bool, Query()] = None,
                    user=Depends(check_user_permissions)):
    """Сторінка відображення всіх тарифів
    флаг is_active служить для фільтрації тарифів по статусу (активний/не активний)"""
    with StorageManager() as uow:
        categories = uow.categoryrepository.get()
        cur_cat = uow.categoryrepository.get(id=category_id)
        if cur_cat:
            cur_cat = cur_cat[0]
        tariffs = uow.tariffrepository.get_tariffs_by_category_id(category_id)
        if is_active:
            tariffs = remove_inactive_tariffs(tariffs)
        tariffs = remove_tariff_type_3_tariffs(tariffs)
    return templates.TemplateResponse(
        request=request,
        name='tariffs.html',
        context={
            'categories': categories,
            'tariffs': tariffs,
            'cur_cat': cur_cat,
            'user': user
        }
    )


@main_router.get('/tariff/{category_id}/{tariff_id}', name='tariffs_change_form', response_class=HTMLResponse)
def change_tariffs(request: Request, category_id: int, tariff_id: int, user=Depends(check_user_permissions)):
    """Сторінка відображення всіх тарифів"""
    with StorageManager() as uow:
        category = uow.categoryrepository.get(id=category_id)
        if category:
            category = category[0]
        tariff = uow.tariffrepository.get(id=tariff_id)
        if tariff:
            tariff = tariff[0]

    return templates.TemplateResponse(
        request=request,
        name='change_tariff.html',
        context={
            'category': category,
            'tariff': tariff,
            'user': user
        }
    )


@main_router.get('/exit', name='exit')
def user_exit():
    logger.debug('exit')
    response = RedirectResponse('/user/login')
    response.delete_cookie('access_token')
    return response
