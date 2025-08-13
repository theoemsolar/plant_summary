import ast
import pandas as pd
import streamlit as st
import plotly.express as px


class DailyGeneration:

    def plot(self, df):
        self.df = df
        self.df["generation_timestamp"] = pd.to_datetime(
            self.df["generation_timestamp"]
        )
        self.filter()
        self.plot_daily_generation()

    def filter(self):
        col1, col2 = st.columns(2)
        with col1:
            day = self.day_filter()
        with col2:
            inverter = self.inverter_filter()
        self.df = self.df[
            (self.df["generation_timestamp"].dt.day == day)
            & (self.df["inverter"] == inverter)
        ]

    def day_filter(self):
        days = self.df["generation_timestamp"].dt.day.unique()
        days.sort()
        day = st.selectbox("Dia", days)
        return day

    def inverter_filter(self):
        inverters = self.df["inverter"].unique()
        inverters.sort()
        inverter = st.selectbox("Inversor", inverters)
        return inverter

    def get_daily_generation_df(self):
        generation_dict = ast.literal_eval(self.df["generation_history"].iloc[0])
        df_from_dict = pd.DataFrame(
            list(generation_dict.items()),
            columns=["Tempo", "Geração"],
        )
        return df_from_dict

    def plot_daily_generation(self):
        df = self.get_daily_generation_df()
        fig = px.line(df, x="Tempo", y="Geração", title="Geração Diária")
        st.plotly_chart(fig)
