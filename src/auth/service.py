from datetime import timedelta, datetime, UTC
from typing import Any

import bcrypt
import jwt
from fastapi import HTTPException
from fastapi.security import APIKeyCookie
from jwt import InvalidTokenError
from pydantic import BaseModel
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from src.auth.exeptions import UnknownUserException, InvalidPasswordException
from src.auth.schemas import UserSignInDTO
from src.core import settings
from src.core.uow import StorageManager
from src.core.logging import logger

cookie_scheme = APIKeyCookie(name="access_token", auto_error=False)


class HTTPExceptionUARouters(HTTPException):
    def __init__(self, status_code, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class HTTPExceptionUAApi(HTTPException):
    def __init__(self, status_code, detail: str):
        super().__init__(status_code=status_code, detail=detail)


def user_exist(email: str):
    """Проверка существования пользователя в базе данных. Проверяются по email.
    Возвращает ИСТИНУ если пользователь найден в БД, и ЛОЖЬ - если нет"""

    with StorageManager() as sm:
        user_db = sm.userrepository.get_by_email(email)
        if user_db:
            return user_db
    return False


def validate_user(data: UserSignInDTO) -> bool:
    if not (user_ := user_exist(data.email)):
        logger.warning(f'Помилка валідаціі користувача (невідомий користувач) - {data.email}')
        raise UnknownUserException
    if not check_password(data.password, user_.password):
        logger.warning(f'Помилка валідаціі користувача (невірний пароль) - {data.email}')
        raise InvalidPasswordException
    return True


def check_password(password: str, hashed_password: bytes):
    return bcrypt.checkpw(password.encode(), hashed_password)


def hash_password(password: str) -> bytes:
    """Хеш-функция"""
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def encode_jwt(
        user_: UserSignInDTO,
        private_key: str = settings.private_key_path.read_text(),
        algorithm: str = settings.algorithm,
        expire_day: int = settings.access_token_expire_days,
        expire_timedelta: timedelta | None = None
) -> str:
    to_encode = get_payload(user_)
    now = datetime.now(UTC)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(days=expire_day)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


def get_payload(user_: UserSignInDTO) -> dict:
    payload = {'sub': user_.email}
    return payload


def decode_jwt(
        token: str | bytes,
        public_key: str = settings.public_key_path.read_text(),
        algorithm: str = settings.algorithm,
) -> Any:
    decoded = jwt.decode(token, public_key, algorithm)
    return decoded


def HTTPExceptionUARouters_handler(request: Request, exc: HTTPExceptionUARouters):
    if exc.status_code in (401, 403):
        return RedirectResponse('/user/login')


def HTTPExceptionUAApi_handler(request: Request, exc: HTTPExceptionUAApi):
    if exc.status_code in (401, 403):
        raise HTTPException(exc.status_code, exc.detail)


async def get_current_token_payload(request: Request):
    """Возвращает payload из куки"""
    token = await cookie_scheme(request=request)
    try:
        payload = decode_jwt(token)
    except InvalidTokenError as e:
        logger.warning(f'error 401//{e}')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f'invalid token: {e}')
    return payload


async def get_current_auth_user(request: Request) -> BaseModel:
    """Возвращает пользователя из БД"""
    payload: dict = await get_current_token_payload(request)
    user_email: str | None = payload.get("sub")
    with StorageManager() as sm:
        user = sm.userrepository.get_by_email(user_email)
    if not user:
        logger.debug('error 403')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='token invalid (user not found)')

    return user


async def get_current_active_user(request: Request):
    user = await get_current_auth_user(request)
    if user.is_active:
        return user
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail='user inactive')


async def check_user_permissions(request: Request):
    user = None
    try:
        user: BaseModel = await get_current_active_user(request)
    except HTTPException as e:
        raise HTTPExceptionUARouters(e.status_code, e.detail)
    return user


async def check_user_permissions_api(request: Request):
    user = None
    try:
        user: BaseModel = await get_current_active_user(request)
    except HTTPException as e:
        raise HTTPExceptionUAApi(e.status_code, e.detail)
    return user


if __name__ == '__main__':
    ...
