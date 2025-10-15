"""
Helper centralizado para conexão com banco de dados.
Re-exporta get_connection de util.db_util para centralizar acesso.
"""
from util.db_util import get_connection

__all__ = ['get_connection']
