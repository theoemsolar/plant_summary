import streamlit as st


class FilterDataFrame:

    @staticmethod
    def filter_df(df, return_filter=False):
        if return_filter:
            df_filtered_by_client, client = FilterDataFrame.filter_df_by_client(
                df, return_client_name=True
            )
            plant_dataframe, plant = FilterDataFrame.filter_df_by_plant(
                df_filtered_by_client, return_plant_name=True
            )
            return plant_dataframe, (client, plant)

        df_filtered_by_client = FilterDataFrame.filter_df_by_client(df)
        plant_dataframe = FilterDataFrame.filter_df_by_plant(df_filtered_by_client)
        return plant_dataframe

    @staticmethod
    def filter_df_by_plant(df_filtered_by_client, return_plant_name=False):
        plant = st.radio(
            "Selecione uma planta",
            df_filtered_by_client.plant_name.unique(),
            horizontal=True,
        )
        plant_dataframe = df_filtered_by_client[
            df_filtered_by_client.plant_name == plant
        ]
        if return_plant_name:
            return plant_dataframe, plant
        return plant_dataframe

    @staticmethod
    def filter_df_by_client(df, return_client_name=False):
        client = st.selectbox("Selecione um cliente", df.client.unique())
        df_filtered_by_client = df[df.client == client]
        if return_client_name:
            return df_filtered_by_client, client
        return df_filtered_by_client

    @staticmethod
    def filter_df_last_data_per_inverter(df, timestamp_col):
        df_sorted = df.sort_values(by=f"{timestamp_col}_timestamp", ascending=False)
        df_latest = df_sorted.drop_duplicates(subset="inverter", keep="first")
        return df_latest
