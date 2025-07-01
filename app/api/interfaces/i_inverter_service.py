from abc import ABC, abstractmethod


class IInverterService(ABC):
    @abstractmethod
    def fetch_inverter_data(self, fsp: str, inverter_id: str) -> dict:
        pass
