import streamlit as st

if "selected_trackers" not in st.session_state:
    st.session_state["selected_trackers"] = []


class Filter:
    NUMBER_OF_COLUMNS = 10
    NUMBER_OF_TRACKERS = 80

    def __init__(self):
        self.trackers_per_column = self._calculate_trackers_per_column()
        self.selected_trackers = []

    def filter_widget(self):
        current_plant = st.session_state.get("plant")
        previous_plant = st.session_state.get("_previous_plant")
        if previous_plant != current_plant:
            self.selected_trackers = []
            st.session_state["selected_trackers"] = []
        st.session_state["_previous_plant"] = current_plant

        trackers_per_column = self._calculate_trackers_per_column()
        columns = st.columns(self.NUMBER_OF_COLUMNS)
        for column_index, column in enumerate(columns):
            self._filter_column(column, column_index, trackers_per_column)

        self._update_cache()

    def _calculate_trackers_per_column(self):
        return int(self._get_number_of_trackers() / self.NUMBER_OF_COLUMNS)

    def _filter_column(self, column, column_index, trackers_per_column):
        with column:
            for tracker in range(trackers_per_column):
                tracker_index = self._calculate_tracker_index(column_index, tracker)
                self._checkbox(tracker_index)

    def _update_cache(self):
        st.session_state["selected_trackers"] = self.selected_trackers

    def _calculate_tracker_index(self, column_index, tracker):
        return (tracker + 1) + (self.trackers_per_column * column_index)

    def _checkbox(self, tracker_index):
        if st.checkbox(f"Tracker {tracker_index}"):
            self.selected_trackers.append(tracker_index)

    def _get_number_of_trackers(self):
        return len(
            (
                st.session_state.get(st.session_state.get("plant"))
                .get("trackers_angles")
                .get("data")
            )
        )
