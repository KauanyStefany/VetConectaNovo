from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
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
from util.middlewares import configurar_middlewares


usuario_repo.criar_tabela()
tutor_repo.criar_tabela()
veterinario_repo.criar_tabela()
administrador_repo.criar_tabela()

# Inicializar FastAPI
app = FastAPI(
    title="VetConecta",
    description="Plataforma de conexão veterinária",
    version="1.0.0"
)

# Configurar middlewares
configurar_middlewares(app)


app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(public.router)
# app.include_router(auth.router)

# app.include_router(categorias.router, prefix="/admin")
# app.include_router(chamados.router, prefix="/admin")
# app.include_router(comentarios.router, prefix="/admin")
# app.include_router(denuncias.router, prefix="/admin")
# app.include_router(verificacoes_crmv.router, prefix="/admin")

# app.include_router(postagens_feed.router, prefix="/tutor")
# app.include_router(artigos.router, prefix="/veterinario")
# app.include_router(estatisticas.router, prefix="/veterinario")
# app.include_router(solicitacoes_crmv.router, prefix="/veterinario")

# app.include_router(usuario.router, prefix="/usuario")
# app.include_router(perfil.router, prefix="/perfil")

if __name__ == "__main__":
    environment = os.getenv("ENVIRONMENT", "development")
    logger.info("Iniciando aplicação VetConecta")
    logger.info(f"Ambiente: {environment}")
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
