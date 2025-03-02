import logging

from src.utilitiesaccounting_v3.services import (CategoryService,
                                                 CounterService,
                                                 CounterReadingService,
                                                 TariffService,
                                                 ProviderService)

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)


def get_category():
    with CategoryService().storage_manager() as sm:
        res = sm.category.get()
        log.debug(res)
def get_provider():
    with ProviderService().storage_manager() as sm:
        res = sm.provider.get(relation=True)
        log.debug(res)

def get_counters():
    with CounterService().storage_manager() as sm:
        res = sm.counter.get(relation=True)
        log.debug(res)


if __name__ == '__main__':
    get_category()

