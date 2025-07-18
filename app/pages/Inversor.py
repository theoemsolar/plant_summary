import os
import sys
import logging
from dotenv import load_dotenv
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from components import InverterDashboard
from components.side_bar.side_bar import side_bar
from api.background_updater import start_background_updater
from api.services import ApiClient, AlarmService, InverterService

ENV_BASE_URL = "BASE_URL"
ALARMS_KEY = "alarms"
INVERTERS_KEY = "inverter_generation"
ALARMS_REFRESH_INTERVAL = 30
INVERTERS_REFRESH_INTERVAL = 60
DASHBOARD_REFRESH_MS = 5000
TIME_FORMAT = "%d/%m/%Y às %H:%M:%S"


class InverterPage:

    def __init__(self):
        self.alarm_service, self.inverter_service = self._init_services()

    def _init_services(self):
        client = ApiClient("https://oemsolarfsp.loca.lt")
        return AlarmService(client), InverterService(client)

    def _render_dashboard(self):
        InverterDashboard().render()

        self.print_last_inverter_collection_time()
        self.print_last_alarm_collection_time()

        st_autorefresh(interval=DASHBOARD_REFRESH_MS, key="dashboard_autorefresh")

    def run(self):

        if not st.session_state.get("authentication_status"):
            return
        side_bar()
        self._render_dashboard()

    @staticmethod
    def _validate_config() -> str:
        load_dotenv()
        base_url = os.getenv(ENV_BASE_URL)
        if not base_url:
            logging.error("Missing environment variable: %s", ENV_BASE_URL)
            sys.exit(f"Error: {ENV_BASE_URL} not set in environment.")
        return base_url

    @staticmethod
    def print_last_alarm_collection_time():
        last_alarm = (
            st.session_state.get(st.session_state.get("plant"))
            .get("alarms", None)
            .get("last_update")
        )
        if last_alarm:
            st.caption(
                f"Última coleta dos Alarmes Inversores: {last_alarm.strftime(TIME_FORMAT)}"
            )
        else:
            st.caption("Última coleta dos Alarmes Inversores: ainda não coletado.")

    @staticmethod
    def print_last_inverter_collection_time():
        last_inv = (
            st.session_state.get(st.session_state.get("plant"))
            .get("inverter_generation", {})
            .get("last_update")
        )
        if last_inv:
            st.caption(
                f"Última coleta dos valores Inversores: {last_inv.strftime(TIME_FORMAT)}"
            )
        else:
            st.caption("Última coleta dos valores Inversores: ainda não coletado.")


InverterPage().run()
