from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from util.auth_decorator import requer_autenticacao, obter_usuario_logado

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def get_root(request: Request):
    response = templates.TemplateResponse("veterinario/veterinario_home.html", {"request": request})
    return response

@router.get("/listar_estatisticas")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def pagina_postagem_artigo(request: Request):
    return templates.TemplateResponse("veterinario/listar_estatisticas.html", {"request": request})
