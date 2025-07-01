import os
import time
import threading
import datetime

import streamlit as st
from dotenv import load_dotenv
from streamlit.runtime.scriptrunner import add_script_run_ctx

from domain.analytics import detect_outliers
from streamlit_autorefresh import st_autorefresh
from components.tracker.tracker_page import TrackerPage
from components.inverter_card.inverter import InverterCard
from components.tracker.tracker_dashboard import TrackerDashboard
from components.inverter_dashboard.inverter_dashboard import InverterDashboard
from api.services import ApiClient, AlarmService, InverterService, TrackerService

st.set_page_config(layout="wide")

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

# st_autorefresh(interval=10_000, key="dashboard_autorefresh")

api_client = ApiClient(BASE_URL)
alarm_service = AlarmService(api_client)
tracker_service = TrackerService(api_client)
inverter_service = InverterService(api_client)

if "alarm_thread_started" not in st.session_state:
    st.session_state["alarm_thread_started"] = True
    st.session_state["alarms"] = []
    st.session_state["inverters"] = []
    st.session_state["trackers"] = []
    st.session_state["historical_tracker_position"] = {}
    st.session_state["last_update"] = None

    def fetch_alarms_periodically():
        while True:
            try:
                alarm_data = alarm_service.fetch_all_last_alarms()
                st.session_state["alarms"] = alarm_data

            except Exception as e:
                st.session_state["alarms_error"] = str(e)

            try:
                inverter_date = inverter_service.get_all_inverters_last_data()
                st.session_state["inverters"] = inverter_date

            except Exception as e:
                st.session_state["inverter_error"] = str(e)

            try:
                tracker_data = tracker_service.fetch_all_tracker_last_angle()
                st.session_state["trackers"] = tracker_data

            except Exception as e:
                st.session_state["tracker_error"] = str(e)

            st.session_state["last_update"] = datetime.datetime.now()
            print("updated")
            time.sleep(60)

    thread = threading.Thread(target=fetch_alarms_periodically, daemon=True)
    add_script_run_ctx(thread)
    thread.start()

# InverterDashboard(alarm_service, inverter_service).render()
