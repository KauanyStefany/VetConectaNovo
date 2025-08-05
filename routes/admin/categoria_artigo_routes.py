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
    categoria_artigo = CategoriaArtigo(nome=nome)
    categoria_artigos_por_id = categoria_artigo.inserir(categoria_artigo)
    if categoria_artigos_por_id:
        return templates.TemplateResponse("admin/cadastrar_categoria_artigo.html", {"request": {}, "mensagem": "Categoria de artigo cadastrada com sucesso!"})
    return templates.TemplateResponse("admin/cadastrar_categoria_artigo.html", {"request": {}, "mensagem": "Erro ao cadastrar categoria de artigo."})

@router.get("/admin/categoria_artigo/alterar/{categoria_artigo_id}")
async def get_alterar_categoria_artigo_(categoria_artigo_id: int):
    categoria_artigo = categoria_artigo_repo.obter_categoria_por_id(categoria_artigo_id)
    if categoria_artigo:
        response = templates.TemplateResponse("admin/alterar_categoria_artigo.html", {"request": {}, "categoria": categoria_artigo})
        return response
    return templates.TemplateResponse("admin/listar_categoria_artigo.html", {"request": {}, "mensagem": "Categoria de artigo não encontrada."})

@router.post("/admin/categoria_artigo/alterar")
async def post_alterar_categoria_artigo(categoria_artigo_id: int, nome: str):
    categoria_artigo = CategoriaArtigo(id_categoria_artigo=categoria_artigo_id, nome=nome)
    if categoria_artigo_repo.atualizar_categoria(categoria_artigo):
        return templates.TemplateResponse("admin/listar_categoria_artigo.html", {"request": {}, "mensagem": "Categoria de artigo atualizada com sucesso!"})
    return templates.TemplateResponse("admin/alterar_categoria_artigo.html", {"request": {}, "mensagem": "Erro ao atualizar categoria de artigo."})

@router.get("/admin/categoria_artigo/excluir/{categoria_artigo_id}")
async def get_excluir_categoria_artigo(categoria_artigo_id: int):
    