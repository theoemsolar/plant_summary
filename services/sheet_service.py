import pandas as pd
from utils import read_sheet_to_dataframe

SPREAD_SHEET_IDS = {
    "Copel": "1_KoK1ll3t0b8fDd5V75-KMrRg5tiSTG8cqd6Ebn_Mss",
    # "GY": "1fxlC5x9BwmZJ1JkMoyRRgrENdMdUxu-5D4bTdxF8C8E",
}

MONTHS = [
    "Janeiro",
    "Fevereiro",
    "Março",
    "Abril",
    "Maio",
    "Junho",
    "Julho",
    "Agosto",
    "Setembro",
    "Outubro",
    "Novembro",
    "Dezembro",
]


class SheetService:

    def get_daily_data_by_client(self, client):
        df = read_sheet_to_dataframe(SPREAD_SHEET_IDS.get(client, None), f"Hoje")
        if "generation" in df.columns:
            df["generation"] = df["generation"].replace("", -1)
        df["client"] = client
        return df

    def get_historical_data_by_client(self, client, month):
        if client not in SPREAD_SHEET_IDS.keys():
            raise ValueError(
                f"Client '{client}' not found in spreadsheet IDs. Choose from {list(SPREAD_SHEET_IDS.keys())}."
            )

        if month not in MONTHS:
            raise ValueError(f"Month '{month}' is not valid. Choose from {MONTHS}.")

        df = read_sheet_to_dataframe(SPREAD_SHEET_IDS.get(client, None), month)
        df["client"] = client
        return df
