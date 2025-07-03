import time
import datetime
import threading
import streamlit as st
from streamlit.runtime.scriptrunner import add_script_run_ctx


def start_background_updater(fetch_func, state_key, wait_time=5):
    if state_key not in st.session_state:
        st.session_state[state_key] = []
        error_key = f"{state_key}_error"
        update_time_key = f"{state_key}_update_time"
        st.session_state[error_key] = None
        st.session_state[update_time_key] = None

        def updater():
            while True:
                try:
                    data = fetch_func()
                    st.session_state[state_key] = data
                    st.session_state[update_time_key] = datetime.datetime.now()
                    print(f"[{datetime.datetime.now()}] [INFO] {state_key} updated")

                except Exception as e:
                    st.session_state[error_key] = str(e)
                    print(f"[{datetime.datetime.now()}] [ERROR] {state_key} - {e}")

                time.sleep(wait_time)

        thread = threading.Thread(target=updater, daemon=True)
        add_script_run_ctx(thread)
        thread.start()
