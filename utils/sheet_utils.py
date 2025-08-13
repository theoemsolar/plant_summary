import os
import json
import gspread
import pandas as pd
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
sa_json = os.environ.get("GOOGLE_SA_JSON")


def get_ws(spreadsheet_id: str, worksheet_name: str):
    creds_dict = json.loads(os.environ["GOOGLE_SA_JSON"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(spreadsheet_id)
    return sh.worksheet(worksheet_name)


def read_sheet_to_dataframe(spreadsheet_id: str, worksheet_name: str) -> pd.DataFrame:
    ws = get_ws(spreadsheet_id, worksheet_name)
    data = ws.get_all_records()
    return pd.DataFrame(data)
