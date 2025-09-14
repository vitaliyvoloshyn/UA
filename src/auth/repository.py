from pydantic import BaseModel

from src.auth.models import User
from src.auth.schemas import UserDTO, UserAddDTO
from src.auth.service import user_exist, hash_password
from src.core.repository.sqlalchemy_repository import SqlRepository
from src.core.uow import StorageManager


class UserRepository(SqlRepository):
    model = User
    dto = UserDTO
    dto_add = UserAddDTO

    def add(self, record: BaseModel):
        """Добавление нового пользователя. Но сначала проверяется отсутствие этого пользователя в системе"""
        if user_exist(record.email):
            raise ValueError('Користувач з таким email вже зареєстрований в системі')
        record.password = hash_password(record.password)
        super().add(record)

    @staticmethod
    def get_by_email(email: str):
        with StorageManager() as sm:
            user = sm.userrepository.get(email=email)
        return user[0] if user else None


StorageManager.register_repository(UserRepository)
