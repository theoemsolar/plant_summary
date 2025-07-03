import os
import dotenv
from sqlmodel import Session
from sqlmodel import create_engine
from urllib.parse import quote_plus

dotenv.load_dotenv()
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")
SERVER = os.getenv("SERVER")
PORT = os.getenv("PORT")
DATABASE_GRL = os.getenv("DATABASE_GRL")
DATABASE_UFV = os.getenv("DATABASE_UFV")
DATABASE_UFV_FSP01 = os.getenv("DATABASE_UFV_FSP01")
DATABASE_UFV_FSP02 = os.getenv("DATABASE_UFV_FSP02")
DRIVER = f"{os.getenv('DRIVER')}"

driver_enc = quote_plus(DRIVER)
password_enc = quote_plus(PASSWORD)

DATABASE_URL_GRL = (
    f"mssql+pyodbc://{USER}:{password_enc}"
    f"@{SERVER},{PORT}/{DATABASE_GRL}"
    f"?driver={driver_enc}&Encrypt=no"
)

DATABASE_URL_UFV_FSP01 = (
    f"mssql+pyodbc://{USER}:{password_enc}"
    f"@{SERVER},{PORT}/{DATABASE_UFV_FSP01}"
    f"?driver={driver_enc}&Encrypt=no"
)

DATABASE_URL_UFV_FSP02 = (
    f"mssql+pyodbc://{USER}:{password_enc}"
    f"@{SERVER},{PORT}/{DATABASE_UFV_FSP02}"
    f"?driver={driver_enc}&Encrypt=no"
)

DATABASE_URL_UFV = (
    f"mssql+pyodbc://{USER}:{password_enc}"
    f"@{SERVER},{PORT}/{DATABASE_UFV}"
    f"?driver={driver_enc}&Encrypt=no"
)

engine_grl = create_engine(DATABASE_URL_GRL)
engine_ufv = create_engine(DATABASE_URL_UFV)
engine_ufv_fsp01 = create_engine(DATABASE_URL_UFV_FSP01)
engine_ufv_fsp02 = create_engine(DATABASE_URL_UFV_FSP02)


def get_session_grl():
    with Session(engine_grl) as session:
        yield session


def get_session_ufv():
    with Session(engine_ufv) as session:
        yield session


def get_session_ufv_fsp01():
    with Session(engine_ufv_fsp01) as session:
        yield session


def get_session_ufv_fsp02():
    with Session(engine_ufv_fsp02) as session:
        yield session
