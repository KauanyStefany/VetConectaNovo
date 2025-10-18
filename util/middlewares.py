"""
Módulo de configuração de middlewares para a aplicação VetConecta.
"""

import os
import secrets
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware


def obter_secret_key() -> str:
    """
    Obtém a chave secreta da variável de ambiente ou gera uma temporária.

    Returns:
        str: Chave secreta para uso em sessões e tokens
    """
    secret_key = os.getenv("SECRET_KEY")
    if not secret_key:
        # Em desenvolvimento, gerar uma chave temporária com aviso
        secret_key = secrets.token_urlsafe(32)
        print("⚠️  AVISO: SECRET_KEY não configurada. Usando chave temporária.")
        print("⚠️  Defina a variável de ambiente SECRET_KEY para produção!")
    return secret_key


def configurar_rate_limiter(app: FastAPI) -> Limiter:
    """
    Configura o rate limiter para a aplicação.

    Args:
        app: Instância do FastAPI

    Returns:
        Limiter: Instância configurada do rate limiter
    """
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=["200/hour"],  # Limite padrão global
        storage_uri="memory://",  # Usar Redis em produção
    )
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore[arg-type]
    return limiter


async def security_headers_middleware(request: Request, call_next):
    """Adiciona headers de segurança nas respostas"""
    response = await call_next(request)

    environment = os.getenv("ENVIRONMENT", "development")

    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"

    if environment == "production":
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )

    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
        "img-src 'self' data: https:; "
        "font-src 'self' data: https://cdn.jsdelivr.net https://fonts.gstatic.com; "
        "connect-src 'self' https://cdn.jsdelivr.net"
    )
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

    return response


async def log_requests_middleware(request: Request, call_next):
    """Loga requisições (sem dados sensíveis)"""
    req_logger = logging.getLogger("vetconecta.requests")

    # Não logar senhas ou tokens
    safe_path = request.url.path
    if "senha" not in safe_path.lower() and "password" not in safe_path.lower():
        req_logger.info(
            f"{request.method} {safe_path} - {request.client.host if request.client else 'unknown'}"
        )

    response = await call_next(request)
    return response


def configurar_middlewares(app: FastAPI) -> None:
    """
    Configura todos os middlewares da aplicação.

    Args:
        app: Instância do FastAPI
    """
    # Obter variáveis de ambiente
    environment = os.getenv("ENVIRONMENT", "development")
    secret_key = obter_secret_key()

    # Configurar rate limiter
    configurar_rate_limiter(app)

    # Middleware de segurança - Trusted Host
    allowed_hosts = ["localhost", "127.0.0.1", "*.vetconecta.com"]
    if environment == "development":
        allowed_hosts.append("*")  # Aceitar todos em desenvolvimento
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)

    # Middleware de segurança - CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=(
            ["http://localhost:8000"] if environment == "production" else ["*"]
        ),
        allow_credentials=True,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )

    # Middleware de rate limiting
    app.add_middleware(SlowAPIMiddleware)

    # Middleware de sessão
    app.add_middleware(
        SessionMiddleware,
        secret_key=secret_key,
        max_age=3600,  # Sessão expira em 1 hora
        same_site="strict" if environment == "production" else "lax",
        https_only=(environment == "production"),  # HTTPS obrigatório em produção
    )

    # Middleware de segurança customizado - Security Headers
    app.middleware("http")(security_headers_middleware)

    # Middleware de logging
    app.middleware("http")(log_requests_middleware)
