"""
Sistema de mensagens flash para FastAPI
Permite enviar mensagens através de redirects usando sessões

VetConecta - Utilidade de mensagens flash
"""

from fastapi import Request
from typing import List, Dict, Any


def adicionar_mensagem(request: Request, mensagem: str, tipo: str = "info") -> None:
    """
    Adiciona uma mensagem flash à sessão

    Args:
        request: Objeto Request do FastAPI
        mensagem: Mensagem a ser exibida
        tipo: Tipo da mensagem (success, danger, warning, info)
    """
    if "_mensagens" not in request.session:
        request.session["_mensagens"] = []

    request.session["_mensagens"].append({
        "text": mensagem,
        "type": tipo
    })


def adicionar_mensagem_sucesso(request: Request, mensagem: str) -> None:
    """Adiciona mensagem de sucesso"""
    adicionar_mensagem(request, mensagem, "success")


def adicionar_mensagem_erro(request: Request, mensagem: str) -> None:
    """Adiciona mensagem de erro"""
    adicionar_mensagem(request, mensagem, "danger")


def adicionar_mensagem_aviso(request: Request, mensagem: str) -> None:
    """Adiciona mensagem de aviso"""
    adicionar_mensagem(request, mensagem, "warning")


def adicionar_mensagem_info(request: Request, mensagem: str) -> None:
    """Adiciona mensagem informativa"""
    adicionar_mensagem(request, mensagem, "info")


def obter_mensagens(request: Request) -> List[Dict[str, Any]]:
    """
    Recupera e remove as mensagens flash da sessão

    Args:
        request: Objeto Request do FastAPI

    Returns:
        Lista de mensagens flash
    """
    mensagens = request.session.pop("_mensagens", [])
    return mensagens


# Aliases para compatibilidade
flash = adicionar_mensagem
informar_sucesso = adicionar_mensagem_sucesso
informar_erro = adicionar_mensagem_erro
informar_aviso = adicionar_mensagem_aviso
informar_info = adicionar_mensagem_info
get_flashed_messages = obter_mensagens
