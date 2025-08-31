from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from .settings import DB_URL, DB_ECHO

engine = create_engine(url=DB_URL,
                       echo=DB_ECHO)

db_session_maker = sessionmaker(engine)


class Base(DeclarativeBase):
    pass


def create_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    drop_db()
    create_db()
