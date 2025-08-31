from src.utilitiesaccounting_v4.repository import RepositoryBase, SchemaModel


class UserRepository(RepositoryBase):
    def get(self):
        ...

    def add(self, record: SchemaModel):
        ...

    def update(self, pk: int, **data):
        ...

    def remove(self, pk: int):
        ...
