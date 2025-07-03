from abc import ABC, abstractmethod


class ITrackerService(ABC):
    @abstractmethod
    def fetch_all_tracker_last_angle(self, tracker: int) -> dict:
        pass
