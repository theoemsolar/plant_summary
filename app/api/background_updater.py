import time
import datetime
import threading
import streamlit as st
from streamlit.runtime.scriptrunner import add_script_run_ctx


def start_background_updater(fetch_func, state_key, plant, wait_time=5):
    if plant not in st.session_state:
        st.session_state[plant] = {}
    if state_key not in st.session_state[plant].keys():
        st.session_state[plant][state_key] = {
            "data": None,
            "error": None,
            "last_update": None,
        }

        def updater():
            while True:
                try:
                    data = fetch_func()
                    st.session_state[plant][state_key]["data"] = data
                    st.session_state[plant][state_key][
                        "last_update"
                    ] = datetime.datetime.now()
                    st.session_state[plant][state_key]["error"] = None
                    print(
                        f"[{datetime.datetime.now()}] [INFO] [{plant}] [{state_key}]: updated"
                    )

                except Exception as e:
                    st.session_state[plant][state_key]["error"] = str(e)
                    print(
                        f"[{datetime.datetime.now()}] [ERROR] [{plant}]  [{state_key}]:  {e}"
                    )

                time.sleep(wait_time)

        thread = threading.Thread(target=updater, daemon=True)
        add_script_run_ctx(thread)
        thread.start()
