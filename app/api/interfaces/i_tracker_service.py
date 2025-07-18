from abc import ABC, abstractmethod
from api.models.plant_models import Plant


class ITrackerService(ABC):
    @abstractmethod
    def fetch_all_tracker_last_angle(self, plant: Plant):
        pass

    def fetch_tracker_historical_angle(self, tracker_number: int, plant: Plant):
        pass

    def fetch_trackers_alarm(self, plant: Plant):
        pass
