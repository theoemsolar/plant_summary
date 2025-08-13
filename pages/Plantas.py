import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from utils import read_sheet_to_dataframe
from components.plants.map.map import PlantMap

SPREADSHEET_ID = "1NYvgvdHIAvaNXbRe_PQHs9z9tXaabBk14RVSFqSN-nY"
WORKSHEET_NAME = "PWP_Details"


@st.cache_data
def load_data():
    return read_sheet_to_dataframe(SPREADSHEET_ID, WORKSHEET_NAME)


class PlantsDashboard:
    def __init__(self):
        self.df = load_data()

    def render(self):
        if self.df is not None:
            PlantMap().render(self.df)
        else:
            st.error("Não foi possível carregar os dados das plantas.")


PlantsDashboard().render()
