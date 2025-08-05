from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

from model.categoria_artigo_model import CategoriaArtigo
from repo import categoria_artigo_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/admin/categoria_artigo/listar")
async def get_categoria_artigos():
    categorias_artigo = categoria_artigo_repo.obter_categorias_paginado()
    response = templates.TemplateResponse("admin/listar_categoria_artigo.html", {"request": {}, "categorias_artigo": categorias_artigo})
    return response

@router.get("/admin/categoria_artigo/cadastrar")
async def get_categoria_artigo_cadastrar():
    response = templates.TemplateResponse("admin/cadastrar_categoria_artigo.html", {"request": {}})
    return response

@router.post("/admin/categoria_artigo/cadastrar")
async def post_categoria_artigo_cadastrar(nome: str):