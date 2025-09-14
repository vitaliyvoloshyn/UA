from fastapi import APIRouter
from src.core.logging import logger
from starlette.responses import JSONResponse

from src.core.uow import StorageManager
from src.utilitiesaccounting.schemas.result_content import ErrorResultContent, SuccessResultContent
from .schemas import UserAddDTO, UserSignInDTO
from .service import encode_jwt, validate_user

user_api_router = APIRouter(prefix='/api/user', tags=['User Api'])


@user_api_router.post('/signup', name='signup')
def user_signup(data: UserAddDTO) -> JSONResponse:
    logger.info(f'Запит на реєстрацію - {data.email}')
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
        logger.warning(f'Помилка при реєстрації нового користувача {data} - {e}')
        attrs['message_operation'] = str(e)
        res_cont = ErrorResultContent(**attrs)
        return JSONResponse(content=res_cont.model_dump(),
                            status_code=400)
    attrs[
        'message_operation'] = f'{data.first_name.capitalize()}, вітаємо Вас в системі обліку комунальних послуг <br> hsdgfhds'
    res_cont = SuccessResultContent(**attrs)
    return JSONResponse(content=res_cont.model_dump(), status_code=200)


@user_api_router.post('/signin', name='signin')
def user_signin(user_schema: UserSignInDTO):
    logger.info(f'Запит на аутентифікацію - {user_schema.email}')
    if validate_user(user_schema):
        token = (encode_jwt(user_schema))
        response = JSONResponse(content='Ви успішно авторизовані в системі')
        response.set_cookie(key='access_token', value=token)
        return response
