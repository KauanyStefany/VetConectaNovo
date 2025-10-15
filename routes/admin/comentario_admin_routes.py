from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from repo import comentario_repo
from util.auth_decorator import requer_autenticacao, obter_usuario_logado

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
@requer_autenticacao(perfis_autorizados=["admin"])
async def get_root(request: Request):
    response = templates.TemplateResponse("administrador/home_administrador.html", {"request": request})
    return response


@router.get("/moderar_comentarios/{id_comentario}")
@requer_autenticacao(perfis_autorizados=["admin"])
async def pagina_comentario(request: Request, id_comentario: int):
    return templates.TemplateResponse("administrador/moderar_comentarios.html", {"request": request})