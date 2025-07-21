import streamlit as st
import streamlit_authenticator as stauth
from api.background_updater import start_background_updater
from api.services import ApiClient, TrackerService, AlarmService, InverterService

st.set_page_config(layout="wide")

config = {
    "credentials": dict(st.secrets.get("credentials", {})),
    "cookie": dict(st.secrets.get("cookie", {})),
    "api_urls": dict(st.secrets.get("api_urls", {}))
}

# Converter usernames nested dict
if "credentials" in config and "usernames" in config["credentials"]:
    config["credentials"]["usernames"] = {
        username: dict(user_data)
        for username, user_data in config["credentials"]["usernames"].items()
    }

authenticator = stauth.Authenticate(
    config.get("credentials", {}),
    config.get("cookie", {}).get("name", ""),
    config.get("cookie", {}).get("key", ""),
    config.get("cookie", {}).get("expiry_days", 30),
)

segredo_endpoint = config.get("api_urls", {}).get("segredo", "")
santo_antonio_endpoint = config.get("api_urls", {}).get("santo_antonio", "")

try:
    authenticator.login()
except Exception as e:
    st.error(e)

if st.session_state.get("authentication_status"):
    authenticator.logout()
    st.write(f'Welcome *{st.session_state.get("name")}*')
    start_background_updater(
        TrackerService(
            ApiClient("https://oemsolarfsp.loca.lt")
        ).fetch_all_tracker_last_angle,
        "trackers_angles",
        "Santo Antonio",
        wait_time=30,
    )
    start_background_updater(
        AlarmService(ApiClient(santo_antonio_endpoint)).fetch_all_last_alarms,
        "alarms",
        "Santo Antonio",
        wait_time=30,
    )

    start_background_updater(
        InverterService(
            ApiClient(santo_antonio_endpoint)
        ).get_all_inverters_last_data,
        "inverter_generation",
        "Santo Antonio",
        wait_time=30,
    )

    start_background_updater(
        TrackerService(ApiClient(santo_antonio_endpoint)).fetch_trackers_alarm,
        "trackers_alarms",
        "Santo Antonio",
        wait_time=30,
    )

    start_background_updater(
        TrackerService(
            ApiClient(segredo_endpoint)
        ).fetch_all_tracker_last_angle,
        "trackers_angles",
        "Segredo",
        wait_time=30,
    )
    start_background_updater(
        AlarmService(ApiClient(segredo_endpoint)).fetch_all_last_alarms,
        "alarms",
        "Segredo",
        wait_time=30,
    )

    start_background_updater(
        InverterService(
            ApiClient(segredo_endpoint)
        ).get_all_inverters_last_data,
        "inverter_generation",
        "Segredo",
        wait_time=30,
    )

    start_background_updater(
        TrackerService(ApiClient(segredo_endpoint)).fetch_trackers_alarm,
        "trackers_alarms",
        "Segredo",
        wait_time=30,
    )

elif st.session_state.get("authentication_status") is False:
    st.error("Username/password is incorrect")
elif st.session_state.get("authentication_status") is None:
    st.warning("Please enter your username and password")

if not st.session_state.get("authentication_status"):
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] { display: none; }
            .block-container { padding-left: 1rem; padding-right: 1rem; }
        </style>
    """,
        unsafe_allow_html=True,
    )
