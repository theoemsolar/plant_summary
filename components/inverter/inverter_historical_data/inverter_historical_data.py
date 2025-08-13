import ast
import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import timedelta
from services.sheet_service import SheetService, MONTHS
from .plots.daily_generation import DailyGeneration


class InverterHistoricalData:

    def __init__(self):
        self.sheet_service = SheetService()
        self.df: pd.DataFrame = None

    def render(self, applied_filters):
        month = self.header(applied_filters)
        self.prepare_df(applied_filters, month)
        self.alarm_history()
        col1, col2 = st.columns(2)
        with col1:
            self.generation_line()

        with col2:
            self.generation_by_day()

        DailyGeneration().plot(self.df)

    def header(self, applied_filters):
        month = st.selectbox("Selecione o mês", MONTHS)
        st.subheader(f"{month} - {applied_filters[0]} - {applied_filters[1]}")
        return month

    def prepare_df(self, applied_filters, month):
        client, plant = applied_filters
        try:
            # self.df = self.sheet_service.get_historical_data_by_client(client, month)
            # self.df.to_csv("sample.csv")
            self.df = pd.read_csv("sample.csv")
        except Exception as e:
            st.warning(f"Sem dados para o {month} em {client} - {plant}.")
            return
        self.df = self.df[self.df.plant_name == plant]

    def generation_by_day(self):
        st.write("Geração por inversor")
        st.bar_chart(self.df.groupby("inverter")["generation"].sum())

    def generation_line(self):
        st.write("Geração diária")
        self.df["generation_timestamp"] = pd.to_datetime(
            self.df["generation_timestamp"]
        )
        daily_generation = self.df.groupby(self.df["generation_timestamp"].dt.date)[
            "generation"
        ].sum()
        daily_generation.index = daily_generation.index.astype(str)
        st.line_chart(daily_generation)

    def alarm_history(self):
        segments = []
        for _, row in self.df.iterrows():
            inv = f"Inversor {row['inverter']}"

            history: dict = ast.literal_eval(row["alarm_history"])
            # cria lista de (timestamp, estado)
            events = []
            for state, times in history.items():
                for t in times:
                    ts = pd.to_datetime(t)
                    events.append((ts, state))
            # ordena cronologicamente
            events.sort(key=lambda x: x[0])
            # gera segmentos contínuos de estado
            for i, (ts, state) in enumerate(events):
                start = ts
                if i + 1 < len(events):
                    end = events[i + 1][0]
                else:
                    # último evento vai até o fim do dia
                    end = start.normalize() + timedelta(days=1)
                segments.append(
                    {"inverter": inv, "start": start, "end": end, "alarm": state}
                )

        seg_df = pd.DataFrame(segments)

        # Mapa de cores baseado na lógica específica
        unique_states = seg_df["alarm"].unique()
        color_map = {state: self.get_alarm_color(state) for state in unique_states}

        # 5) Desenha a linha do tempo: uma linha por inversor
        fig = px.timeline(
            seg_df,
            x_start="start",
            x_end="end",
            y="inverter",
            color="alarm",
            color_discrete_map=color_map,
            title="Linha do Tempo de Alarme por Inversor",
        )
        fig.update_yaxes(autorange="reversed")
        fig.update_layout(
            xaxis_title="Data e Hora",
            yaxis_title="Inversor",
            legend_title="Estado de Alarme",
            height=600,
            margin=dict(l=100, r=20, t=60, b=40),
        )

        st.plotly_chart(fig, use_container_width=True)

    def get_alarm_color(self, alarm_state):
        alarm_upper = alarm_state.upper()

        if alarm_upper in ["INICIANDO", "ESPERA"]:
            return "#D97706"
        elif alarm_upper in ["FALHA", "PARADO"]:
            return "#B91C1C"
        elif alarm_upper == "SEM COMUNICAÇÃO":
            return "#1E3A8A"
        else:
            return "#064E3B"
