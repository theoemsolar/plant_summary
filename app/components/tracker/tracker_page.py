import streamlit as st
from .historical_position_plot import HistoricalPosition
from .tracker_dashboard import TrackerDashboard


class TrackerPage:

    def render(self):
        dashboard, graph = st.tabs(["Dashboard", "Grafico"])
        with dashboard:
            TrackerDashboard().render()
        with graph:
            HistoricalPosition().render()
