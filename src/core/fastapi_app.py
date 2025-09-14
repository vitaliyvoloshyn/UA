from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.staticfiles import StaticFiles

from src.auth.service import HTTPExceptionUARouters_handler, HTTPExceptionUARouters, HTTPExceptionUAApi, \
    HTTPExceptionUAApi_handler
from src.utilitiesaccounting.routers import main_router
from src.utilitiesaccounting.api import api_router
from src.auth.api import user_api_router
from src.auth.routers import auth_router

fastapi_app = FastAPI()
fastapi_app.include_router(main_router)
fastapi_app.include_router(api_router)
fastapi_app.include_router(user_api_router)
fastapi_app.include_router(auth_router)
fastapi_app.mount("/static", StaticFiles(directory="static/"), name="static")
fastapi_app.add_exception_handler(HTTPExceptionUARouters, HTTPExceptionUARouters_handler)
fastapi_app.add_exception_handler(HTTPExceptionUAApi, HTTPExceptionUAApi_handler)

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_app():
    return fastapi_app
