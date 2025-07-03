from api.interfaces import IAlarmService, IApiClient


class AlarmService(IAlarmService):

    def __init__(self, api_client: IApiClient):
        self.api_client = api_client

    def fetch_alarms(self, limit: int = 100) -> dict:
        return self.api_client.get("/alarms", params={"limit": limit})

    def fetch_all_last_alarms(self):
        return self.api_client.get("/alarms/all")
