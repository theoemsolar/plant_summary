import time
import datetime
import threading
import streamlit as st
from services import SheetService
from utils import read_sheet_to_dataframe
import pickle
import os
from pathlib import Path

WORKSHEET_NAME = "PWP_Details"
WORKSHEET_NAME_GENERAL_DATA = "Resumo"
SPREADSHEET_ID = "1NYvgvdHIAvaNXbRe_PQHs9z9tXaabBk14RVSFqSN-nY"
DADOS_DAS_USINAS_SPREADSHEET_ID = "1_KoK1ll3t0b8fDd5V75-KMrRg5tiSTG8cqd6Ebn_Mss"

# Arquivo para persistir dados entre sessões
DATA_FILE = Path("temp_dashboard_data.pkl")
THREAD_CONTROL_FILE = Path("thread_control.txt")


def save_data_to_file(data):
    """Salva dados em arquivo temporário"""
    try:
        with open(DATA_FILE, "wb") as f:
            pickle.dump(data, f)
    except Exception as e:
        print(f"[ERROR] Erro ao salvar dados: {e}")


def load_data_from_file():
    """Carrega dados do arquivo temporário"""
    try:
        if DATA_FILE.exists():
            with open(DATA_FILE, "rb") as f:
                return pickle.load(f)
    except Exception as e:
        print(f"[ERROR] Erro ao carregar dados: {e}")
    return None


def is_thread_running():
    """Verifica se thread está rodando baseado em arquivo de controle"""
    if not THREAD_CONTROL_FILE.exists():
        return False

    try:
        with open(THREAD_CONTROL_FILE, "r") as f:
            timestamp = float(f.read().strip())
        # Se última atualização foi há mais de 30 segundos, considera thread morta
        return (time.time() - timestamp) < 30
    except:
        return False


def mark_thread_running():
    """Marca thread como rodando"""
    with open(THREAD_CONTROL_FILE, "w") as f:
        f.write(str(time.time()))


def start_background_updater(wait_time=5):
    """Inicia background updater com controle de thread melhorado"""

    # Carrega dados existentes primeiro
    existing_data = load_data_from_file()
    if existing_data:
        st.session_state.update(existing_data)
        print(f"[{datetime.datetime.now()}][INFO] Dados carregados do cache")

    # Verifica se thread já está rodando
    if is_thread_running():
        print(f"[{datetime.datetime.now()}][INFO] Thread já está rodando")
        return

    # Inicializa dados se não existirem
    if "day_data" not in st.session_state or st.session_state["day_data"] is None:
        st.session_state["day_data"] = None
        st.session_state["last_update"] = None

        # Carrega dados iniciais
        try:
            st.session_state["general_data"] = read_sheet_to_dataframe(
                DADOS_DAS_USINAS_SPREADSHEET_ID, WORKSHEET_NAME_GENERAL_DATA
            )
            print(f"[{datetime.datetime.now()}][INFO] General data fetched")

            st.session_state["plants_details"] = read_sheet_to_dataframe(
                SPREADSHEET_ID, WORKSHEET_NAME
            )
            print(f"[{datetime.datetime.now()}][INFO] Plants details fetched")
        except Exception as e:
            print(
                f"[{datetime.datetime.now()}][ERROR] Erro ao carregar dados iniciais: {e}"
            )

    def updater():
        """Função de atualização em background"""
        while True:
            try:
                mark_thread_running()

                # Busca dados atualizados
                df = SheetService().get_daily_data_by_client("Copel")

                # Carrega dados do arquivo para obter general_data
                file_data = load_data_from_file()
                if file_data and "general_data" in file_data:
                    general_data_df = file_data["general_data"]
                else:
                    # Fallback: carrega diretamente
                    general_data_df = read_sheet_to_dataframe(
                        DADOS_DAS_USINAS_SPREADSHEET_ID, WORKSHEET_NAME_GENERAL_DATA
                    )

                # Adiciona cliente aos dados
                for plant in df.plant_name.unique():
                    try:
                        client = general_data_df[general_data_df["Usina"] == plant][
                            "Cliente"
                        ].values[0]
                        df.loc[df["plant_name"] == plant, "client"] = client
                    except IndexError:
                        print(f"[WARNING] Cliente não encontrado para planta: {plant}")

                # Prepara dados para salvar
                updated_data = {
                    "day_data": df,
                    "last_update": datetime.datetime.now(),
                    "general_data": general_data_df,
                }

                if "plants_details" in st.session_state:
                    updated_data["plants_details"] = st.session_state["plants_details"]

                # Salva no arquivo e no session_state
                save_data_to_file(updated_data)
                st.session_state.update(updated_data)

                print(f"[{datetime.datetime.now()}][INFO] Data fetched and saved")

            except Exception as e:
                print(f"[{datetime.datetime.now()}][ERROR] {e}")

            time.sleep(wait_time)

    # Inicia thread
    thread = threading.Thread(target=updater, daemon=True)
    thread.start()
    print(f"[{datetime.datetime.now()}][INFO] Background thread iniciada")


def cleanup_temp_files():
    """Remove arquivos temporários"""
    try:
        if DATA_FILE.exists():
            os.remove(DATA_FILE)
        if THREAD_CONTROL_FILE.exists():
            os.remove(THREAD_CONTROL_FILE)
    except Exception as e:
        print(f"[ERROR] Erro ao limpar arquivos temporários: {e}")
