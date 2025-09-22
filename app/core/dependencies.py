from fastapi import Depends, HTTPException, status, Request
from app.database.connection import get_connection
from app.core.auth_decorator import obter_usuario_logado
from typing import Optional


async def get_db():
    """Dependência para obter conexão com banco de dados"""
    return get_connection()


async def get_current_user(request: Request) -> Optional[dict]:
    """Dependência para obter usuário logado (opcional)"""
    return obter_usuario_logado(request)


async def require_authenticated_user(request: Request) -> dict:
    """Dependência para exigir usuário autenticado"""
    user = obter_usuario_logado(request)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não autenticado"
        )
    return user


async def require_admin_user(request: Request) -> dict:
    """Dependência para exigir usuário administrador"""
    user = await require_authenticated_user(request)
    if user.get("perfil") not in ["admin", "administrador"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado - privilégios de administrador necessários"
        )
    return user


async def require_veterinarian_user(request: Request) -> dict:
    """Dependência para exigir usuário veterinário"""
    user = await require_authenticated_user(request)
    if user.get("perfil") != "veterinario":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado - apenas veterinários"
        )
    return user


async def require_tutor_user(request: Request) -> dict:
    """Dependência para exigir usuário tutor"""
    user = await require_authenticated_user(request)
    if user.get("perfil") != "tutor":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado - apenas tutores"
        )
    return user