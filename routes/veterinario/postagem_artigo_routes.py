from fastapi import APIRouter, Request
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

@router.get("/cadastrar_postagem_artigo")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def get_cadastrar_postagem_artigo(request: Request):
    return templates.TemplateResponse("veterinario/cadastrar_postagem_artigo.html", {"request": request})

@router.get("/excluir_postagem_artigo/{id_postagem_artigo}")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def get_excluir_postagem_artigo(request: Request, id_postagem_artigo: int):
    return templates.TemplateResponse("veterinario/excluir_postagem_artigo.html", {"request": request})