import os 
from pathlib import Path

import psycopg 
from dotenv import load_dotenv 
from psycopg.rows import dict_row

raiz_projeto = Path(__file__).resolve().parents[2]
load_dotenv(raiz_projeto / ".env")

def conectar():
    return psycopg.connect(
        host="127.0.0.1",
        port=5434,
        dbname="catalogo_musical",
        user="catalogo",
        password=os.environ["POSTGRES_PASSWORD"],
        row_factory=dict_row,
        connect_timeout=5,
    )