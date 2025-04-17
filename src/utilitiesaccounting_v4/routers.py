from typing import List

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from src.utilitiesaccounting_v4.schemas.debt_dto import DebtDTO
from src.utilitiesaccounting_v4.services import ElectricService, WaterService
from src.utilitiesaccounting_v4.uow import UnitOfWork

main_router = APIRouter()
templates = Jinja2Templates(directory="templates")

ws = WaterService()
es = ElectricService()


@main_router.get('/', response_class=HTMLResponse, name='home')
def ts(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"id": id}
    )


@main_router.post('/', response_class=HTMLResponse, name='home')
def ts_post(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"id": id}
    )


@main_router.get('/erroraddcounterreadings', response_class=HTMLResponse, name='error_add_cr')
def error_add_cr(request: Request, message: str):
    return templates.TemplateResponse(
        request=request,
        name='error_add_counter_readings.html',
        context={'message': message},
    )


@main_router.get('/successaddcounterreadings', response_class=HTMLResponse, name='success_add_cr')
def success_add_cr(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='success_add_counter_readings.html',
    )


@main_router.get('/datatables.html')
def ts():
    template = env.get_template('datatables.html')
    res = ws.calc_all_services()
    return HTMLResponse(template.render(context=res))


@main_router.get('/electric_debt', response_model=DebtDTO)
def ts():
    res = es.calc()
    return res


@main_router.get('/water_debt', response_model=DebtDTO)
def ts1():
    res = ws.calc()
    return res


@main_router.get('/all_debt', response_model=List[DebtDTO])
def ts1() -> HTMLResponse:
    res = ws.calc_all_services()
    return res


@main_router.get('/form')
def form(request: Request):
    with UnitOfWork() as uow:
        context = uow.counter.get(relation=True)
    return templates.TemplateResponse(
        request=request,
        name='form1.html',
        context={'cr': context},
    )


@main_router.get('/addcounterreadings', response_class=HTMLResponse, name='addcounterreadings')
def form_add_counter_readings(request: Request):
    with UnitOfWork() as uow:
        counters = uow.counter.get(relation=True)
    return templates.TemplateResponse(
        request=request,
        name='formelement.html',
        context={'counters': counters}
    )
