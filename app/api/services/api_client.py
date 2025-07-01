import requests
from api.interfaces import IApiClient
from typing import Optional, Dict, Any


class ApiClient(IApiClient):

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get(
        self, endpoint: str, params: Optional[Dict[str, int]] = None
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:

            response = requests.get(url, params=params) if params else requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise RuntimeError(f"Erro ao fazer requisição GET para {url}: {e}") from e
