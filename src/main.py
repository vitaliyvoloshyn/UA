import uvicorn

from src.utilitiesaccounting_v4.data import add_data
from src.utilitiesaccounting_v4.database import drop_db, create_db
from src.utilitiesaccounting_v4.fastapi_app import fastapi_app

if __name__ == '__main__':
    # drop_db()
    # create_db()
    # add_data()
    uvicorn.run(app='main:fastapi_app', host='0.0.0.0', port=5555, reload=True)
