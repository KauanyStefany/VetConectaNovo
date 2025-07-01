import sqlite3
import os

def get_connection():
    conn = None
    try:
        database_path = os.environ.get('TEST_DATABASE_PATH', 'dados.db')
        conn = sqlite3.connect(database_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")  # Ativa as chaves estrangeiras
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    return conn