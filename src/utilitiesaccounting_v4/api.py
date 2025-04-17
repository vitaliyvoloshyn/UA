from typing import List

import loguru
from fastapi import APIRouter
from starlette.responses import JSONResponse, RedirectResponse, HTMLResponse

from src.utilitiesaccounting_v4.schemas.counter_reading_dto import CounterReadingAddDTO
from src.utilitiesaccounting_v4.uow import UnitOfWork
from src.utilitiesaccounting_v4.utils import validate_counter_readings

api_router = APIRouter(
    prefix='/api',
    tags=['API']
)


@api_router.post('/add_counterreading', name='add_counterreading')
def add_counter_reading(records: List[CounterReadingAddDTO]):
    """Пост-запрос на добавление показателей счетчиков"""
    loguru.logger.debug(records)
    try:
        validate_counter_readings(records)
    except ValueError as e:
        return JSONResponse(content=str(e),
                            status_code=400)
    with UnitOfWork() as uow:
        uow.counter_reading.add_all(records)
    loguru.logger.info(f"Added new counter readings")
    return JSONResponse(content='OK', status_code=200)
