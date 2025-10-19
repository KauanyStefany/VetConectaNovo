import re
from typing import Optional, Any
from pydantic import ValidationError


def processar_erros_validacao(e: ValidationError) -> dict:
    erros = {}
    for erro in e.errors():
        campo = erro["loc"][0] if erro["loc"] else "campo"
        mensagem = erro["msg"].replace("Value error, ", "")
        erros[str(campo).lower()] = mensagem
    return erros


def validar_forca_senha(senha: str) -> tuple[bool, str]:
    erros = []
    if len(senha) < 8:
        erros.append("A senha deve ter pelo menos 8 caracteres")

    if not any(c.islower() for c in senha):
        erros.append("A senha deve conter pelo menos uma letra minúscula")

    if not any(c.isupper() for c in senha):
        erros.append("A senha deve conter pelo menos uma letra maiúscula")

    if not any(c.isdigit() for c in senha):
        erros.append("A senha deve conter pelo menos um número")

    if not any(c in "!@#$%^&*(),.?\":{}|<>_-+=[]\\;'/" for c in senha):
        erros.append(
            "A senha deve conter pelo menos um caractere especial (!@#$%^&*(),.?\":{}|<>_-+=[]\\;'/)"
        )

    # Lista de senhas comuns que devem ser rejeitadas
    senhas_comuns = [
        "123456",
        "password",
        "123456789",
        "12345678",
        "12345",
        "1234567",
        "qwerty",
        "abc123",
        "password1",
        "123123",
    ]

    if senha.lower() in senhas_comuns:
        erros.append("A senha é muito comum e fácil de adivinhar")

    if erros:
        return False, "; ".join(erros)

    return True, ""


def validar_crmv(crmv: str) -> str:    
    crmv_limpo = re.sub(r"[^0-9]", "", crmv)
    if not crmv.strip():
        raise ValueError("CRMV é obrigatório")
    if len(crmv_limpo) != 6:
        raise ValueError("CRMV deve ter 6 dígitos")
    if crmv_limpo == crmv_limpo[0] * 6:
        raise ValueError("CRMV inválido")
    return crmv_limpo


def validar_telefone(telefone: str) -> str:
    telefone_limpo = re.sub(r"[^0-9]", "", telefone)
    if not telefone_limpo:
        raise ValueError("Telefone é obrigatório")
    if len(telefone_limpo) < 10 or len(telefone_limpo) > 11:
        raise ValueError("Telefone deve ter 10 ou 11 dígitos")
    ddd = telefone_limpo[:2]
    if not (11 <= int(ddd) <= 99):
        raise ValueError("DDD inválido")
    return telefone_limpo


def validar_nome_pessoa(nome: str, min_words: int = 2, min_chars: int = 2, max_chars: int = 100) -> str:
    if not nome or not nome.strip():
        raise ValueError("Nome é obrigatório")
    palavras = nome.split()
    if len(palavras) < min_words:
        raise ValueError(f"Nome deve conter pelo menos {min_words} palavras")
    nome_limpo = " ".join(palavras)
    if len(nome_limpo) < min_chars:
        raise ValueError(f"Nome deve ter pelo menos {min_chars} caracteres")
    if len(nome_limpo) > max_chars:
        raise ValueError(f"Nome deve ter no máximo {max_chars} caracteres")
    # Verificar se contém apenas letras, espaços e acentos
    if not re.match(r"^[a-zA-ZÀ-ÿ\s]+$", nome_limpo):
        raise ValueError("Nome deve conter apenas letras e espaços")
    return nome_limpo


def validar_texto_obrigatorio(
    texto: str, campo: str, min_chars: int = 1, max_chars: int = 1000
) -> str:
    if not texto or not texto.strip():
        raise ValueError(f"{campo} é obrigatório")
    texto_limpo = " ".join(texto.split())
    if len(texto_limpo) < min_chars:
        raise ValueError(f"{campo} deve ter pelo menos {min_chars} caracteres")
    if len(texto_limpo) > max_chars:
        raise ValueError(f"{campo} deve ter no máximo {max_chars} caracteres")
    return texto_limpo


def validar_texto_opcional(
    texto: Optional[str], max_chars: int = 1000
) -> Optional[str]:
    if not texto:
        return None
    texto_limpo = " ".join(texto.split()) if texto.strip() else None
    if texto_limpo and len(texto_limpo) > max_chars:
        raise ValueError(f"Texto deve ter no máximo {max_chars} caracteres")
    return texto_limpo


def validar_email(email: str) -> str:
    email_limpo = email.strip()
    if not email_limpo:
        raise ValueError("Email é obrigatório")
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_regex, email_limpo):
        raise ValueError("Email inválido")
    return email_limpo.lower()


def validar_senha(
    senha: str,
    min_chars: int = 6,
    max_chars: int = 128
) -> str:
    if not senha.strip():
        raise ValueError("Senha é obrigatória")
    if len(senha.strip()) < min_chars:
        raise ValueError(f"Senha deve ter pelo menos {min_chars} caracteres")
    if len(senha.strip()) > max_chars:
        raise ValueError(f"Senha deve ter no máximo {max_chars} caracteres")
    is_forte, mensagem = validar_forca_senha(senha.strip())
    if not is_forte:
        raise ValueError(f"Senha fraca: {mensagem}")
    return senha.strip()


def validar_senhas_coincidem(senha: str, confirmar_senha: str) -> str:
    if senha.strip() != confirmar_senha.strip():
        raise ValueError("As senhas não coincidem")
    return confirmar_senha.strip()


def converter_checkbox_para_bool(valor: Any) -> bool:
    if isinstance(valor, bool):
        return valor
    if isinstance(valor, str):
        return valor.lower() in ["on", "true", "1", "yes"]
    return bool(valor)


def validar_enum_valor(valor: Any, enum_class) -> Any:
    if isinstance(valor, str):
        try:
            return enum_class(valor.upper())
        except ValueError:
            valores_validos = [item.value for item in enum_class]
            raise ValueError(
                f'Valor deve ser uma das opções: {", ".join(valores_validos)}'
            )
    valores_validos = [item.value for item in enum_class]
    if valor not in valores_validos:
        raise ValueError(
            f'Valor deve ser uma das opções: {", ".join(valores_validos)}'
        )
    return valor

