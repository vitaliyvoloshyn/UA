import bcrypt

from src.core.uow import StorageManager


def user_exist(email: str):
    """Проверка существования пользователя в базе данных. Проверяются по email"""

    with StorageManager() as sm:
        user_db = sm.userrepository.get_by_email(email)
        if not user_db:
            return True
    raise ValueError('Користувач з таким email вже зареєстрований в системі')


def hash_password(password: str) -> bytes:
    """Хеш-функция"""
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


if __name__ == '__main__':
    print(hash_password('qwerty'))
