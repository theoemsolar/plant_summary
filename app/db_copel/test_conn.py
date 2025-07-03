import os
import pyodbc
from dotenv import load_dotenv

load_dotenv()
databases = [
    os.getenv("DATABASE_GRL"),
    os.getenv("DATABASE_UFV"),
    os.getenv("DATABASE_UFV_FSP01"),
    os.getenv("DATABASE_UFV_FSP02"),
]

for database in databases:
    SERVER = f"{os.getenv('SERVER')},{os.getenv('PORT')}"
    USER = f"{os.getenv('USER')}"
    PASSWORD = f"{os.getenv('PASSWORD')}"
    DRIVER = f"{os.getenv('DRIVER')}"

    CONN_STR = (
        f"DRIVER={{{DRIVER}}};SERVER={SERVER};DATABASE={database};"
        f"UID={USER};PWD={PASSWORD};Encrypt=no;"
    )

    try:
        conn = pyodbc.connect(CONN_STR, timeout=5)
        print(f"✅ {database} Conexão OK!")
        conn.close()
    except Exception as e:
        print(f"❌ {database} Erro:", e)
