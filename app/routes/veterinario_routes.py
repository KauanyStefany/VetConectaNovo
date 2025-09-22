from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.core.auth_decorator import requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("veterinario/dashboard.html", {"request": request, "usuario": usuario_logado})
    return response

# Rotas de artigos
@router.get("/artigos")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def listar_artigos(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("veterinario/artigos/listar.html", {"request": request, "usuario": usuario_logado})

@router.get("/artigos/criar")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def criar_artigo(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("veterinario/artigos/criar.html", {"request": request, "usuario": usuario_logado})

@router.get("/artigos/editar/{id_postagem_artigo}")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def editar_artigo(request: Request, id_postagem_artigo: int, usuario_logado: dict = None):
    return templates.TemplateResponse("veterinario/artigos/editar.html", {"request": request, "usuario": usuario_logado, "id_artigo": id_postagem_artigo})

@router.get("/artigos/visualizar/{id_postagem_artigo}")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def visualizar_artigo(request: Request, id_postagem_artigo: int, usuario_logado: dict = None):
    return templates.TemplateResponse("veterinario/artigos/visualizar.html", {"request": request, "usuario": usuario_logado, "id_artigo": id_postagem_artigo})

@router.get("/artigos/excluir/{id_postagem_artigo}")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def excluir_artigo(request: Request, id_postagem_artigo: int, usuario_logado: dict = None):
    return templates.TemplateResponse("veterinario/excluir_postagem_artigo.html", {"request": request, "usuario": usuario_logado, "id_artigo": id_postagem_artigo})

# Rotas de estatísticas
@router.get("/estatisticas")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def estatisticas(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("veterinario/estatisticas.html", {"request": request, "usuario": usuario_logado})

# Rotas de solicitação CRMV
@router.get("/crmv/solicitar")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def solicitar_crmv(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("veterinario/solicitacao_crmv.html", {"request": request, "usuario": usuario_logado})

@router.get("/crmv/status")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def status_crmv(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("veterinario/obter_solicitacao_crmv.html", {"request": request, "usuario": usuario_logado})

# Rotas de chamados
@router.get("/chamados")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def chamados(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("veterinario/chamados.html", {"request": request, "usuario": usuario_logado})