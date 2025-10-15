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

@router.get("/obter_solicitacao_crmv")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def get_obter_solicitacao_crmv(request: Request):
    return templates.TemplateResponse("veterinario/obter_solicitacao_crmv.html", {"request": request})

@router.get("/fazer_solicitacao_crmv")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def get_fazer_solicitacao_crmv(request: Request):
    return templates.TemplateResponse("veterinario/fazer_solicitacao_crmv.html", {"request": request})
