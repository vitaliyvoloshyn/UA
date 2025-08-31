from typing import Type, List

from sqlalchemy.orm import Session

from src.core.database import db_session_maker
from .repository.base_repository import RepositoryBase


class StorageManager:
    session: Session = db_session_maker()

    # def __init__(self, session: Session = None):
    #     self.session = session
    #     if session is None:
    #         self.

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.commit()
        except Exception as e:
            self.rollback()
            print(e)
        finally:
            self.session.close()

    def rollback(self):
        self.session.rollback()

    def commit(self):
        self.session.commit()

    @classmethod
    def register_repository(cls, repository: Type[RepositoryBase] | List[Type[RepositoryBase]]):
        if isinstance(repository, list):
            for repo in repository:
                cls._register_repository(repo)
            return
        cls._register_repository(repository)

    @classmethod
    def _register_repository(cls, repository: Type[RepositoryBase]):
        """Добавляет в атрибуты класса атрибут репозитория з названием класса в нижнем регистре"""
        setattr(cls, repository.__name__.lower(), repository(cls.session))


if __name__ == '__main__':
    ...
