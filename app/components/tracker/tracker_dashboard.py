import streamlit as st
from .tracker_card.tracker_card import TrackerCard
from components.tracker.mock import tracker_alarms


class TrackerDashboard:

    def render(self):
        TrackerCard()._load_css()

        NUMBER_OF_COLUMNS = 10
        NUMBER_OF_TRACKERS_PER_COLUMN = 8
        columns = st.columns(NUMBER_OF_COLUMNS)
        prev = 0
        self._generate_grid(NUMBER_OF_TRACKERS_PER_COLUMN, columns, prev)

    def _generate_grid(self, NUMBER_OF_TRACKERS_PER_COLUMN, columns, prev):
        for index, column in enumerate(columns):
            with column:
                self._generate_column(NUMBER_OF_TRACKERS_PER_COLUMN, prev)
                prev += NUMBER_OF_TRACKERS_PER_COLUMN

    def _generate_column(self, NUMBER_OF_TRACKERS_PER_COLUMN, prev):
        for tracker in st.session_state["trackers"][
            prev : prev + NUMBER_OF_TRACKERS_PER_COLUMN
        ]:
            TrackerCard().render(
                tracker["UTC"],
                f"{tracker['FieldValue']:.2f}",
                self._get_emoji(tracker["UTC"]),
            )

    @staticmethod
    def _get_alarm(tracker):
        return [
            tracker_data["Message"].split()[-1]
            for tracker_data in st.session_state.trackers_alarms
            if tracker_data["TCU"] == f"TCU{tracker}"
        ]

    def _get_emoji(self, tracker):
        alarms = self._get_alarm(tracker)

        emoji_string = ""
        if "COMUNICAÇÃO" in alarms:
            emoji_string += "📡 "

        if "SISTEMA" in alarms:
            emoji_string += "🖥️ "

        if "BACKTRACKING" in alarms:
            emoji_string += "🔄 "

        if "BATERIA" in alarms:
            emoji_string += "🔋 "
        return emoji_string
