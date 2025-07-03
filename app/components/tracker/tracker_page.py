import streamlit as st
from .tracker_dashboard import TrackerDashboard
from .historical_positio.historical_position_page import HistoricalPositionPage


class TrackerPage:

    def render(self):
        dashboard, graph = st.tabs(["Dashboard", "Grafico"])
        with dashboard:
            TrackerDashboard().render()
        with graph:
            HistoricalPositionPage().render()
