"""
Utilitários para conversão de enums.
"""

from enum import Enum
from typing import Union, Type, TypeVar, Optional

E = TypeVar('E', bound=Enum)


def enum_para_valor(enum_ou_valor: Union[E, str, int]) -> Union[str, int]:
    """
    Converte enum para valor ou retorna o valor se já for primitivo.

    Args:
        enum_ou_valor: Um enum ou valor primitivo (str, int)

    Returns:
        O valor do enum (str ou int)

    Examples:
        >>> from enum import Enum
        >>> class Status(Enum):
        ...     ABERTO = "aberto"
        ...     FECHADO = "fechado"
        >>> enum_para_valor(Status.ABERTO)
        'aberto'
        >>> enum_para_valor("aberto")
        'aberto'
    """
    return enum_ou_valor.value if isinstance(enum_ou_valor, Enum) else enum_ou_valor


def valor_para_enum(valor: Union[str, int, None], enum_class: Type[E]) -> Optional[E]:
    """
    Converte valor para enum de forma segura.

    Args:
        valor: Valor a ser convertido (str, int ou None)
        enum_class: Classe do enum

    Returns:
        Instância do enum ou None se valor for None ou inválido

    Examples:
        >>> from enum import Enum
        >>> class Status(Enum):
        ...     ABERTO = "aberto"
        ...     FECHADO = "fechado"
        >>> valor_para_enum("aberto", Status)
        <Status.ABERTO: 'aberto'>
        >>> valor_para_enum(None, Status)
        None
        >>> valor_para_enum("invalido", Status)
        None
    """
    if valor is None:
        return None

    try:
        return enum_class(valor)
    except (ValueError, KeyError):
        return None


def enum_para_nome(enum_ou_valor: Union[E, str, int, None]) -> Optional[str]:
    """
    Retorna o nome do enum (não o valor).

    Args:
        enum_ou_valor: Um enum, valor primitivo ou None

    Returns:
        O nome do enum ou None

    Examples:
        >>> from enum import Enum
        >>> class Status(Enum):
        ...     ABERTO = "aberto"
        ...     FECHADO = "fechado"
        >>> enum_para_nome(Status.ABERTO)
        'ABERTO'
    """
    if enum_ou_valor is None:
        return None

    return enum_ou_valor.name if isinstance(enum_ou_valor, Enum) else None


def listar_valores_enum(enum_class: Type[E]) -> list[Union[str, int]]:
    """
    Lista todos os valores possíveis de um enum.

    Args:
        enum_class: Classe do enum

    Returns:
        Lista com todos os valores do enum

    Examples:
        >>> from enum import Enum
        >>> class Status(Enum):
        ...     ABERTO = "aberto"
        ...     FECHADO = "fechado"
        >>> listar_valores_enum(Status)
        ['aberto', 'fechado']
    """
    return [item.value for item in enum_class]


def listar_nomes_enum(enum_class: Type[E]) -> list[str]:
    """
    Lista todos os nomes possíveis de um enum.

    Args:
        enum_class: Classe do enum

    Returns:
        Lista com todos os nomes do enum

    Examples:
        >>> from enum import Enum
        >>> class Status(Enum):
        ...     ABERTO = "aberto"
        ...     FECHADO = "fechado"
        >>> listar_nomes_enum(Status)
        ['ABERTO', 'FECHADO']
    """
    return [item.name for item in enum_class]
