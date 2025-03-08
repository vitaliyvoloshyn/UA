from src.utilitiesaccounting_v4.data import add_data
from src.utilitiesaccounting_v4.database import create_db, drop_db
from src.utilitiesaccounting_v4.get_test_data import get_consumption_tariffs_on_category
from src.utilitiesaccounting_v4.tariff_manager import ConsumptionVolumeTariffManager

if __name__ == '__main__':
    drop_db()
    create_db()
    add_data()

    # get_category()
    # get_provider()
    # get_counters()
    tariffs_ = get_consumption_tariffs_on_category("Електропостачання", 2)
    print(ConsumptionVolumeTariffManager().calculate(tariffs_))
