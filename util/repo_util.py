"""
Utilitários para repositórios, incluindo decoradores para tratamento de exceções.
"""

import logging
from functools import wraps
from typing import Callable, TypeVar, Any

logger = logging.getLogger(__name__)

T = TypeVar('T')


def tratar_excecao_repo(valor_retorno_padrao: Any = None):
    """
    Decorador para tratar exceções em métodos de repositório.

    Este decorador captura todas as exceções que ocorrem durante a execução
    de métodos de repositório, registra o erro com logging e retorna um valor
    padrão em vez de propagar a exceção.

    Args:
        valor_retorno_padrao: Valor a ser retornado em caso de exceção
            (padrão: None)

    Returns:
        Decorador configurado

    Examples:
        >>> @tratar_excecao_repo(valor_retorno_padrao=None)
        ... def obter_usuario(id: int) -> Optional[Usuario]:
        ...     # código que pode lançar exceção
        ...     return usuario

        >>> @tratar_excecao_repo(valor_retorno_padrao=[])
        ... def listar_usuarios() -> List[Usuario]:
        ...     # código que pode lançar exceção
        ...     return usuarios

        >>> @tratar_excecao_repo(valor_retorno_padrao=False)
        ... def atualizar_usuario(usuario: Usuario) -> bool:
        ...     # código que pode lançar exceção
        ...     return True
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(
                    f"Erro em {func.__module__}.{func.__name__}: {e}",
                    exc_info=True
                )
                return valor_retorno_padrao
        return wrapper
    return decorator


def validar_id(id_valor: int, nome_campo: str = "ID") -> bool:
    """
    Valida se um ID é válido (inteiro positivo).

    Args:
        id_valor: Valor do ID a ser validado
        nome_campo: Nome do campo para mensagem de log (padrão: "ID")

    Returns:
        True se válido, False caso contrário

    Examples:
        >>> validar_id(1)
        True
        >>> validar_id(0)
        False
        >>> validar_id(-1)
        False
        >>> validar_id(None)
        False
    """
    if not isinstance(id_valor, int) or id_valor <= 0:
        logger.warning(f"{nome_campo} inválido: {id_valor}")
        return False
    return True


def validar_string_nao_vazia(valor: str, nome_campo: str) -> bool:
    """
    Valida se uma string não é vazia ou apenas espaços.

    Args:
        valor: String a ser validada
        nome_campo: Nome do campo para mensagem de log

    Returns:
        True se válido, False caso contrário

    Examples:
        >>> validar_string_nao_vazia("teste", "nome")
        True
        >>> validar_string_nao_vazia("", "nome")
        False
        >>> validar_string_nao_vazia("   ", "nome")
        False
        >>> validar_string_nao_vazia(None, "nome")
        False
    """
    if not valor or not isinstance(valor, str) or not valor.strip():
        logger.warning(f"{nome_campo} inválido: '{valor}'")
        return False
    return True


def validar_email(email: str) -> bool:
    """
    Valida formato básico de email.

    Args:
        email: Email a ser validado

    Returns:
        True se válido, False caso contrário

    Examples:
        >>> validar_email("user@example.com")
        True
        >>> validar_email("invalid-email")
        False
        >>> validar_email("")
        False
        >>> validar_email(None)
        False
    """
    if not email or not isinstance(email, str):
        logger.warning(f"Email inválido: {email}")
        return False

    # Validação básica de email
    if '@' not in email or '.' not in email.split('@')[-1]:
        logger.warning(f"Email com formato inválido: {email}")
        return False

    return True


def validar_paginacao(limite: int, offset: int) -> bool:
    """
    Valida parâmetros de paginação.

    Args:
        limite: Número máximo de registros por página
        offset: Número de registros a pular

    Returns:
        True se válido, False caso contrário

    Examples:
        >>> validar_paginacao(10, 0)
        True
        >>> validar_paginacao(10, 20)
        True
        >>> validar_paginacao(-1, 0)
        False
        >>> validar_paginacao(10, -1)
        False
    """
    if not isinstance(limite, int) or limite <= 0:
        logger.warning(f"Limite inválido: {limite}")
        return False

    if not isinstance(offset, int) or offset < 0:
        logger.warning(f"Offset inválido: {offset}")
        return False

    return True
