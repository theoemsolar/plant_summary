from abc import ABC, abstractmethod
from typing import Dict, Any
from api.models.plant_models import Plant


class IAlarmService(ABC):
    @abstractmethod
    def fetch_all_last_alarms(self) -> Dict[str, Any]:
        pass
