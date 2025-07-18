from datetime import datetime, timedelta
from api.interfaces import IApiClient, ITrackerService
from mocks import trackers_positions, tracker_historical_position, tracker_alarms


class TrackerService(ITrackerService):

    def __init__(self, api_client: IApiClient):
        self.api_client = api_client

    def fetch_all_tracker_last_angle(self):
        response = self.api_client.get(f"/tracker/angles/all")
        return response
        # return trackers_positions

    def fetch_tracker_historical_angle(self, tracker_number: int):
        response = self.api_client.get(f"/tracker/angles/{tracker_number}")
        return response
        # return tracker_historical_position

    def fetch_trackers_alarm(self):
        response = self.api_client.get(f"/tracker/alarms/all")
        return response
        # return tracker_alarms
