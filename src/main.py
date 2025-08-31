import uvicorn

from src.auth.data import insert_test_data as insert_test_users
from src.utilitiesaccounting.data import add_data as insert_test_data
from src.core.database import create_db, drop_db
from src.core.fastapi_app import get_app
from src.core.settings import APP_PORT, APP_RELOAD, APP_HOST
from src.auth.models import *
from src.utilitiesaccounting.models import *

fastapi_app = get_app()

if __name__ == '__main__':
    drop_db()
    create_db()
    insert_test_users()
    insert_test_data()
    # add_data()
    uvicorn.run(app='main:fastapi_app', host=APP_HOST, port=APP_PORT, reload=APP_RELOAD)
