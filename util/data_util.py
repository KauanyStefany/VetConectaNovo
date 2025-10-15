"""
Utilitários para conversão de datas e timestamps.
"""

from datetime import datetime, date
from typing import Union, Optional


def converter_para_date(
    valor: Union[str, date, None],
    formato: str = "%Y-%m-%d"
) -> Optional[date]:
    """
    Converte string ou date para date, retorna None se inválido.

    Args:
        valor: Valor a ser convertido (str, date ou None)
        formato: Formato de data esperado para strings (padrão: %Y-%m-%d)

    Returns:
        date object ou None se conversão falhar

    Examples:
        >>> converter_para_date("2025-10-15")
        date(2025, 10, 15)
        >>> converter_para_date(date(2025, 10, 15))
        date(2025, 10, 15)
        >>> converter_para_date(None)
        None
    """
    if valor is None:
        return None

    if isinstance(valor, date):
        return valor

    if isinstance(valor, str):
        try:
            return datetime.strptime(valor, formato).date()
        except ValueError:
            # Tentar formato com hora
            try:
                return datetime.strptime(valor, "%Y-%m-%d %H:%M:%S").date()
            except ValueError:
                # Tentar formato ISO
                try:
                    return datetime.fromisoformat(valor).date()
                except (ValueError, AttributeError):
                    return None

    return None


def converter_para_datetime(
    valor: Union[str, datetime, None],
    formato: str = "%Y-%m-%d %H:%M:%S"
) -> Optional[datetime]:
    """
    Converte string ou datetime para datetime.

    Args:
        valor: Valor a ser convertido (str, datetime ou None)
        formato: Formato de datetime esperado para strings

    Returns:
        datetime object ou None se conversão falhar

    Examples:
        >>> converter_para_datetime("2025-10-15 10:30:00")
        datetime(2025, 10, 15, 10, 30, 0)
        >>> converter_para_datetime(datetime(2025, 10, 15))
        datetime(2025, 10, 15, 0, 0)
        >>> converter_para_datetime(None)
        None
    """
    if valor is None:
        return None

    if isinstance(valor, datetime):
        return valor

    if isinstance(valor, str):
        try:
            return datetime.strptime(valor, formato)
        except ValueError:
            # Tentar formato ISO
            try:
                return datetime.fromisoformat(valor)
            except (ValueError, AttributeError):
                # Tentar formato apenas data
                try:
                    return datetime.strptime(valor, "%Y-%m-%d")
                except ValueError:
                    return None

    return None


def formatar_data(
    valor: Union[date, datetime, str, None],
    formato: str = "%d/%m/%Y"
) -> Optional[str]:
    """
    Formata uma data para string no formato brasileiro ou personalizado.

    Args:
        valor: Valor a ser formatado (date, datetime, str ou None)
        formato: Formato de saída desejado (padrão: %d/%m/%Y - brasileiro)

    Returns:
        String formatada ou None se conversão falhar

    Examples:
        >>> formatar_data(date(2025, 10, 15))
        '15/10/2025'
        >>> formatar_data("2025-10-15", "%d/%m/%Y")
        '15/10/2025'
    """
    if valor is None:
        return None

    if isinstance(valor, str):
        # Tentar converter string para date primeiro
        valor = converter_para_date(valor)
        if valor is None:
            return None

    if isinstance(valor, (date, datetime)):
        return valor.strftime(formato)

    return None


def formatar_datetime(
    valor: Union[datetime, str, None],
    formato: str = "%d/%m/%Y %H:%M:%S"
) -> Optional[str]:
    """
    Formata um datetime para string no formato brasileiro ou personalizado.

    Args:
        valor: Valor a ser formatado (datetime, str ou None)
        formato: Formato de saída desejado

    Returns:
        String formatada ou None se conversão falhar

    Examples:
        >>> formatar_datetime(datetime(2025, 10, 15, 10, 30, 0))
        '15/10/2025 10:30:00'
    """
    if valor is None:
        return None

    if isinstance(valor, str):
        # Tentar converter string para datetime primeiro
        valor = converter_para_datetime(valor)
        if valor is None:
            return None

    if isinstance(valor, datetime):
        return valor.strftime(formato)

    return None
