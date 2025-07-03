import datetime
import pandas as pd
import streamlit as st
from .filter import Filter
import plotly.express as px
from .tracker_cache import TrackerCache


class HistoricalPositionPage:

    def __init__(self):
        self.filter = Filter()
        self.tracker_cache = TrackerCache()

    def render(self):
        self.filter.filter_widget()
        self.tracker_cache.get_values()
        self._plot()

    def _plot(self):
        if not self._exist_tracker_selected():
            return
        dados_plot = self._create_plot_df()
        self._plot_line_chart(dados_plot)

    def _exist_tracker_selected(self):
        if len(st.session_state.selected_trackers) != 0:
            return True
        st.warning("Nenhum tracker selecionado.")

    def _create_plot_df(self):
        dados_plot = []
        for tracker, tracker_data in st.session_state.trackers_data.items():
            if self.is_tracker_selected(tracker):
                continue
            for line in tracker_data["tracker_historical_position"]:
                dados_plot.append(
                    {
                        "Tracker": tracker,
                        "Tempo": datetime.datetime(1899, 12, 30)
                        + datetime.timedelta(days=line["E3TimeStamp"]),
                        "Angulo": line["FieldValue"],
                    }
                )

        return pd.DataFrame(dados_plot)

    def is_tracker_selected(self, tracker):
        return tracker not in st.session_state.selected_trackers

    def _plot_line_chart(self, df_plot):
        fig = px.line(df_plot, x="Tempo", y="Angulo", color="Tracker")
        st.plotly_chart(fig)
