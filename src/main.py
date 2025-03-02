from src.utilitiesaccounting_v3.database import create_db, drop_db
from src.utilitiesaccounting_v3.schemas.category_dto import CategoryAddDTO
from src.utilitiesaccounting_v3.services import CategoryService
from utilitiesaccounting_v3.data import TestData

if __name__ == '__main__':
    drop_db()
    create_db()
    TestData()
