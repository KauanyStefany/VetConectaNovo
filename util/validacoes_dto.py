import re
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, Any


class ValidacaoError(ValueError):
    pass


def validar_crmv(crmv: Optional[str]) -> Optional[str]:
    if not crmv:
        return None

    # Remover caracteres especiais
    crmv_limpo = re.sub(r'[^0-9]', '', crmv)
    
    if len(crmv_limpo) != 6:
        raise ValidacaoError('CRMV deve ter 6 dígitos')

    # Verificar se todos os dígitos são iguais
    if crmv_limpo == crmv_limpo[0] * 6:
        raise ValidacaoError('CRMV inválido')

    return crmv_limpo

def validar_telefone(telefone: str) -> str:
    if not telefone:
        raise ValidacaoError('Telefone é obrigatório')

    # Remover caracteres especiais
    telefone_limpo = re.sub(r'[^0-9]', '', telefone)

    if len(telefone_limpo) < 10 or len(telefone_limpo) > 11:
        raise ValidacaoError('Telefone deve ter 10 ou 11 dígitos')

    # Validar DDD
    ddd = telefone_limpo[:2]
    if not (11 <= int(ddd) <= 99):
        raise ValidacaoError('DDD inválido')

    return telefone_limpo



def validar_nome_pessoa(nome: str, min_chars: int = 2, max_chars: int = 100) -> str:
    if not nome or not nome.strip():
        raise ValidacaoError('Nome é obrigatório')

    # Verificar se contém pelo menos duas palavras
    palavras = nome.split()
    if len(palavras) < 2:
        raise ValidacaoError('Nome deve conter pelo menos nome e sobrenome')

    # Remover espaços extras
    nome_limpo = ' '.join(palavras)

    if len(nome_limpo) < min_chars:
        raise ValidacaoError(f'Nome deve ter pelo menos {min_chars} caracteres')

    if len(nome_limpo) > max_chars:
        raise ValidacaoError(f'Nome deve ter no máximo {max_chars} caracteres')

    # Verificar se contém apenas letras, espaços e acentos
    if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', nome_limpo):
        raise ValidacaoError('Nome deve conter apenas letras e espaços')

    return nome_limpo


def validar_texto_obrigatorio(texto: str, campo: str, min_chars: int = 1, max_chars: int = 1000) -> str:
    if not texto or not texto.strip():
        raise ValidacaoError(f'{campo} é obrigatório')

    # Remover espaços extras
    texto_limpo = ' '.join(texto.split())

    if len(texto_limpo) < min_chars:
        raise ValidacaoError(f'{campo} deve ter pelo menos {min_chars} caracteres')

    if len(texto_limpo) > max_chars:
        raise ValidacaoError(f'{campo} deve ter no máximo {max_chars} caracteres')

    return texto_limpo


def validar_texto_opcional(texto: Optional[str], max_chars: int = 1000) -> Optional[str]:
    if not texto:
        return None

    # Remover espaços extras
    texto_limpo = ' '.join(texto.split()) if texto.strip() else None

    if texto_limpo and len(texto_limpo) > max_chars:
        raise ValidacaoError(f'Texto deve ter no máximo {max_chars} caracteres')

    return texto_limpo



def validar_senha(senha: Optional[str], min_chars: int = 6, max_chars: int = 128, obrigatorio: bool = True) -> Optional[str]:
    if not senha:
        if obrigatorio:
            raise ValidacaoError('Senha é obrigatória')
        return None

    if len(senha) < min_chars:
        raise ValidacaoError(f'Senha deve ter pelo menos {min_chars} caracteres')

    if len(senha) > max_chars:
        raise ValidacaoError(f'Senha deve ter no máximo {max_chars} caracteres')

    return senha


def validar_senhas_coincidem(senha: str, confirmar_senha: str) -> str:
    if senha != confirmar_senha:
        raise ValidacaoError('As senhas não coincidem')

    return confirmar_senha


def converter_checkbox_para_bool(valor: Any) -> bool:
    if isinstance(valor, bool):
        return valor
    if isinstance(valor, str):
        return valor.lower() in ['on', 'true', '1', 'yes']
    return bool(valor)


def validar_enum_valor(valor: Any, enum_class, campo: str = "Campo") -> Any:
    if isinstance(valor, str):
        try:
            return enum_class(valor.upper())
        except ValueError:
            valores_validos = [item.value for item in enum_class]
            raise ValidacaoError(f'{campo} deve ser uma das opções: {", ".join(valores_validos)}')

    if valor not in enum_class:
        valores_validos = [item.value for item in enum_class]
        raise ValidacaoError(f'{campo} deve ser uma das opções: {", ".join(valores_validos)}')

    return valor


class ValidadorWrapper:
    @staticmethod
    def criar_validador(funcao_validacao, campo_nome: str = None, **kwargs):
        def validador(valor):
            try:
                if campo_nome:
                    return funcao_validacao(valor, campo_nome, **kwargs)
                else:
                    return funcao_validacao(valor, **kwargs)
            except ValidacaoError as e:
                raise ValueError(str(e))
        return validador

    @staticmethod
    def criar_validador_opcional(funcao_validacao, campo_nome: str = None, **kwargs):
        def validador(valor):
            if valor is None or (isinstance(valor, str) and not valor.strip()):
                return None
            try:
                if campo_nome:
                    return funcao_validacao(valor, campo_nome, **kwargs)
                else:
                    return funcao_validacao(valor, **kwargs)
            except ValidacaoError as e:
                raise ValueError(str(e))
        return validador


VALIDADOR_NOME = ValidadorWrapper.criar_validador(validar_nome_pessoa, "Nome")
VALIDADOR_CRMV = ValidadorWrapper.criar_validador_opcional(validar_crmv, "CRMV")
VALIDADOR_TELEFONE = ValidadorWrapper.criar_validador(validar_telefone, "Telefone")
VALIDADOR_SENHA = ValidadorWrapper.criar_validador(validar_senha, "Senha")
VALIDADOR_EMAIL = ValidadorWrapper.criar_validador_opcional(lambda v, c: v, "Email")