from src.auth.models import User
from src.auth.schemas import UserDTO, UserAddDTO
from src.core.repository.sqlalchemy_repository import SqlRepository
from src.core.uow import StorageManager


class UserRepository(SqlRepository):
    model = User
    dto = UserDTO
    dto_add = UserAddDTO


StorageManager.register_repository(UserRepository)
