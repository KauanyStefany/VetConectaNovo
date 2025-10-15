from fastapi import APIRouter, Request, HTTPException, status, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from model.verificacao_crmv_model import VerificacaoCRMV
from repo import verificacao_crmv_repo
from util.auth_decorator import requer_autenticacao, obter_usuario_logado

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
@requer_autenticacao(perfis_autorizados=["admin"])
async def get_root(request: Request):
    response = templates.TemplateResponse("administrador/home_administrador.html", {"request": request})
    return response

@router.get("/listar_verificação_crmv")
@requer_autenticacao(perfis_autorizados=["admin"])
async def get_listar_verificacao_crmv(request: Request):
    return templates.TemplateResponse("administrador/listar_verificação_crmv.html", {"request": request})

@router.get("/responder_verificação_crmv/{id_verificacao_crmv}")
@requer_autenticacao(perfis_autorizados=["admin"])
async def get_responder_verificacao_crmv(request: Request, id_verificacao_crmv: int):
    return templates.TemplateResponse("administrador/responder_verificação_crmv.html", {"request": request})