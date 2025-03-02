from src.utilitiesaccounting_v4.database import create_db, drop_db
from src.utilitiesaccounting_v4.data import TestData
from src.utilitiesaccounting_v4.get_test_data import get_category, get_provider, get_counters

if __name__ == '__main__':
    drop_db()
    create_db()
    TestData()

    get_category()
    get_provider()
    get_counters()
