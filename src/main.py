import uvicorn

# from src.utilitiesaccounting_v4.data import add_data
# from src.utilitiesaccounting_v4.database import create_db, drop_db
# from src.utilitiesaccounting_v4.get_test_data import get_tariffs_on_category
from src.utilitiesaccounting_v4.tariff_manager import ConsumptionVolumeTariffManager, OnTimeChargeTariffManager
from src.utilitiesaccounting_v4.fastapi_app import fastapi_app

if __name__ == '__main__':
    # drop_db()
    # create_db()
    # add_data()

    # get_category()
    # get_provider()
    # get_counters()
    # tariffs_ = get_tariffs_on_category("Електропостачання", 3)
    # print(OnTimeChargeTariffManager().calculate(tariffs_))
    uvicorn.run(app='main:fastapi_app', host='0.0.0.0', port=5555, reload=True)
    # TODO: Создание формы для внесения показателей по одному счетчику

