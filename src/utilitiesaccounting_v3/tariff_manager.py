from abc import ABC, abstractmethod


class TariffManager(ABC):
    @abstractmethod
    def calculate(self):
        ...


class SubscriptionTariffManager(TariffManager):
    def calculate(self):
        ...
