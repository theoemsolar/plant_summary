from abc import ABC, abstractmethod


class IApiClient(ABC):
    @abstractmethod
    def get(self, endpoint: str, params: dict = None) -> dict:
        pass
