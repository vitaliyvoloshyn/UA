from pathlib import Path
from typing import Annotated, Any

from fastapi import APIRouter, Depends, UploadFile, Form, File
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from src.auth.service import check_user_permissions
from src.core.logging import logger
from src.core.settings import user_photo_upload_path

auth_router = APIRouter(prefix='/user', tags=['User'])
templates = Jinja2Templates(directory="templates")


@auth_router.get('/registration', name='reg', response_class=HTMLResponse)
def get_registration(request: Request):
    """Страница регистрации пользователя"""
    return templates.TemplateResponse(
        request=request,
        name="registration.html",
    )

@auth_router.get('/login', name='login', response_class=HTMLResponse)
def login(request: Request):
    """Сторінка для аутентифікації"""
    return templates.TemplateResponse(
        request=request,
        name="login.html",
    )

@auth_router.get('/profile', name='profile', response_class=HTMLResponse)
def profile(request: Request, user=Depends(check_user_permissions)):
    """Сторінка для аутентифікації"""
    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={
            'user': user
        },
    )

@auth_router.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    x = await file.read()
    with open(Path(user_photo_upload_path, file.filename), 'wb') as f:
        f.write(x)
    logger.debug(x)
    return {"filename": file.filename}

@auth_router.post('/change_profile', name='change_profile')
def change_profile(request: Request,
                   first_name: Annotated[str, Form()] = None,
                   last_name: Annotated[str, Form()] = None,
                   file: UploadFile = None):
    logger.debug(first_name)
    logger.debug(last_name)
    logger.debug(file)
    return {
    # 'detail': first_name,
            'photo': file}
