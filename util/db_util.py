import sqlite3
import os
from contextlib import contextmanager
from typing import Generator
import logging

logger = logging.getLogger(__name__)

# Configuração via variáveis de ambiente
DB_PATH: str = os.getenv("TEST_DATABASE_PATH") or os.getenv("DATABASE_PATH") or "dados.db"
DB_TIMEOUT: float = float(os.getenv("DATABASE_TIMEOUT", "30.0"))


def _criar_conexao() -> sqlite3.Connection:
    """Cria uma conexão configurada com o banco de dados."""
    try:
        conn = sqlite3.connect(DB_PATH, timeout=DB_TIMEOUT, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        # CRITICAL: Habilitar foreign keys no SQLite
        conn.execute("PRAGMA foreign_keys = ON")
        # Performance improvements
        conn.execute("PRAGMA journal_mode = WAL")
        conn.execute("PRAGMA synchronous = NORMAL")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Erro ao conectar ao banco de dados: {e}")
        raise


@contextmanager
def get_connection() -> Generator[sqlite3.Connection, None, None]:
    """Context manager para gerenciar conexões com commit/rollback automático."""
    conn = _criar_conexao()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(f"Erro na transação, rollback executado: {e}")
        raise
    finally:
        conn.close()


def get_connection_sem_commit() -> sqlite3.Connection:
    """Retorna conexão sem commit automático para operações de leitura."""
    return _criar_conexao()
