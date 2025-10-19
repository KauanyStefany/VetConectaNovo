"""
Rota de demonstração do sistema de toasts
Exemplo prático de uso do sistema de mensagens
"""

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from util.template_util import criar_templates
from util.mensagens import (
    adicionar_mensagem_sucesso,
    adicionar_mensagem_erro,
    adicionar_mensagem_aviso,
    adicionar_mensagem_info
)

router = APIRouter(prefix="/demo-toasts", tags=["Demo"])
templates = criar_templates()


@router.get("/")
async def pagina_demo(request: Request):
    """
    Página de demonstração do sistema de toasts
    """
    return templates.TemplateResponse("publico/demo_toasts.html", {
        "request": request
    })


@router.post("/sucesso")
async def demo_sucesso(request: Request):
    """
    Demonstra mensagem de sucesso
    """
    adicionar_mensagem_sucesso(request, "Operação realizada com sucesso!")
    return RedirectResponse(url="/demo-toasts/", status_code=302)


@router.post("/erro")
async def demo_erro(request: Request):
    """
    Demonstra mensagem de erro
    """
    adicionar_mensagem_erro(request, "Erro ao processar a requisição. Tente novamente.")
    return RedirectResponse(url="/demo-toasts/", status_code=302)


@router.post("/aviso")
async def demo_aviso(request: Request):
    """
    Demonstra mensagem de aviso
    """
    adicionar_mensagem_aviso(request, "Atenção: esta ação não pode ser desfeita!")
    return RedirectResponse(url="/demo-toasts/", status_code=302)


@router.post("/info")
async def demo_info(request: Request):
    """
    Demonstra mensagem informativa
    """
    adicionar_mensagem_info(request, "Informação: os dados foram atualizados recentemente")
    return RedirectResponse(url="/demo-toasts/", status_code=302)


@router.post("/multiplas")
async def demo_multiplas(request: Request):
    """
    Demonstra múltiplas mensagens
    """
    adicionar_mensagem_sucesso(request, "Arquivo enviado com sucesso")
    adicionar_mensagem_info(request, "Processamento iniciado")
    adicionar_mensagem_aviso(request, "Você receberá um e-mail ao concluir")
    return RedirectResponse(url="/demo-toasts/", status_code=302)
