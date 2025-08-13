import os
import datetime
import pandas as pd
import streamlit as st
import plotly.express as px
from dotenv import load_dotenv
from utils import read_sheet_to_dataframe

load_dotenv()
DATA_SPREADSHEET_ID = os.getenv("DATA_SPREADSHEET_ID")

MONTHS = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Março",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro",
}


@st.cache_data
def load_data():
    month = datetime.datetime.today().month
    month_name = MONTHS[month]
    df = read_sheet_to_dataframe(DATA_SPREADSHEET_ID, month_name)
    df["generation_timestamp"] = pd.to_datetime(df["generation_timestamp"])
    return df


class Summary:
    def __init__(self):
        self.df = load_data()

    def render(self):
        self.header()
        self.generation_by_day()

    def header(self):
        st.title(MONTHS.get(datetime.datetime.today().month))
        st.caption(f"1 - {datetime.datetime.today().day}")

    def generation_by_day(self):
        daily_generation = (
            self.df.groupby(self.df["generation_timestamp"].dt.date)["generation"]
            .sum()
            .reset_index()
        )
        daily_generation.columns = ["Data", "Geração"]
        fig = px.line(
            daily_generation,
            x="Data",
            y="Geração",
            title="Geração Total Diária",
            labels={"Geração Total": "Geração (kWh)", "Data": "Data"},
        )
        fig.update_layout(
            xaxis_title="Data", yaxis_title="Geração (kWh)", hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)


Summary().render()
