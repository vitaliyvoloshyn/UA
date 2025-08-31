# from dataclasses import dataclass
# from typing import TypeVar
#
# from sqlalchemy.orm import Session
#
# from src.utilitiesaccounting.database import db_session_maker
# from src.utilitiesaccounting.repository import SqlRepository, CategoryRepository, ProviderRepository, \
#     MeasurementUnitRepository, TariffTypeRepository, CounterRepository, CounterReadingRepository, TariffRepository, \
#     PaymentRepository
#
# REPO = TypeVar('REPO', bound=SqlRepository)
#
#
# @dataclass
# class Repositories:
#     category: REPO = CategoryRepository
#     provider: REPO = ProviderRepository
#
#
# class UnitOfWork[REPO]:
#
#     def __init__(self, session=None):
#         self.session = session
#         if session is None:
#             self.session: Session = db_session_maker()
#         self.category = CategoryRepository(self.session)
#         self.provider = ProviderRepository(self.session)
#         self.measurement_unit = MeasurementUnitRepository(self.session)
#         self.tariff_type = TariffTypeRepository(self.session)
#         self.tariff = TariffRepository(self.session)
#         self.counter = CounterRepository(self.session)
#         self.counter_reading = CounterReadingRepository(self.session)
#         self.payment = PaymentRepository(self.session)
#
#     def __enter__(self):
#         return self
#
#     def __exit__(self, exc_type, exc_val, exc_tb):
#         try:
#             self.commit()
#         except Exception as e:
#             self.rollback()
#             print(e)
#         finally:
#             self.session.close()
#
#     def rollback(self):
#         self.session.rollback()
#
#     def commit(self):
#         self.session.commit()
#
#
# if __name__ == '__main__':
#     ...
