import streamlit as st
from components.inverter.inverter_card.inverter import InverterCard
from datetime import datetime, timedelta
from domain.analytics import detect_outliers


class InverterDashboard:

    def __init__(self):
        self.items = 40
        self.total_columns = 8
        self._get_data()

    def _get_data(self):
        self.alarms_data = st.session_state.alarms
        self.inverter_data = st.session_state.inverters

    def render(self):
        self._get_data()
        if len(self.inverter_data) == 0 or len(self.alarms_data) == 0:
            st.warning("Sem dados de inversor")
            return
        self._grid()

    def _grid(self):
        cols = st.columns(self.total_columns)
        half = self.total_columns // 2
        rows = (self.items + self.total_columns - 1) // self.total_columns

        for row in range(rows):
            self._columns_grid(cols, half, row)

    def _columns_grid(self, cols, half, row):
        for col_idx in range(self.total_columns):
            index = row * self.total_columns + col_idx
            if index >= self.items:
                break
            self._update_values(col_idx, half, row)
            self._render_individual_card(col_idx, cols)

    def _render_individual_card(self, col_idx, cols):
        with cols[col_idx]:
            InverterCard().render(
                self.name, self.data, self.date, self.alarm, self.is_outlier
            )

    def _update_values(self, col_idx, half, row):
        self.fsp = 1 if col_idx < half else 2
        self.inverter = row * half + (col_idx % half) + 1
        self.data = self._get_inverter_data()
        self.date = self._get_inverter_date()
        self.alarm = self._get_inverter_alarm()
        self.is_outlier = self._is_outlier()
        self.name = f"{self.fsp}.{self.inverter:02d}"

    def _get_inverter_data(self):
        return [
            item["FieldValue"]
            for item in self.inverter_data
            if item["Inversor"] == f"{self.fsp}.{self.inverter:02d}"
        ][0]

    def _get_inverter_date(self):
        return (
            datetime(1899, 12, 30)
            + timedelta(
                days=[
                    item["time"]
                    for item in self.inverter_data
                    if item["Inversor"] == f"{self.fsp}.{self.inverter:02d}"
                ][0]
            )
        ).strftime("%d/%m/%Y %H:%M:%S")

    def _get_inverter_alarm(self):
        return [
            item["Message"].split()[-1]
            for item in self.alarms_data
            if item["Area"][12:] == f"FSP{self.fsp:02d}.INV{self.inverter:02d}"
        ][0]

    def _is_outlier(self):
        return self.data in detect_outliers(self.inverter_data)
