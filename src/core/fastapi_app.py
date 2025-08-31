from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from src.utilitiesaccounting.routers import main_router
from src.utilitiesaccounting.api import api_router
from src.auth.api import user_router

fastapi_app = FastAPI()
fastapi_app.include_router(main_router)
fastapi_app.include_router(api_router)
fastapi_app.include_router(user_router)
fastapi_app.mount("/static", StaticFiles(directory="static/"), name="static")

fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_app():
    return fastapi_app
