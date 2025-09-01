from fastapi import APIRouter
from loguru import logger
from starlette.responses import JSONResponse

from .schemas import UserAddDTO
from src.core.uow import StorageManager
from src.utilitiesaccounting.schemas.result_content import ErrorResultContent, SuccessResultContent

user_api_router = APIRouter(prefix='/api/user', tags=['User Api'])


@user_api_router.post('/signup', name='signup')
def user_signup(data: UserAddDTO) -> JSONResponse:
    """Пост-запит на реєстрацію нового користувача"""
    attrs = {
        'header': 'Реєстрація нового користувача',
        'back_ref': 'tariffs',
        'back_ref_text': 'Повернутися на сторінку перегляду тарифів',
    }
    try:
        with StorageManager() as sm:
            sm.userrepository.add(data)
    except Exception as e:
        logger.error(f'Помилка при реєстрації нового користувача {data} - {e}')
        attrs['message_operation'] = str(e)
        res_cont = ErrorResultContent(**attrs)
        return JSONResponse(content=res_cont.model_dump(),
                            status_code=400)
    logger.info(f'Request for signup {data.email}')
    attrs['message_operation'] = f'{data.first_name.capitalize()}, вітаємо Вас в системі обліку комунальних послуг <br> hsdgfhds'
    res_cont = SuccessResultContent(**attrs)
    return JSONResponse(content=res_cont.model_dump(), status_code=200)
