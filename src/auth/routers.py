from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

auth_router = APIRouter(prefix='/user', tags=['User'])
templates = Jinja2Templates(directory="templates")


@auth_router.get('/registration', name='reg', response_class=HTMLResponse)
def get_registration(request: Request):
    """Страница регистрации пользователя"""
    return templates.TemplateResponse(
        request=request,
        name="registration.html",
    )
