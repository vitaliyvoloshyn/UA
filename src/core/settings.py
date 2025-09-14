from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent

# --------------------\ Application /--------------------

APP_HOST = '0.0.0.0'
APP_PORT = 5555
APP_RELOAD = False

logging_file = Path(BASE_DIR, 'src/logging.txt')
logging_level = 'INFO'
file_rotation = '10 MB'
file_retention = 20  # буде збережено тільки 20 останніх файлів

# --------------------\ Database /--------------------

DB_URL = f"sqlite:///ua.db"
DB_ECHO = False

# --------------------\ Auth /--------------------
private_key_path: Path = BASE_DIR / 'src' / 'certs' / 'jwt-private.pem'
public_key_path: Path = BASE_DIR / 'src' / 'certs' / 'jwt-public.pem'
algorithm: str = 'RS256'
access_token_expire_days: int = 30

user_photo_upload_path = Path(BASE_DIR, 'src/static/asset/img')


if __name__ == '__main__':
    print(BASE_DIR)
