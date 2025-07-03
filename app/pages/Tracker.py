import datetime
import os
import streamlit as st
from dotenv import load_dotenv
from streamlit_autorefresh import st_autorefresh
from api.services import ApiClient, TrackerService
from components.tracker.tracker_page import TrackerPage
from api.backgorund_updater import start_background_updater


load_dotenv()
BASE_URL = os.getenv("BASE_URL")

api_client = ApiClient(BASE_URL)
tracker_service = TrackerService(api_client)
WAIT_TIME = 5

start_background_updater(
    tracker_service.fetch_all_tracker_last_angle, "trackers", wait_time=300
)
start_background_updater(
    tracker_service.fetch_trackers_alarm, "trackers_alarms", wait_time=30
)


TrackerPage().render()

st_autorefresh(interval=5000, key="dashboard_autorefresh")

st.caption(
    f"Última coleta dos valores Tracker: {st.session_state.trackers_update_time.strftime("%d/%m/%Y às %H:%M:%S")}"
)
st.caption(
    f"Última coleta dos Alarmes Tracker: {st.session_state.trackers_alarms_update_time.strftime("%d/%m/%Y às %H:%M:%S")}"
)
