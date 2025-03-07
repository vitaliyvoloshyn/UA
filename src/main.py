from src.utilitiesaccounting_v4.database import create_db, drop_db
from src.utilitiesaccounting_v4.data import TestData
from src.utilitiesaccounting_v4.get_test_data import get_category, get_provider, get_counters, get_tariffs_on_category
from src.utilitiesaccounting_v4.tariff_manager import SubscriptionTariffManager

if __name__ == '__main__':
    # drop_db()
    # create_db()
    # TestData()

    # get_category()
    # get_provider()
    # get_counters()
    tariffs_ = get_tariffs_on_category("Електропостачання", 1)
    SubscriptionTariffManager().calculate(tariffs_)
