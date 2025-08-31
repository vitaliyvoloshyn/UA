from src.auth.models import User
from src.auth.schemas import UserDTO, UserAddDTO
from src.utilitiesaccounting_v4.repository import SqlRepository


class UserRepository(SqlRepository):
    model = User
    dto = UserDTO
    dto_add = UserAddDTO
