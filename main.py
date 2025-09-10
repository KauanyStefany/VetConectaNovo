from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from starlette.middleware.sessions import SessionMiddleware
import secrets

from routes.admin import categoria_artigo_routes, chamado_routes, comentario_admin_routes, denuncia_admin_routes, chamado_routes, verificação_crmv_routes
from routes.publico import auth_routes, perfil_routes, public_routes
from routes.tutor import postagem_feed_routes
from routes.usuario import usuario_routes
from routes.veterinario import estatisticas_routes, postagem_artigo_routes, solicitacao_crmv_routes




app = FastAPI()

# Gerar chave secreta (em produção, use variável de ambiente!)
SECRET_KEY = secrets.token_urlsafe(32)

# Adicionar middleware de sessão
app.add_middleware(
    SessionMiddleware, 
    secret_key=SECRET_KEY,
    max_age=3600,  # Sessão expira em 1 hora
    same_site="lax",
    https_only=False  # Em produção, mude para True com HTTPS
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(public_routes.router)
app.include_router(auth_routes.router)

app.include_router(categoria_artigo_routes.router, prefix="/admin")
app.include_router(chamado_routes.router, prefix="/admin")
app.include_router(comentario_admin_routes.router, prefix="/admin")
app.include_router(denuncia_admin_routes.router, prefix="/admin")
app.include_router(chamado_routes.router, prefix="/admin")
app.include_router(verificação_crmv_routes.router, prefix="/admin")

app.include_router(postagem_feed_routes.router, prefix="/tutor")
# app.include_router(denuncia_veterinario_routes.router, prefix="/veterinario")
app.include_router(postagem_artigo_routes.router, prefix="/veterinario")
# app.include_router(seguida_veterinario_routes.router, prefix="/veterinario") 
app.include_router(estatisticas_routes.router, prefix="/veterinario")
app.include_router(solicitacao_crmv_routes.router, prefix="/veterinario")

app.include_router(usuario_routes.router, prefix="/usuario")
app.include_router(perfil_routes.router, prefix="/perfil")

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)