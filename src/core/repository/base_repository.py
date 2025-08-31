from abc import ABC, abstractmethod

from pydantic import BaseModel
from sqlalchemy.orm import Session


class RepositoryBase(ABC):
    def __init__(self, session: Session):
        self.session = session

    @abstractmethod
    def add(self, record: BaseModel):
        ...

    @abstractmethod
    def remove(self, pk: int):
        ...

    @abstractmethod
    def get(self):
        ...

    @abstractmethod
    def update(self, pk: int, **data):
        ...