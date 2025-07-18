import streamlit as st
from components import InverterCard
from datetime import datetime, timedelta
from domain.analytics import detect_outliers


class InverterDashboard:

    def __init__(self, total_columns=8):
        self.total_columns = total_columns
        self.inverter_groups = {}
        self.items = 0
        self._get_data()
        self._process_inverter_data()

    def _get_data(self):
        self.alarms_data = (
            st.session_state.get(st.session_state["plant"])
            .get("alarms", {})
            .get("data")
        )
        self.inverter_data = (
            st.session_state.get(st.session_state["plant"])
            .get("inverter_generation", {})
            .get("data")
        )

    def _process_inverter_data(self):
        if self.inverter_data is None:
            return

        self.inverter_groups = {}

        for item in self.inverter_data:
            inverter_name = item["inverter"]
            fsp_number = int(inverter_name.split(".")[0])

            if fsp_number not in self.inverter_groups:
                self.inverter_groups[fsp_number] = []

            if inverter_name not in self.inverter_groups[fsp_number]:
                self.inverter_groups[fsp_number].append(inverter_name)

        for fsp in self.inverter_groups:
            self.inverter_groups[fsp].sort()

        self.items = sum(len(inverters) for inverters in self.inverter_groups.values())

    def render(self):
        self._get_data()
        self._process_inverter_data()
        if self.inverter_data is None or self.alarms_data is None:
            st.warning("Sem dados de inversor. Por favor, aguarde a coleta dos dados.")
            return
        self._grid()

    def _grid(self):
        if self.items == 0:
            st.warning("Nenhum inversor encontrado nos dados.")
            return

        cols = st.columns(self.total_columns)
        rows = (self.items + self.total_columns - 1) // self.total_columns

        for row in range(rows):
            self._columns_grid(cols, row)

    def _columns_grid(self, cols, row):
        for col_idx in range(self.total_columns):
            index = row * self.total_columns + col_idx
            if index >= self.items:
                break

            inverter_name = self._get_inverter_name_by_index(index)
            if inverter_name:
                self._update_values(inverter_name)
                self._render_individual_card(col_idx, cols)

    def _get_inverter_name_by_index(self, index):
        current_index = 0

        for fsp in sorted(self.inverter_groups.keys()):
            fsp_inverters = self.inverter_groups[fsp]
            if current_index + len(fsp_inverters) > index:
                return fsp_inverters[index - current_index]
            current_index += len(fsp_inverters)

        return None

    def _render_individual_card(self, col_idx, cols):
        with cols[col_idx]:
            InverterCard().render(
                self.name, self.data, self.date, self.alarm, self.is_outlier
            )

    def _update_values(self, inverter_name):
        self.name = inverter_name
        parts = inverter_name.split(".")
        self.fsp = int(parts[0])
        self.inverter = int(parts[1])

        self.data = self._get_inverter_data()
        self.date = self._get_inverter_date()
        self.alarm = self._get_inverter_alarm()
        self.is_outlier = self._is_outlier()

    def _get_inverter_data(self):
        return (
            [
                item["value"]
                for item in self.inverter_data
                if item["inverter"] == self.name
            ][0]
            if self.inverter_data
            else None
        )

    def _get_inverter_date(self):
        return "TODO: Implement date retrieval logic here"
        # return (
        #     datetime(1899, 12, 30)
        #     + timedelta(
        #         days=[
        #             item["timestamp"]
        #             for item in self.inverter_data
        #             if item["inverter"] == self.name
        #         ][0]
        #     )
        # ).strftime("%d/%m/%Y %H:%M:%S")

    def _get_inverter_alarm(self):
        try:
            return [
                item["Message"].split()[-1]
                for item in self.alarms_data
                if item["Area"][12:] == f"FSP{self.fsp:02d}.INV{self.inverter:02d}"
            ][0]
        except (IndexError, KeyError):
            return "OK"

    def _is_outlier(self):
        if self.data is None:
            return False
        return self.data in detect_outliers(self.inverter_data)

    def get_dashboard_summary(self):
        """Retorna um resumo da configuração atual do dashboard"""
        summary = {
            "total_inversores": self.items,
            "grupos": {},
            "total_colunas": self.total_columns,
        }

        for fsp, inverters in self.inverter_groups.items():
            summary["grupos"][f"FSP{fsp:02d}"] = len(inverters)

        return summary
