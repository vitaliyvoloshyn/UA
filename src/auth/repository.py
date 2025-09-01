from pydantic import BaseModel

from src.auth.models import User
from src.auth.schemas import UserDTO, UserAddDTO
from src.core.repository.sqlalchemy_repository import SqlRepository
from src.core.uow import StorageManager


class UserRepository(SqlRepository):
    model = User
    dto = UserDTO
    dto_add = UserAddDTO

    def add(self, record: BaseModel):
        """Добавление нового пользователя. Но сначала проверяется отсутствие этого пользователя в системе"""
        with StorageManager() as sm:
            user = sm.userrepository.get(email=record.email)
            if user:
                raise ValueError('Користувач з таким email вже зареєстрований в системі')
        super().add(record)


StorageManager.register_repository(UserRepository)
