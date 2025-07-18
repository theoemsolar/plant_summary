from datetime import datetime, timedelta
from domain.models.inverter import Inverter
from api.interfaces import IInverterService, IApiClient
from mocks import mock_invertes

FSP_LIMIT_INVERTER = 20


class InverterService(IInverterService):
    def __init__(self, api_client: IApiClient):
        self.api_client = api_client

    def get_all_inverters_last_data(self):
        response = self.api_client.get(f"/inverter/generation/all")
        return response

    def excel_timestamp_to_datetime(selfm, ts: float) -> datetime:
        base_date = datetime(1899, 12, 30)  # Excel considera 1900-01-01 como dia 1
        return base_date + timedelta(days=ts)
