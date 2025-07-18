import pathlib
import streamlit as st
from string import Template


class TrackerCard:
    BASE = pathlib.Path(__file__).parent
    CSS_PATH = BASE / "tracker_card.css"
    HTML_PATH = BASE / "tracker_card.html"

    @classmethod
    def _load_css(cls):
        css = cls.CSS_PATH.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
        cls._css_loaded = True

    def __init__(self):
        self.angle = 123
        self.tracker = 0

    def render(self, tracker, angle, alarms_emoji):
        self.angle = angle
        self.tracker = tracker

        tpl = Template(self.HTML_PATH.read_text(encoding="utf-8"))
        html = tpl.substitute(
            field_name=f"Tracker {self.tracker}",
            value=self.angle,
            alarm=alarms_emoji,
            bg_color="#064E3B" if len(alarms_emoji) == 0 else "#B91C1C",
        )
        st.markdown(html, unsafe_allow_html=True)
