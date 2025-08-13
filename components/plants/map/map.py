import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.express as px


class PlantMap:

    def render(self, df):
        self.prepare_df(df)
        self.apply_filters()
        self.map()
        self.stats()

    def prepare_df(self, df):
        self.df = df.copy()
        coords_split = df["Coordenadas(lat, lon)"].str.split(",", expand=True)
        self.df["Latitude"] = pd.to_numeric(
            coords_split[0].str.strip(), errors="coerce"
        )
        self.df["Longitude"] = pd.to_numeric(
            coords_split[1].str.strip(), errors="coerce"
        )

    def apply_filters(self):
        st.sidebar.header("🔍 Filtros")

        # Filtro por Shareholder
        shareholders = ["Todos"] + sorted(
            self.df["Shareholder"].dropna().unique().tolist()
        )
        selected_shareholder = st.sidebar.selectbox("Cliente:", shareholders)

        # Filtro por Cluster
        clusters = ["Todos"] + sorted(self.df["Cluster"].dropna().unique().tolist())
        selected_cluster = st.sidebar.selectbox("Cluster:", clusters)

        # Filtro por Nome
        st.sidebar.subheader("Nome da Planta:")
        search_name = st.sidebar.text_input(
            "Buscar por nome:", placeholder="Digite o nome da planta..."
        )

        # Aplicar filtros
        filtered_df = self.df.copy()

        if selected_shareholder != "Todos":
            filtered_df = filtered_df[
                filtered_df["Shareholder"] == selected_shareholder
            ]

        if selected_cluster != "Todos":
            filtered_df = filtered_df[filtered_df["Cluster"] == selected_cluster]

        if search_name:
            filtered_df = filtered_df[
                filtered_df["Name_PWP"].str.contains(search_name, case=False, na=False)
            ]

        # Exibir informações do filtro
        st.sidebar.markdown("---")
        st.sidebar.metric("Total de Plantas", len(filtered_df))

        self.df = filtered_df

    def map(self):
        clicked_plant = pd.DataFrame()
        col1, col2 = st.columns(2)
        with col1:
            m = folium.Map(location=[-15.7797, -47.9297], zoom_start=4)

            for _, row in self.df.iterrows():
                folium.Marker(
                    location=[row["Latitude"], row["Longitude"]],
                    popup=row["Name_PWP"],
                ).add_to(m)

            map_data = st_folium(m, width=700, height=600)

            if map_data and map_data.get("last_object_clicked_popup"):
                clicked_plant = self.df[
                    self.df["Name_PWP"] == map_data["last_object_clicked_popup"]
                ]
        with col2:
            if not clicked_plant.empty:
                self.write_plant_info(clicked_plant.iloc[0])

    def write_plant_info(self, plant):
        st.subheader("Informações da Planta Selecionada")

        # Informações principais em colunas
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📋 **Dados Gerais**")
            st.markdown(f"**Nome:** {plant.get('Name_PWP', 'N/A')}")
            st.markdown(f"**Estado:** {plant.get('State', 'N/A')}")
            st.markdown(f"**Cluster:** {plant.get('Cluster', 'N/A')}")
            st.markdown(f"**Região:** {plant.get('Region', 'N/A')}")
            st.markdown(f"**Endereço:** {plant.get('Coordenadas(lat, lon)', 'N/A')}")

        with col2:
            st.markdown("### ⚡ **Especificações Técnicas**")
            st.markdown(
                f"**Capacidade DC:** {plant.get('CapacidadeDC (kWp)', 'N/A')} kWp"
            )
            st.markdown(
                f"**Capacidade AC:** {plant.get('CapacidadeAC (kW)', 'N/A')} kW"
            )
            st.markdown(f"**Tipo de Estrutura:** {plant.get('TypeOfStructure', 'N/A')}")
            st.markdown(f"**Operador da Rede:** {plant.get('Grid Operator', 'N/A')}")

        st.markdown("### 👥 **Responsáveis**")
        col3, col4 = st.columns(2)

        with col3:
            st.markdown(f"**Cliente:** {plant.get('Shareholder', 'N/A')}")
            st.markdown(f"**Supervisor:** {plant.get('PWP_Supervisor', 'N/A')}")

        with col4:
            st.markdown(f"**Gerente:** {plant.get('PWP_Manager', 'N/A')}")

        st.markdown("### 🏭 **Fabricantes**")
        col5, col6, col7 = st.columns(3)

        with col5:
            st.markdown(f"**Inversor:** {plant.get('Fabricante Inversor', 'N/A')}")

        with col6:
            st.markdown(f"**Trackers:** {plant.get('Fabricante Trackers', 'N/A')}")

        with col7:
            st.markdown(f"**Módulos:** {plant.get('Fabricante_Modulos', 'N/A')}")

    def stats(self):
        col1, col2, col3 = st.columns(3)
        with col1:
            shareholder_counts = self.df["Shareholder"].value_counts()
            fig = px.pie(
                values=shareholder_counts.values,
                names=shareholder_counts.index,
                title="Distribuição de Plantas por Cliente",
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            cluster_counts = self.df["Cluster"].value_counts()
            fig = px.bar(
                x=cluster_counts.index,
                y=cluster_counts.values,
                title="Distribuição de Plantas por Cluster",
                labels={"x": "Cluster", "y": "Número de Plantas"},
            )
            st.plotly_chart(fig, use_container_width=True)

        with col3:
            state_counts = self.df["State"].value_counts()
            treemap_df = pd.DataFrame(
                {
                    "ids": state_counts.index,
                    "labels": state_counts.index,
                    "parents": [""] * len(state_counts),
                    "values": state_counts.values,
                }
            )
            fig = px.treemap(
                treemap_df,
                ids="ids",
                names="labels",
                parents="parents",
                values="values",
                title="Distribuição de Plantas por Estado",
                color="values",
                color_continuous_scale="Viridis",
            )
            st.plotly_chart(fig, use_container_width=True)
