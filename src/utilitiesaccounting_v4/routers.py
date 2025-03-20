from typing import List

from fastapi import APIRouter
from jinja2 import Environment, FileSystemLoader
from starlette.responses import HTMLResponse

from src.utilitiesaccounting_v4.schemas.debt_dto import DebtDTO
from src.utilitiesaccounting_v4.services import ElectricService, WaterService

main_router = APIRouter()
loader = FileSystemLoader("static")
env = Environment(loader=loader)

ws = WaterService()
es = ElectricService()


@main_router.get('/')
def ts():
    template = env.get_template('index.html')

    return HTMLResponse(template.render())

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
def form():
    template = env.get_template('form1.html')
    return HTMLResponse(template.render())
