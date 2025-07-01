import os
import datetime
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
import plotly.express as px
from .mock import tracker_historical_position
from api.services import ApiClient, TrackerService

load_dotenv()
BASE_URL = os.getenv("BASE_URL")


if "historical_tracker_position" not in st.session_state:
    st.session_state["historical_tracker_position"] = {}


api_client = ApiClient(BASE_URL)
tracker_service = TrackerService(api_client)


class HistoricalPosition:

    def render(self):
        df = pd.DataFrame(tracker_historical_position)
        df["E3TimeStamp"] = pd.to_datetime(
            df["E3TimeStamp"], unit="D", origin="1899-12-30"
        )
        self._filter()
        self._get_data()
        self._plot()

    def _filter(self):
        number_of_columns = 10
        columns = st.columns(number_of_columns)
        for tracker in range(80):
            with columns[tracker % number_of_columns]:
                if (
                    st.checkbox(f"Tra.{tracker+1:02d}")
                    and tracker + 1
                    not in st.session_state["historical_tracker_position"].keys()
                ):
                    st.session_state["historical_tracker_position"][
                        f"Tracker {tracker + 1}"
                    ] = (
                        None,
                        datetime.datetime.now(),
                    )

    def _get_data(self):
        for tracker, data in st.session_state["historical_tracker_position"].items():
            if data[0] is None or datetime.datetime.now() - data[
                1
            ] > datetime.timedelta(minutes=5):
                st.write(tracker, "toca", datetime.datetime.now() - data[1])
                st.session_state["historical_tracker_position"][tracker] = (
                    tracker_service.fetch_tracker_historical_angle(
                        tracker.split("Tracker")[-1]
                    ),
                    datetime.datetime.now(),
                )
            else:
                st.write(tracker, "ok", datetime.datetime.now() - data[1])

    @staticmethod
    def _plot():
        base_date = datetime.datetime(1899, 12, 30)
        df = []
        for tracker, registros in st.session_state[
            "historical_tracker_position"
        ].items():
            for register in registros[0]:
                df.append(
                    {
                        "Tracker": tracker,
                        "Tempo": base_date
                        + datetime.timedelta(days=register["E3TimeStamp"]),
                        "Angulo": register["FieldValue"],
                    }
                )

        fig = px.line(df, x="Tempo", y="Angulo", color="Tracker")
        st.plotly_chart(fig)
