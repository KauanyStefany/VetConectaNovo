from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from starlette.middleware.sessions import SessionMiddleware

from app.core.config import settings
from app.database.repositories import administrador_repo, tutor_repo, usuario_repo, veterinario_repo
from app.routes import auth_routes, public_routes, usuario_routes, tutor_routes, veterinario_routes, admin_routes


# Criar tabelas do banco de dados
usuario_repo.criar_tabela_usuario()
tutor_repo.criar_tabela_tutor()
veterinario_repo.criar_tabela_veterinario()
administrador_repo.criar_tabela_administrador()

app = FastAPI(title="VetConecta", version="1.0.0")

# Adicionar middleware de sessão
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    max_age=settings.SESSION_MAX_AGE,
    same_site="lax",
    https_only=False  # Em produção, mude para True com HTTPS
)

# Servir arquivos estáticos
app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

# Incluir rotas
app.include_router(public_routes.router)
app.include_router(auth_routes.router)
app.include_router(usuario_routes.router, prefix="/usuario")
app.include_router(tutor_routes.router, prefix="/tutor")
app.include_router(veterinario_routes.router, prefix="/veterinario")
app.include_router(admin_routes.router, prefix="/admin")

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)