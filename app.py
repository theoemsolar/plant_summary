import datetime
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from utils import read_sheet_to_dataframe
from streamlit_autorefresh import st_autorefresh
from services import SheetService, SPREAD_SHEET_IDS


load_dotenv()
st.set_page_config(layout="wide")

WORKSHEET_NAME = "PWP_Details"
WORKSHEET_NAME_GENERAL_DATA = "Resumo"
SPREADSHEET_ID = "1NYvgvdHIAvaNXbRe_PQHs9z9tXaabBk14RVSFqSN-nY"
DADOS_DAS_USINAS_SPREADSHEET_ID = "1_KoK1ll3t0b8fDd5V75-KMrRg5tiSTG8cqd6Ebn_Mss"


# @st.cache_data(ttl=300)
def get_data():
    df_list = []
    for client in SPREAD_SHEET_IDS.keys():
        df_list.append(SheetService().get_daily_data_by_client(client))

    df = pd.concat(df_list, axis=0, ignore_index=True)
    general_data_df = st.session_state["general_data"]
    for plant in df.plant_name.unique():
        client = general_data_df[general_data_df["Usina"] == plant]["Cliente"].values[0]
        df.loc[df["plant_name"] == plant, "client"] = client

    print(f"[{datetime.datetime.now()}][INFO] Data fetched")
    if "day_data" not in st.session_state:
        st.session_state["day_data"] = df


def get_plants_data():
    if "plants_details" not in st.session_state:
        st.session_state["plants_details"] = read_sheet_to_dataframe(
            SPREADSHEET_ID, WORKSHEET_NAME
        )
        print(f"[{datetime.datetime.now()}][INFO] Plants details fetched")


def get_general_data():
    if "general_data" not in st.session_state:
        st.session_state["general_data"] = read_sheet_to_dataframe(
            DADOS_DAS_USINAS_SPREADSHEET_ID, WORKSHEET_NAME_GENERAL_DATA
        )
        print(f"[{datetime.datetime.now()}][INFO] General data fetched")


get_plants_data()
get_general_data()
get_data()


if __name__ == "__main__":
    from components.home_page.home_page import home_dashboard

    for row in st.session_state["day_data"].itertuples():
        if type(row[5]) == str:
            st.write(row)

    home_dashboard()
    st.caption(
        f'Ultima atualização: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}'
    )
