from routes.tutor import postagem_feed_routes
from routes.publico import perfil_routes
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from dotenv import load_dotenv

from util.db_util import inicializar_banco
from routes.publico import auth_routes, public_routes
from util.middlewares import configurar_middlewares
from routes.admin import (
    admin_routes,
    categoria_artigo_routes,
    chamado_routes,
    comentario_admin_routes,
    denuncia_admin_routes,
    verificacao_crmv_routes
)

from routes.veterinario import (
    postagem_artigo_routes,
    solicitacao_crmv_routes,
    estatisticas_routes
)

from routes.usuario import usuario_routes
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

# Inicializar banco de dados
inicializar_banco()

# Inicializar FastAPI
app = FastAPI(
    title="VetConecta",
    description="Plataforma de conexão veterinária",
    version="1.0.0"
)

# Configurar middlewares
configurar_middlewares(app)

# Montar arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir rotas
app.include_router(public_routes.router)
app.include_router(auth_routes.router)

# Rotas públicas adicionais
app.include_router(perfil_routes.router, prefix="/perfil", tags=["perfil"])

# Rotas admin
app.include_router(admin_routes.router, prefix="/admin", tags=["admin"])
app.include_router(categoria_artigo_routes.router, prefix="/administrador", tags=["admin-categorias"])
app.include_router(chamado_routes.router, prefix="/administrador", tags=["admin-chamados"])
app.include_router(comentario_admin_routes.router, prefix="/administrador", tags=["admin-comentarios"])
app.include_router(denuncia_admin_routes.router, prefix="/administrador", tags=["admin-denuncias"])
app.include_router(verificacao_crmv_routes.router, prefix="/administrador", tags=["admin-crmv"])

# Rotas tutor
app.include_router(postagem_feed_routes.router, prefix="/tutor", tags=["tutor"])

# Rotas veterinário
app.include_router(postagem_artigo_routes.router, prefix="/veterinario", tags=["veterinario-artigos"])
app.include_router(solicitacao_crmv_routes.router, prefix="/veterinario", tags=["veterinario-crmv"])
app.include_router(estatisticas_routes.router, prefix="/veterinario", tags=["veterinario-stats"])

# Rotas usuário
app.include_router(usuario_routes.router, prefix="/usuario", tags=["usuario"])

# Inícialização do servidor
if __name__ == "__main__":
    environment = os.getenv("ENVIRONMENT", "development")
    logger.info("Iniciando aplicação VetConecta")
    logger.info(f"Ambiente: {environment}")
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
