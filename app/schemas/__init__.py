"""
Pacote de DTOs do sistema.

Este módulo centraliza todos os DTOs (Data Transfer Objects) organizados por funcionalidade:
- BaseDTO: Classe base com configurações comuns
- usuario_dto: DTOs relacionados a usuários

Imports facilitados para os DTOs mais comuns:
"""

# Base
from .base_dto import BaseDTO

# Usuário
from .usuario_dto import (
    CriarUsuarioDTO,
    AtualizarUsuarioDTO
)

__all__ = [
    # Base
    'BaseDTO',

    # Usuário
    'CriarUsuarioDTO',
    'AtualizarUsuarioDTO',
]