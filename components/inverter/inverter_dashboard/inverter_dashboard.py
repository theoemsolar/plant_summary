import pandas as pd
import streamlit as st
from utils import FilterDataFrame
from components.inverter.inverter_card import InverterCard


class InverterDahsboard:
    NUMBER_OF_COLUMNS = 5

    def render(self, last_data: pd.DataFrame):
        self.last_data = last_data
        self.prepare_dataframe()
        self.grid()

    def grid(self):
        columns = st.columns(self.NUMBER_OF_COLUMNS)
        for index, row in self.last_data.iterrows():
            with columns[index % self.NUMBER_OF_COLUMNS]:
                InverterCard().render(
                    row["inverter"],
                    row["generation"],
                    row["generation_timestamp"],
                    row["alarm"].split()[-1],
                    False,
                )

    def prepare_dataframe(self):
        self.last_data.sort_values(by="inverter", inplace=True)
        self.last_data.reset_index(drop=True, inplace=True)
