import pathlib
import streamlit as st
from string import Template
from datetime import datetime


class InverterCard:
    BASE = pathlib.Path(__file__).parent
    CSS_PATH = BASE / "inverter.css"
    HTML_PATH = BASE / "inverter.html"

    @classmethod
    def _load_css(cls):
        css = cls.CSS_PATH.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
        cls._css_loaded = True

    def __init__(self):
        self.value = 123
        self.date = datetime.now()
        self.fsp_number = 0
        self.inverter_number = 0

    def render(self, inverter, data, date, alarm, is_outlier):
        self.data = data
        self.date = date
        self.alarm = alarm
        self.inverter = inverter
        self._load_css()
        alert_icon = " ⚠️" if is_outlier else ""

        tpl = Template(self.HTML_PATH.read_text(encoding="utf-8"))
        html = tpl.substitute(
            field_name=f"Inversor {self.inverter}",
            alert_icon=alert_icon,
            value=self.data,
            date=self.date,
            bg_color=self._get_color(self.alarm),
        )
        st.markdown(html, unsafe_allow_html=True)

    def _get_color(self, alert):
        if alert == "INICIANDO" or alert == "ESPERA":
            return "#D97706"
        elif alert == "FALHA" or alert == "PARADO":
            return "#B91C1C"
        elif alert == "COMUNICAÇÃO":
            return "#1E3A8A"
        else:
            return "#064E3B"
