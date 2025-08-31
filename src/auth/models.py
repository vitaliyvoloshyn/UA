from sqlalchemy.orm import Mapped

from src.utilitiesaccounting_v4.models import Base


class User(Base):
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
