"""
Módulo de segurança para gerenciar senhas e tokens
"""

import secrets
import string
import logging
from datetime import datetime, timedelta
from passlib.context import CryptContext

# Configurar logger
logger = logging.getLogger(__name__)

# Contexto para hash de senhas usando bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def criar_hash_senha(senha: str) -> str:
    """
    Cria um hash seguro da senha usando bcrypt

    Args:
        senha: Senha em texto plano

    Returns:
        Hash da senha
    """
    return pwd_context.hash(senha)


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """
    Verifica se a senha em texto plano corresponde ao hash

    Args:
        senha_plana: Senha em texto plano
        senha_hash: Hash da senha armazenado no banco

    Returns:
        True se a senha está correta, False caso contrário
    """
    try:
        return pwd_context.verify(senha_plana, senha_hash)
    except ValueError as e:
        logger.warning(f"Erro ao verificar senha: hash inválido - {e}")
        return False
    except Exception as e:
        logger.error(f"Erro inesperado ao verificar senha: {e}", exc_info=True)
        return False


def gerar_token_redefinicao(tamanho: int = 32) -> str:
    """
    Gera um token aleatório seguro para redefinição de senha

    Args:
        tamanho: Tamanho do token em caracteres

    Returns:
        Token aleatório
    """
    caracteres = string.ascii_letters + string.digits
    return "".join(secrets.choice(caracteres) for _ in range(tamanho))


def obter_data_expiracao_token(horas: int = 24) -> str:
    """
    Calcula a data de expiração do token

    Args:
        horas: Número de horas de validade do token

    Returns:
        Data de expiração no formato ISO
    """
    expiracao = datetime.now() + timedelta(hours=horas)
    return expiracao.isoformat()


def gerar_senha_aleatoria(tamanho: int = 8) -> str:
    """
    Gera uma senha aleatória segura

    Args:
        tamanho: Tamanho da senha

    Returns:
        Senha aleatória
    """
    caracteres = string.ascii_letters + string.digits + "!@#$%"
    senha = "".join(secrets.choice(caracteres) for _ in range(tamanho))
    return senha
