import os
import datetime
import streamlit as st
from dotenv import load_dotenv
from api.services import ApiClient, TrackerService

load_dotenv()
BASE_URL = "https://oemsolarfsp.loca.lt"

URL = {
    "Santo Antonio": "https://oemsolarfsp.loca.lt",
    "Segredo": "https://oemsolarfsg.loca.lt",
}


class TrackerCache:

    def __init__(self):
        if "trackers_data" not in st.session_state:
            st.session_state.trackers_data = {}
        self.tracker_service = TrackerService(
            ApiClient(URL.get(st.session_state.get("plant")))
        )

    def get_values(self):
        for selected_tracker in st.session_state["selected_trackers"]:
            try:
                self._update_cache(selected_tracker)
            except Exception as e:
                st.error(
                    f"Erro fetching tracker {selected_tracker} historical data {e}"
                )

    def _update_cache(self, tracker_id):
        if (
            st.session_state.get("plant")
            not in st.session_state["trackers_data"].keys()
        ):
            st.session_state["trackers_data"][st.session_state.get("plant")] = {}
        tracker_data = (
            st.session_state.get("trackers_data", {})
            .get(st.session_state.get("plant", {}))
            .get(tracker_id)
        )
        if self._should_update(tracker_data):
            st.session_state["trackers_data"].get(st.session_state.get("plant"))[
                tracker_id
            ] = {
                "last_updated": datetime.datetime.now(),
                "tracker_historical_position": self.tracker_service.fetch_tracker_historical_angle(
                    tracker_id
                ),
            }

    @staticmethod
    def _should_update(tracker_data):
        return tracker_data is None or datetime.datetime.now() - tracker_data[
            "last_updated"
        ] > datetime.timedelta(minutes=1)
