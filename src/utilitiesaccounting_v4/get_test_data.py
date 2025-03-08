import logging

from src.utilitiesaccounting_v4.services import (CategoryService,
                                                 CounterService,
                                                 TariffService,
                                                 ProviderService,
                                                 ElectricService)
from src.utilitiesaccounting_v4.tariff_manager import SubscriptionTariffManager

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)

electric_service = ElectricService()
electric_service.add_tariff_manager(SubscriptionTariffManager)


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


def get_tariffs_on_category(category_name: str, tariff_type: int):
    with TariffService().storage_manager() as sm:
        res = sm.tariff.get_tariffs_by_category_tariff_type(category_name, tariff_type)
        log.debug(res)
        return res


if __name__ == '__main__':
    tariffs_of_electric = electric_service.storage_manager
