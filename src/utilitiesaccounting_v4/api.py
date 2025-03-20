import loguru
from fastapi import APIRouter
from src.utilitiesaccounting_v4.schemas.counter_reading_dto import CounterReadingAddDTO
from src.utilitiesaccounting_v4.uow import UnitOfWork

api_router = APIRouter(
    prefix='/api',
    tags=['API']
)


@api_router.post('/add_counterreading', name='form')
def add_counter_reading(record: CounterReadingAddDTO):
    """Пост-запрос на добавление показателей счетчиков"""
    with UnitOfWork() as uow:
        uow.counter_reading.add(record)
    loguru.logger.info(f"Added new counter readings")
