"""
Módulo de segurança para autenticação e autorização
Baseado no sistema da loja2025, adaptado para VetConecta
"""
import secrets
import re
from datetime import datetime, timedelta
from typing import Tuple
from passlib.context import CryptContext


# Configuração do context de hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def criar_hash_senha(senha: str) -> str:
    """Cria um hash seguro da senha usando bcrypt"""
    return pwd_context.hash(senha)


def verificar_senha(senha_texto: str, senha_hash: str) -> bool:
    """Verifica se a senha em texto coincide com o hash"""
    try:
        return pwd_context.verify(senha_texto, senha_hash)
    except:
        return False


def validar_forca_senha(senha: str) -> Tuple[bool, str]:
    """
    Valida a força da senha conforme critérios de segurança

    Critérios:
    - Mínimo 8 caracteres
    - Pelo menos 1 letra maiúscula
    - Pelo menos 1 letra minúscula
    - Pelo menos 1 número
    - Pelo menos 1 caractere especial

    Returns:
        Tuple[bool, str]: (é_válida, mensagem_erro)
    """
    if len(senha) < 8:
        return False, "A senha deve ter pelo menos 8 caracteres"

    if not re.search(r'[A-Z]', senha):
        return False, "A senha deve conter pelo menos uma letra maiúscula"

    if not re.search(r'[a-z]', senha):
        return False, "A senha deve conter pelo menos uma letra minúscula"

    if not re.search(r'\d', senha):
        return False, "A senha deve conter pelo menos um número"

    if not re.search(r'[!@#$%^&*()_+\-=\[\]{};\'\\:"|,.<>/?]', senha):
        return False, "A senha deve conter pelo menos um caractere especial"

    return True, ""


def gerar_token_redefinicao() -> str:
    """Gera um token seguro para redefinição de senha"""
    return secrets.token_urlsafe(32)


def obter_data_expiracao_token(horas: int = 24) -> str:
    """
    Obtém a data de expiração do token

    Args:
        horas: Número de horas para expiração (padrão: 24)

    Returns:
        str: Data de expiração no formato ISO
    """
    data_expiracao = datetime.now() + timedelta(hours=horas)
    return data_expiracao.isoformat()


def token_expirado(data_token: str) -> bool:
    """
    Verifica se o token está expirado

    Args:
        data_token: Data do token no formato ISO

    Returns:
        bool: True se expirado, False caso contrário
    """
    try:
        data_expiracao = datetime.fromisoformat(data_token)
        return datetime.now() > data_expiracao
    except (ValueError, TypeError):
        return True  # Se não conseguir parsear, considera expirado


def validar_crmv(crmv: str) -> Tuple[bool, str]:
    """
    Valida o formato do CRMV (Conselho Regional de Medicina Veterinária)

    Formato esperado: CRMV-XX NNNNN (onde XX é o estado e NNNNN é o número)

    Args:
        crmv: String do CRMV a ser validado

    Returns:
        Tuple[bool, str]: (é_válido, mensagem_erro)
    """
    if not crmv:
        return False, "CRMV é obrigatório para veterinários"

    # Formato: CRMV-XX NNNNN ou CRMV/XX NNNNN
    padrao = r'^CRMV[-/][A-Z]{2}\s+\d{4,6}$'

    if not re.match(padrao, crmv.strip().upper()):
        return False, "Formato de CRMV inválido. Use: CRMV-XX NNNNN (ex: CRMV-SP 12345)"

    return True, ""


def validar_cpf(cpf: str) -> Tuple[bool, str]:
    """
    Valida o formato e dígitos verificadores do CPF

    Args:
        cpf: String do CPF a ser validado

    Returns:
        Tuple[bool, str]: (é_válido, mensagem_erro)
    """
    # Remove caracteres não numéricos
    cpf_numeros = re.sub(r'\D', '', cpf)

    # Verifica se tem 11 dígitos
    if len(cpf_numeros) != 11:
        return False, "CPF deve ter 11 dígitos"

    # Verifica se não são todos os números iguais
    if cpf_numeros == cpf_numeros[0] * 11:
        return False, "CPF inválido"

    # Validação dos dígitos verificadores
    def calcular_digito(cpf_parcial):
        soma = 0
        for i, digito in enumerate(cpf_parcial):
            soma += int(digito) * (len(cpf_parcial) + 1 - i)
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    # Valida primeiro dígito
    primeiro_digito = calcular_digito(cpf_numeros[:9])
    if primeiro_digito != int(cpf_numeros[9]):
        return False, "CPF inválido"

    # Valida segundo dígito
    segundo_digito = calcular_digito(cpf_numeros[:10])
    if segundo_digito != int(cpf_numeros[10]):
        return False, "CPF inválido"

    return True, ""


def formatar_cpf(cpf: str) -> str:
    """
    Formata o CPF para o padrão XXX.XXX.XXX-XX

    Args:
        cpf: CPF em qualquer formato

    Returns:
        str: CPF formatado
    """
    cpf_numeros = re.sub(r'\D', '', cpf)
    if len(cpf_numeros) == 11:
        return f"{cpf_numeros[:3]}.{cpf_numeros[3:6]}.{cpf_numeros[6:9]}-{cpf_numeros[9:]}"
    return cpf


def validar_telefone(telefone: str) -> Tuple[bool, str]:
    """
    Valida o formato do telefone brasileiro

    Args:
        telefone: String do telefone a ser validado

    Returns:
        Tuple[bool, str]: (é_válido, mensagem_erro)
    """
    # Remove caracteres não numéricos
    telefone_numeros = re.sub(r'\D', '', telefone)

    # Verifica se tem 10 ou 11 dígitos (com ou sem celular)
    if len(telefone_numeros) not in [10, 11]:
        return False, "Telefone deve ter 10 ou 11 dígitos"

    # Verifica se começa com código de área válido (11-99)
    codigo_area = int(telefone_numeros[:2])
    if codigo_area < 11 or codigo_area > 99:
        return False, "Código de área inválido"

    return True, ""


def formatar_telefone(telefone: str) -> str:
    """
    Formata o telefone para o padrão (XX) XXXXX-XXXX ou (XX) XXXX-XXXX

    Args:
        telefone: Telefone em qualquer formato

    Returns:
        str: Telefone formatado
    """
    telefone_numeros = re.sub(r'\D', '', telefone)

    if len(telefone_numeros) == 11:
        # Celular: (XX) 9XXXX-XXXX
        return f"({telefone_numeros[:2]}) {telefone_numeros[2:7]}-{telefone_numeros[7:]}"
    elif len(telefone_numeros) == 10:
        # Fixo: (XX) XXXX-XXXX
        return f"({telefone_numeros[:2]}) {telefone_numeros[2:6]}-{telefone_numeros[6:]}"

    return telefone