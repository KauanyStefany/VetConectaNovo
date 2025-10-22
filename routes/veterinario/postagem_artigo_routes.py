from tkinter.tix import Form
from fastapi import APIRouter, File, Request, UploadFile
from fastapi.params import Query
from fastapi.templating import Jinja2Templates

from repo import postagem_artigo_repo
from util.auth_decorator import requer_autenticacao, obter_usuario_logado
from util.template_util import criar_templates

router = APIRouter(prefix="/veterinario")
templates = criar_templates("templates/veterinario")

@router.get("/")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def get_home_veterinario(request: Request, usuario_logado: dict = None):
    artigos = postagem_artigo_repo.obter_por_veterinario(usuario_logado['id'])  # Criar
    # Calcular estatísticas
    total_visualizacoes = sum(a.visualizacoes for a in artigos)
    # Buscar curtidas totais (criar query)

    return templates.TemplateResponse("veterinario/veterinario_home.html", {
        "request": request,
        "artigos": artigos,
        "total_artigos": len(artigos),
        "total_visualizacoes": total_visualizacoes
    })

@router.get("/listar_postagem_artigo")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def get_listar_postagem_artigo(request: Request):
    return templates.TemplateResponse("veterinario/listar_postagem_artigo.html", {"request": request})

@router.get("/alterar_postagem_artigo/{id_postagem_artigo}")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def get_alterar_postagem_artigo(request: Request, id_postagem_artigo: int):
    return templates.TemplateResponse("veterinario/alterar_postagem_artigo.html", {"request": request})

@router.get("/obter_solicitacao_crmv")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def get_obter_solicitacao_crmv(request: Request):
    return templates.TemplateResponse("veterinario/obter_solicitacao_crmv.html", {"request": request})

@router.get("/fazer_solicitacao_crmv")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def get_fazer_solicitacao_crmv(request: Request):
    return templates.TemplateResponse("veterinario/fazer_solicitacao_crmv.html", {"request": request})

@router.get("/buscar_artigos")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def get_buscar_artigos(
    request: Request,
    q: str = Query(None, min_length=3),
    usuario_logado: dict = None
):
    """Busca nos artigos do veterinário logado"""
    if not q:
        return templates.TemplateResponse("veterinario/buscar_artigos.html", {
            "request": request,
            "termo": "",
            "artigos": []
        })
    
    # Buscar todos os artigos
    artigos = postagem_artigo_repo.buscar_por_termo(q.strip())
    
    # Filtrar apenas os do veterinário logado
    artigos_filtrados = [
        a for a in artigos 
        if a['id_veterinario'] == usuario_logado['id']
    ]
    
    return templates.TemplateResponse("veterinario/buscar_artigos.html", {
        "request": request,
        "termo": q.strip(),
        "artigos": artigos_filtrados
    })