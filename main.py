from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from starlette.middleware.sessions import SessionMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
import secrets
import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Handler para arquivo
file_handler = RotatingFileHandler(
    "logs/app.log", maxBytes=10 * 1024 * 1024, backupCount=5  # 10MB
)
file_handler.setLevel(logging.INFO)

# Handler para console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)

# Formato
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Configurar logger raiz
logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])

# Logger específico para aplicação
logger = logging.getLogger(__name__)

from repo import administrador_repo, tutor_repo, usuario_repo, veterinario_repo
from app.routes.admin import (
    categorias,
    chamados,
    comentarios,
    denuncias,
    verificacoes_crmv,
)
from app.routes.publico import auth, perfil, public
from app.routes.tutor import postagens_feed
from app.routes.usuario import usuario
from app.routes.veterinario import estatisticas, artigos, solicitacoes_crmv


usuario_repo.criar_tabela()
tutor_repo.criar_tabela()
veterinario_repo.criar_tabela()
administrador_repo.criar_tabela()

# Inicializar FastAPI
app = FastAPI(
    title="VetConecta",
    description="Plataforma de conexão veterinária",
    version="1.0.0",
    docs_url="/api/docs" if os.getenv("ENVIRONMENT") == "development" else None,
    redoc_url="/api/redoc" if os.getenv("ENVIRONMENT") == "development" else None,
)

# Obter chave secreta da variável de ambiente
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    # Em desenvolvimento, gerar uma chave temporária com aviso
    SECRET_KEY = secrets.token_urlsafe(32)
    print("⚠️  AVISO: SECRET_KEY não configurada. Usando chave temporária.")
    print("⚠️  Defina a variável de ambiente SECRET_KEY para produção!")

# Determinar ambiente
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Configurar rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200/hour"],  # Limite padrão global
    storage_uri="memory://",  # Usar Redis em produção
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore[arg-type]

# Middleware de segurança - Trusted Host
allowed_hosts = ["localhost", "127.0.0.1", "*.vetconecta.com"]
if ENVIRONMENT == "development":
    allowed_hosts.append("*")  # Aceitar todos em desenvolvimento
app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)

# Middleware de segurança - CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"] if ENVIRONMENT == "production" else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Middleware de rate limiting
app.add_middleware(SlowAPIMiddleware)

# Middleware de sessão
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    max_age=3600,  # Sessão expira em 1 hora
    same_site="strict" if ENVIRONMENT == "production" else "lax",
    https_only=(ENVIRONMENT == "production"),  # HTTPS obrigatório em produção
)


# Middleware de segurança customizado - Security Headers
@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    """Adiciona headers de segurança nas respostas"""
    response = await call_next(request)

    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"

    if ENVIRONMENT == "production":
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )

    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self' data:; "
        "connect-src 'self'"
    )
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

    return response


# Middleware de logging
@app.middleware("http")
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


app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(public.router)
app.include_router(auth.router)

app.include_router(categorias.router, prefix="/admin")
app.include_router(chamados.router, prefix="/admin")
app.include_router(comentarios.router, prefix="/admin")
app.include_router(denuncias.router, prefix="/admin")
app.include_router(verificacoes_crmv.router, prefix="/admin")

app.include_router(postagens_feed.router, prefix="/tutor")
app.include_router(artigos.router, prefix="/veterinario")
app.include_router(estatisticas.router, prefix="/veterinario")
app.include_router(solicitacoes_crmv.router, prefix="/veterinario")

app.include_router(usuario.router, prefix="/usuario")
app.include_router(perfil.router, prefix="/perfil")

if __name__ == "__main__":
    logger.info("Iniciando aplicação VetConecta")
    logger.info(f"Ambiente: {ENVIRONMENT}")
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
