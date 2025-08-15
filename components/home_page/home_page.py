import streamlit as st
from utils.filter_df.filter_dataframe import FilterDataFrame

TOTAL_OF_COLUMNS = 6


def plant_summary_card(plant_name, inverters_alarms, trackers_alarms, total_generation):
    """Componente compacto para resumo da usina"""
    # Cores dos alarmes de inversores
    alarm_colors = {
        "iniciando_espera": "#D97706",  # Laranja - Iniciando ou Espera
        "falha_parado": "#B91C1C",  # Vermelho - Falha ou Parado
        "comunicacao": "#1E3A8A",  # Azul escuro - Comunicação
    }

    # Emojis dos alarmes de trackers
    tracker_emojis = {
        "comunicacao": "📡",  # Comunicação
        "sistema": "🖥️",  # Sistema
        "backtracking": "🔄",  # Backtracking
        "bateria": "🔋",  # Bateria
    }

    # Contar total de alarmes de inversores
    total_inv_alarms = (
        sum(inverters_alarms.values())
        if isinstance(inverters_alarms, dict)
        else inverters_alarms
    )

    # Contar total de alarmes de trackers
    total_track_alarms = (
        sum(trackers_alarms.values())
        if isinstance(trackers_alarms, dict)
        else trackers_alarms
    )

    # Cor para trackers
    track_color = "#ff6b6b" if total_track_alarms > 0 else "#e0e0e0"

    # Criar indicadores visuais dos alarmes de inversores ativos
    alarm_indicators = ""
    if isinstance(inverters_alarms, dict):
        for alarm_type, count in inverters_alarms.items():
            if count > 0 and alarm_type in alarm_colors:
                alarm_indicators += f'<span style="display: inline-block; width: 12px; height: 12px; background-color: {alarm_colors[alarm_type]}; border-radius: 50%; margin-right: 3px; border: 1px solid #fff;"></span>'

    # Criar indicadores visuais dos alarmes de trackers ativos
    tracker_indicators = ""
    if isinstance(trackers_alarms, dict):
        for tracker_type, count in trackers_alarms.items():
            if count > 0 and tracker_type in tracker_emojis:
                tracker_indicators += f'<span style="margin-right: 4px; font-size: 14px;">{tracker_emojis[tracker_type]}</span>'

    # Sempre piscar vermelho se houver qualquer alarme
    card_alarm_color = None
    if total_inv_alarms > 0 or total_track_alarms > 0:
        card_alarm_color = "#B91C1C"  # vermelho

    # CSS para animação do card
    if card_alarm_color:
        st.markdown(
            f"""
            <style>
            @keyframes pulsar-card-alarm {{
                0% {{ box-shadow: 0 0 0 0 {card_alarm_color}55; border-color: {card_alarm_color}; }}
                100% {{ box-shadow: 0 0 24px 8px {card_alarm_color}cc; border-color: {card_alarm_color}; }}
            }}
            .pulsar-card-alarm {{
                animation: pulsar-card-alarm 1.2s infinite alternate;
                border-color: {card_alarm_color} !important;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )

    with st.container():
        st.markdown(
            f"""
        <div class='{'pulsar-card-alarm' if card_alarm_color else ''}' style='
            background-color: #2d3748;
            border: 2px solid {card_alarm_color if card_alarm_color else '#4a5568'};
            border-radius: 8px;
            padding: 10px;
            margin: 5px 0;
            height: 120px;
            color: #e0e0e0;
        '>
            <div style='font-weight: bold; font-size: 14px; margin-bottom: 8px; color: #e0e0e0;'>
                {plant_name}
            </div>
            <div style='font-size: 12px; line-height: 1.4;'>
                <div style='margin-bottom: 4px; color: {"#ff6b6b" if total_inv_alarms > 0 else "#e0e0e0"}; font-weight: {"bold" if total_inv_alarms > 0 else "normal"}; display: flex; justify-content: space-between; align-items: center;'>
                    <span>🔧 Inversores: {total_inv_alarms}</span>
                    <span>{alarm_indicators}</span>
                </div>
                <div style='margin-bottom: 4px; color: {track_color}; font-weight: {"bold" if total_track_alarms > 0 else "normal"}; display: flex; justify-content: space-between; align-items: center;'>
                    <span>📡 Trackers: {total_track_alarms}</span>
                    <span>{tracker_indicators}</span>
                </div>
                <div style='color: #81c784;'>
                    ⚡ {total_generation:.1f} Wh
                </div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )


def get_total_inverter_alarms(df):
    alarms = {"iniciando_espera": 0, "falha_parado": 0, "comunicacao": 0}
    for alarm, total in (
        FilterDataFrame.filter_df_last_data_per_inverter(df, "alarm")["alarm"]
        .value_counts()
        .to_dict()
        .items()
    ):
        if "INICIANDO" in alarm or "ESPERA" in alarm:
            alarms["iniciando_espera"] += total
        elif "FALHA" in alarm or "PARADO" in alarm:
            alarms["falha_parado"] += total
        elif "COMUNICAÇÃO" in alarm:
            alarms["comunicacao"] += total

    return alarms


def get_total_trackers_alarms(df):
    return {
        "comunicacao": 0,
        "sistema": 0,
        "backtracking": 0,
        "bateria": 0,
    }


def get_total_generation(df):
    total_generation = FilterDataFrame.filter_df_last_data_per_inverter(
        df, "generation"
    )["generation"].sum()
    return total_generation if total_generation > 0 else -1


def home_dashboard():
    df = st.session_state.get("day_data", {})
    # Adiciona filtro na sidebar
    filtro_cards = st.sidebar.radio(
        "Exibir cards:", ("Todos", "Apenas com alarme"), index=0
    )
    # Filtra as plantas conforme o filtro selecionado
    plantas_para_exibir = []
    for plant in df.plant_name.unique():
        df_filtered_by_client = df[df.plant_name == plant]
        inv_alarms = get_total_inverter_alarms(df_filtered_by_client)
        track_alarms = get_total_trackers_alarms(df_filtered_by_client)
        has_any_alarm = (sum(inv_alarms.values()) > 0) or (
            sum(track_alarms.values()) > 0
        )
        if filtro_cards == "Apenas com alarme" and not has_any_alarm:
            continue
        plantas_para_exibir.append(
            (
                plant,
                inv_alarms,
                track_alarms,
                get_total_generation(df_filtered_by_client),
            )
        )

    columns = st.columns(TOTAL_OF_COLUMNS)
    for idx, (plant, inv_alarms, track_alarms, total_gen) in enumerate(
        plantas_para_exibir
    ):
        with columns[idx % TOTAL_OF_COLUMNS]:
            plant_summary_card(
                plant,
                inv_alarms,
                track_alarms,
                total_gen,
            )
