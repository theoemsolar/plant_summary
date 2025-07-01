import streamlit as st

# from components.tracker.mock import trackers_positions


class TrackerDashboard:

    def render(self):
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
            st.metric(
                f"tracker {tracker['UTC']}",
                f"{tracker['FieldValue']:.2f} °",
            )
