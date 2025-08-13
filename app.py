import datetime

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from streamlit_autorefresh import st_autorefresh
from services import SheetService, SPREAD_SHEET_IDS


load_dotenv()
st.set_page_config(layout="wide")


@st.cache_data(ttl=300)
def get_data():
    df_list = []
    for client in SPREAD_SHEET_IDS.keys():
        df_list.append(SheetService().get_daily_data_by_client(client))

    print(f"[{datetime.datetime.now()}][INFO] Data fetched")
    return pd.concat(df_list, axis=0, ignore_index=True)


if "day_data" not in st.session_state:
    st.session_state["day_data"] = get_data()


if __name__ == "__main__":
    from components.home_page.home_page import home_dashboard

    for row in st.session_state["day_data"].itertuples():
        if type(row[5]) == str:
            st.write(row)

    home_dashboard()
    st.caption(
        f'Ultima atualização: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}'
    )
