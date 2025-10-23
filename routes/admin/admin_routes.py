from fastapi import APIRouter, Request
from util.auth_decorator import requer_autenticacao
from util.template_util import criar_templates

router = APIRouter()
templates = criar_templates()

@router.get("/dashboard")
@requer_autenticacao(perfis_autorizados=["admin"])
async def get_dashboard(request: Request, usuario_logado: dict = None):
    """Dashboard principal do administrador"""
    return templates.TemplateResponse(
        "administrador/home_administrador_simple.html", 
        {"request": request}
    )
