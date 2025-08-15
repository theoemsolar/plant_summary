import streamlit as st
from dotenv import load_dotenv
from streamlit_autorefresh import st_autorefresh
from utils.background_updater import start_background_updater


load_dotenv()
st.set_page_config(layout="wide")
REFRESH_TIME = 60000

start_background_updater()
if st.session_state["day_data"] is None:
    st.warning("Coletando dados, aguarde...")
    st_autorefresh(interval=2000)
    print("Tentativa de atualização dos dados")
    st.stop()

if __name__ == "__main__":
    from components.home_page.home_page import home_dashboard

    home_dashboard()
    st.caption(
        f'Ultima atualização: {st.session_state.get("last_update").strftime("%d/%m/%Y %H:%M:%S")}'
    )

    st_autorefresh(interval=REFRESH_TIME)
