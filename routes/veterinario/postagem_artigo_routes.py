from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from model.postagem_artigo_model import PostagemArtigo
from repo import postagem_artigo_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/artigos/{id_postagem_artigo}")
async def get_artigo_id(id_postagem_artigo: int):
    postagem_artigo = postagem_artigo_repo.obter_por_id(id_postagem_artigo)
    response = templates.TemplateResponse("veterinario/artigo.html", {"request": {}, "postagem_artigo": postagem_artigo})
    return response

@router.get("/veterinario/artigos")
async def get_artigos():
    artigos = postagem_artigo_repo.obter_todos_paginado()
    response = templates.TemplateResponse("veterinario/listar_artigos.html", {"request": {}, "artigos": artigos})
    return response

@router.get("/veterinario/artigo/postar")
async def get_artigo_postar():
    response = templates.TemplateResponse("veterinario/postar_artigo.html", {"request": {}})
    return response

@router.get("/veterinario/artigo/excluir/{id_postagem_artigo}")
async def get_excluir_artigo(id_postagem_artigo: int):
    if postagem_artigo_repo.excluir(id_postagem_artigo):
        return RedirectResponse("/veterinario/artigos", status_code=303)

