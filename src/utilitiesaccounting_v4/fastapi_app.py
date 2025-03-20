from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from src.utilitiesaccounting_v4.routers import main_router
from src.utilitiesaccounting_v4.api import api_router

fastapi_app = FastAPI()
fastapi_app.include_router(main_router)
fastapi_app.include_router(api_router)
fastapi_app.mount("/static", StaticFiles(directory="static/"), name="static")
