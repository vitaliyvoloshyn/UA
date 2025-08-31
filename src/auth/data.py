from src.core.uow import StorageManager
from .schemas import UserAddDTO

user1 = UserAddDTO(
    first_name='Vitaly',
    last_name='Voloshin',
    email='vitaliy.srt1985@gmail.com',
    password='qwerty'
)

user2 = UserAddDTO(
    first_name='Olya',
    last_name='Voloshina',
    email='olya.voloshina.edu@gmail.com',
    password='123'
)


def insert_test_data():
    with StorageManager() as sm:
        sm.userrepository.add(user1)
        sm.userrepository.add(user2)
