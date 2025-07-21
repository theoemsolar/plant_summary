import os
import sys
import logging
from dotenv import load_dotenv
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from api.services import ApiClient, TrackerService
from api.background_updater import start_background_updater
from components import HistoricalPositionPage, TrackerDashboard
from components.side_bar.side_bar import side_bar

ENV_BASE_URL = "BASE_URL"
TRACKERS_KEY = "trackers_angles"
TRACKERS_ALARMS_KEY = "trackers_alarms"
TRACKERS_DATA_INTERVAL = 60
TRACKERS_ALARM_INTERVAL = 30
PAGE_REFRESH_MS = 5000
TIME_FORMAT = "%d/%m/%Y às %H:%M:%S"


class TrackerApp:

    def __init__(self):
        self.base_url = self._validate_config()
        self.tracker_service = self._init_service()

    def _init_service(self) -> TrackerService:
        client = ApiClient(self.base_url)
        return TrackerService(client)

    def _render_page(self):
        tabs = st.tabs(["Dashboard", "Gráfico"])
        with tabs[0]:
            TrackerDashboard().render()
        with tabs[1]:
            HistoricalPositionPage().render()

        self.print_last_tracker_collection_time()
        self.print_last_alarm_collection_time()

        st_autorefresh(interval=PAGE_REFRESH_MS, key="tracker_autorefresh")

    def run(self):
        if not st.session_state.get("authentication_status"):
            return
        side_bar()
        if (
            st.session_state.get(st.session_state.get("plant"))
            .get(TRACKERS_ALARMS_KEY, {})
            .get("data", None)
            is None
            or st.session_state.get(st.session_state.get("plant"))
            .get(TRACKERS_KEY, {})
            .get("data", None)
            is None
        ):
            st.warning(
                f"Sem valores para tracker em {st.session_state.get('plant')}. Por favor, aguarde a coleta dos dados."
            )
            return
        self._render_page()

    @staticmethod
    def print_last_alarm_collection_time():
        last_alarms = (
            st.session_state.get(st.session_state.get("plant"), {})
            .get("trackers_alarms", {})
            .get("last_update", None)
        )

        if last_alarms:
            st.caption(
                f"Última coleta dos Alarmes Tracker: {last_alarms.strftime(TIME_FORMAT)}"
            )
        else:
            st.caption("Última coleta dos Alarmes Tracker: ainda não coletado.")

    @staticmethod
    def print_last_tracker_collection_time():
        last_trackers = (
            st.session_state.get(st.session_state.get("plant"), {})
            .get("trackers_angles", {})
            .get("last_update", None)
        )

        if last_trackers:
            st.caption(
                f"Última coleta dos valores Tracker: {last_trackers.strftime(TIME_FORMAT)}"
            )
        else:
            st.caption("Última coleta dos valores Tracker: ainda não coletado.")

    @staticmethod
    def _validate_config() -> str:
        load_dotenv()
        base_url = "https://oemsolarfsp.loca.lt"
        if not base_url:
            logging.error("Missing environment variable: %s", ENV_BASE_URL)
            sys.exit(f"Error: {ENV_BASE_URL} not set in environment.")
        return base_url


if __name__ == "__main__":
    TrackerApp().run()
