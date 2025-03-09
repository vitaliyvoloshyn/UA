from fastapi import APIRouter
from jinja2 import Environment, FileSystemLoader
from starlette.responses import HTMLResponse

from src.utilitiesaccounting_v4.services import ElectricService, WaterService

main_router = APIRouter()
loader = FileSystemLoader("static")
env = Environment(loader=loader)
template = env.get_template('index.html')


@main_router.get('/electric_debt')
def ts():
    es = ElectricService()
    res = es.calc()
    return res


@main_router.get('/water_debt')
def ts1():
    es = WaterService()
    res = es.calc()
    return res
