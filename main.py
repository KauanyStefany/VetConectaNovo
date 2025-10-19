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

# Inícialização do servidor
if __name__ == "__main__":
    environment = os.getenv("ENVIRONMENT", "development")
    logger.info("Iniciando aplicação VetConecta")
    logger.info(f"Ambiente: {environment}")
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)
