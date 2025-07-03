from abc import ABC, abstractmethod


class IAlarmService(ABC):
    @abstractmethod
    def fetch_alarms(self) -> dict:
        pass
