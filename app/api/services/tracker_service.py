from datetime import datetime, timedelta
from api.interfaces import IApiClient, ITrackerService


class TrackerService(ITrackerService):

    def __init__(self, api_client: IApiClient):
        self.api_client = api_client

    def fetch_all_tracker_last_angle(self):
        response = self.api_client.get(f"/tracker/all")
        return response

    def fetch_tracker_historical_angle(self, tracker_number: int):
        response = self.api_client.get(f"/tracker/{tracker_number}/historical/")
        return response
