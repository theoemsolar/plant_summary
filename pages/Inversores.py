import streamlit as st
from utils import FilterDataFrame
from components.inverter.inverter_dashboard.inverter_dashboard import InverterDahsboard
from components.inverter.inverter_historical_data.inverter_historical_data import (
    InverterHistoricalData,
)


class InverterPage:

    def render(self):
        self.last_data, self.applied_filters = self.filter()
        self.tabs()

    def tabs(self):
        tab1, tab2 = st.tabs(["Inversores", "Histórico"])
        with tab1:
            InverterDahsboard().render(self.last_data)

        with tab2:
            InverterHistoricalData().render(self.applied_filters)

    def filter(self):
        df = st.session_state.get("day_data")
        plant_dataframe, applied_filters = FilterDataFrame.filter_df(
            df, return_filter=True
        )
        last_data = FilterDataFrame.filter_df_last_data_per_inverter(
            plant_dataframe, "generation"
        )
        return last_data, applied_filters


if __name__ == "__main__":
    InverterPage().render()
