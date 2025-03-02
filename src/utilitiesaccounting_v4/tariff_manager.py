from abc import ABC, abstractmethod


class TariffManager(ABC):
    @abstractmethod
    def calculate(self):
        ...


class SubscriptionTariffManager(TariffManager):
    """
    Вытащить тариф
    """
    def calculate(self):
        ...
