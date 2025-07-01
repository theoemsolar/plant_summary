from datetime import datetime, timedelta
from domain.models.inverter import Inverter
from api.interfaces import IInverterService, IApiClient
from mock import mock

FSP_LIMIT_INVERTER = 20


class InverterService(IInverterService):
    def __init__(self, api_client: IApiClient):
        self.api_client = api_client

    def fetch_inverter_data(self, fsp: int, inverter_id: int, limit: int = 100) -> list:
        response = self.api_client.get(
            f"/ufv/fsp{fsp:02d}/inverter/{inverter_id}",
            params={"limit": limit, "skip": 0},
        )
        return [
            Inverter(
                inverter_id,
                fsp,
                self.excel_timestamp_to_datetime(item["E3TimeStamp"]),
                item["FieldValue"],
            )
            for item in response
        ]

    def get_all_inverters_last_data(self):
        response = self.api_client.get(f"/ufv/metric/generation/all")
        return response

    def excel_timestamp_to_datetime(selfm, ts: float) -> datetime:
        base_date = datetime(1899, 12, 30)  # Excel considera 1900-01-01 como dia 1
        return base_date + timedelta(days=ts)
