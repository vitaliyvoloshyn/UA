from sqlalchemy.orm import Mapped, mapped_column

from src.core import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(server_default='True')
    is_admin: Mapped[bool] = mapped_column(server_default='False')
    avatar: Mapped[str] = mapped_column(nullable=True)
