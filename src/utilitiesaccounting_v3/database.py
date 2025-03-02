from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.utilitiesaccounting_v3.models import Base

engine = create_engine("sqlite:///ua.db", echo=False)
db_session_maker = sessionmaker(engine)


def create_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)


if __name__ == '__main__':
    drop_db()
    create_db()
