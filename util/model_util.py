"""
Utilitários para instanciação de modelos a partir de resultados de banco de dados.
"""

from typing import TypeVar, Type, Dict, Any, Optional
from sqlite3 import Row

T = TypeVar('T')


def row_to_dict(row: Row) -> Dict[str, Any]:
    """
    Converte sqlite3.Row para dict.

    Args:
        row: Objeto Row do sqlite3

    Returns:
        Dicionário com os dados da linha

    Examples:
        >>> # Assumindo cursor.fetchone() retorna um Row
        >>> row_dict = row_to_dict(row)
        >>> print(row_dict)
        {'id': 1, 'nome': 'João', 'email': 'joao@example.com'}
    """
    return dict(row)


def criar_modelo(model_class: Type[T], row: Optional[Row]) -> Optional[T]:
    """
    Cria instância do modelo a partir de Row.

    Args:
        model_class: Classe do modelo a ser instanciada
        row: Objeto Row do sqlite3 ou None

    Returns:
        Instância do modelo ou None se row for None

    Examples:
        >>> from model.usuario_model import Usuario
        >>> usuario = criar_modelo(Usuario, row)
        >>> if usuario:
        ...     print(usuario.nome)
    """
    if row is None:
        return None

    try:
        return model_class(**row_to_dict(row))
    except TypeError as e:
        # Log erro mas retorna None para manter consistência
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Erro ao criar modelo {model_class.__name__}: {e}")
        return None


def criar_modelos(model_class: Type[T], rows: list[Row]) -> list[T]:
    """
    Cria lista de instâncias do modelo a partir de lista de Rows.

    Args:
        model_class: Classe do modelo a ser instanciada
        rows: Lista de objetos Row do sqlite3

    Returns:
        Lista de instâncias do modelo (ignora Rows que causam erro)

    Examples:
        >>> from model.usuario_model import Usuario
        >>> usuarios = criar_modelos(Usuario, rows)
        >>> for usuario in usuarios:
        ...     print(usuario.nome)
    """
    modelos = []
    for row in rows:
        modelo = criar_modelo(model_class, row)
        if modelo is not None:
            modelos.append(modelo)
    return modelos


def row_to_dict_partial(row: Row, campos: list[str]) -> Dict[str, Any]:
    """
    Converte sqlite3.Row para dict contendo apenas campos especificados.

    Args:
        row: Objeto Row do sqlite3
        campos: Lista de nomes de campos a extrair

    Returns:
        Dicionário com apenas os campos especificados

    Examples:
        >>> row_dict = row_to_dict_partial(row, ['id', 'nome'])
        >>> print(row_dict)
        {'id': 1, 'nome': 'João'}
    """
    row_dict = dict(row)
    return {campo: row_dict.get(campo) for campo in campos if campo in row_dict}
