import datetime
import os
import streamlit as st
from dotenv import load_dotenv
from components import InverterDashboard
from streamlit_autorefresh import st_autorefresh
from api.backgorund_updater import start_background_updater
from api.services import ApiClient, AlarmService, InverterService

load_dotenv()
BASE_URL = os.getenv("BASE_URL")


api_client = ApiClient(BASE_URL)
alarm_service = AlarmService(api_client)
inverter_service = InverterService(api_client)

start_background_updater(alarm_service.fetch_all_last_alarms, "alarms", wait_time=30)
start_background_updater(
    inverter_service.get_all_inverters_last_data, "inverters", wait_time=60
)

InverterDashboard().render()

st.caption(
    f"Última coleta dos valores Inversores: {st.session_state.inverters_update_time.strftime("%d/%m/%Y às %H:%M:%S")}"
)
st.caption(
    f"Última coleta dos Alarmes Inversores: {st.session_state.alarms_update_time.strftime("%d/%m/%Y às %H:%M:%S")}"
)

st_autorefresh(interval=5000, key="dashboard_autorefresh")
