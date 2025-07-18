from abc import ABC, abstractmethod
from api.models.plant_models import Plant


class IInverterService(ABC):
    @abstractmethod
    def get_all_inverters_last_data(self, plant: Plant) -> dict:
        pass
