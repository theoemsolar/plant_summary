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
        self.value = None
        self.date = datetime.now()

    def render(self, inverter, data, date, alarm, is_outlier):
        self.data = data
        self.date = date
        self.alarm = alarm
        self.inverter = inverter
        self._load_css()
        alert_icon = " ⚠️" if is_outlier else ""

        # Normaliza o valor do alarme para evitar problemas de caixa e espaços
        alarm_normalized = str(alarm).strip().upper()
        # Estados que NÃO são verdes
        normal_states = ["OPERANDO", "NORMAL", "ONLINE", "LIGADO", "ON"]
        is_normal = (
            alarm_normalized in normal_states or self._get_color(alarm) == "#064E3B"
        )
        alert_class = "" if is_normal else " inverter-card--alert"

        tpl = Template(self.HTML_PATH.read_text(encoding="utf-8"))
        html = tpl.substitute(
            field_name=f"{self.inverter}",
            alert_icon=alert_icon,
            value=self.data,
            date=self.date,
            bg_color=self._get_color(self.alarm),
            alert_class=alert_class,
        )
        st.markdown(html, unsafe_allow_html=True)

    def _get_color(self, alert):
        if alert == "INICIANDO" or alert == "ESPERA":
            return "#D97706"
        elif alert == "FALHA" or alert == "PARADO":
            return "#B91C1C"
        elif alert == "COMUNICAÇÃO":
            return "#1E3A8A"
        elif alert == "FETCH":
            return "#6B7280"
        else:
            return "#064E3B"
