from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.database.models.comentario_model import Comentario
from app.database.repositories import comentario_repo
from app.core.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
@requer_autenticacao(perfis_autorizados=["tutor"])
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("tutor/feed.html", {"request": request, "usuario": usuario_logado})
    return response

@router.get("/feed")
@requer_autenticacao(perfis_autorizados=["tutor"])
async def feed(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("tutor/feed.html", {"request": request, "usuario": usuario_logado})

@router.get("/listar_postagem_feed")
@requer_autenticacao(perfis_autorizados=["tutor"])
async def pagina_listar_postagem_feed(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("tutor/listar_postagens_feed.html", {"request": request, "usuario": usuario_logado})

@router.get("/fazer_postagem_feed")
@requer_autenticacao(perfis_autorizados=["tutor"])
async def pagina_fazer_postagem_feed(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("tutor/nova_postagem.html", {"request": request, "usuario": usuario_logado})

@router.get("/excluir_postagem_feed")
@requer_autenticacao(perfis_autorizados=["tutor"])
async def pagina_excluir_postagem_feed(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("tutor/excluir_postagem_feed.html", {"request": request, "usuario": usuario_logado})

@router.get("/meus_pets")
@requer_autenticacao(perfis_autorizados=["tutor"])
async def meus_pets(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("tutor/meus_pets.html", {"request": request, "usuario": usuario_logado})