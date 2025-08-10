from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from src.utilitiesaccounting_v4.services import electric_service
from src.utilitiesaccounting_v4.uow import UnitOfWork

main_router = APIRouter()
templates = Jinja2Templates(directory="templates")




@main_router.get('/', response_class=HTMLResponse, name='home')
def ts(request: Request):
    """MAIN PAGE"""
    debt = electric_service.calc_all_services()
    # with UnitOfWork() as uow:
    #     context = uow.category.get(relation=True)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            # 'categories': context,
            'debt': debt
        },
    )


@main_router.get('/erroraddcounterreadings', response_class=HTMLResponse, name='error_add_cr')
def error_add_cr(request: Request, message: str):
    """СТРАНИЦА ОШИБКИ ПРИ ВНЕСЕНИИ ПОКАЗАНИЙ СЧЕТЧИКОВ"""
    return templates.TemplateResponse(
        request=request,
        name='error_add_counter_readings.html',
        context={'message': message},
    )


@main_router.get('/successaddcounterreadings', response_class=HTMLResponse, name='success_add_cr')
def success_add_cr(request: Request):
    """СТРАНИЦА УДАЧНОГО ВНЕСЕНИЯ ПОКАЗАНИЙ СЧЕТЧИКОВ"""
    return templates.TemplateResponse(
        request=request,
        name='success_add_counter_readings.html',
    )


@main_router.get('/addcounterreadings', response_class=HTMLResponse, name='addcounterreadings')
def form_add_counter_readings(request: Request):
    """СТРАНИЦА ВНЕСЕНИЯ ПОКАЗАНИЙ СЧЕТЧИКОВ"""
    with UnitOfWork() as uow:
        counters = uow.counter.get(relation=True)
    return templates.TemplateResponse(
        request=request,
        name='formelement.html',
        context={'counters': counters}
    )


@main_router.get('/add_payment', response_class=HTMLResponse, name='payments')
def form_add_payments(request: Request):
    """СТРАНИЦА ВНЕСЕНИЯ ОПЛАТЫ"""
    context = electric_service.calc_all_services()
    return templates.TemplateResponse(
        request=request,
        name='add_payment.html',
        context={'categories': context},
    )


@main_router.get('/erroraddpayments', response_class=HTMLResponse, name='error_add_pymnt')
def error_add_pymnt(request: Request, message: str):
    """СТРАНИЦА ОШИБКИ ПРИ ВНЕСЕНИИ ПОКАЗАНИЙ СЧЕТЧИКОВ"""
    return templates.TemplateResponse(
        request=request,
        name='error_add_payments.html',
        context={'message': message},
    )


@main_router.get('/successaddpayments', response_class=HTMLResponse, name='success_add_pymnt')
def success_add_pymnt(request: Request):
    """СТРАНИЦА УДАЧНОГО ВНЕСЕНИЯ ПОКАЗАНИЙ СЧЕТЧИКОВ"""
    return templates.TemplateResponse(
        request=request,
        name='success_add_payments.html',
    )


@main_router.get('/counterreadings', response_class=HTMLResponse, name='cr')
def get_cr(request: Request):
    """СТОРІНКА ВІДОБРАЖЕННЯ ПОКАЗНИКІВ ЛІЧИЛЬНИКІВ"""
    with UnitOfWork() as uow:
        counters = uow.counter.get(relation=True)
    return templates.TemplateResponse(
        request=request,
        name='counterreadings.html',
        context={
            'counters': counters,
        }
    )


@main_router.get('/counterreadings/{counter_id}', response_class=HTMLResponse, name='cr_id')
def get_cr_by_id(request: Request, counter_id: int):
    """СТОРІНКА ВІДОБРАЖЕННЯ ПОКАЗНИКІВ ЛІЧИЛЬНИКІВ"""
    with UnitOfWork() as uow:
        counters = uow.counter.get(relation=True)
        counter = uow.counter.get(relation=True, id=counter_id)
    return templates.TemplateResponse(
        request=request,
        name='counterreadings.html',
        context={
            'counters': counters,
            'counter': counter[0] if counter else [],
        }
    )

@main_router.get('/payments', response_class=HTMLResponse, name='pymnt')
def get_payments(request: Request):
    """СТОРІНКА ВІДОБРАЖЕННЯ ІСТОРІЇ ПО ОПЛАТІ"""
    with UnitOfWork() as uow:
        providers = uow.provider.get(relation=True)
    return templates.TemplateResponse(
        request=request,
        name='payments.html',
        context={
            'providers': providers,
        }
    )


@main_router.get('/payments/{provider_id}', response_class=HTMLResponse, name='pymnt_id')
def get_payment_by_id(request: Request, provider_id: int):
    """СТОРІНКА ВІДОБРАЖЕННЯ ІСТОРІЇ ПО ОПЛАТІ ПО ВИЗНАЧЕНОМУ ПРОВАЙДЕРУ"""
    with UnitOfWork() as uow:
        providers = uow.provider.get(relation=True)
        payments = uow.payment.get(relation=True, provider_id=provider_id)
    return templates.TemplateResponse(
        request=request,
        name='payments.html',
        context={
            'providers': providers,
            'payments': payments,
        }
    )
