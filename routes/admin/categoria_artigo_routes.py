from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from model.categoria_artigo_model import CategoriaArtigo
from repo import categoria_artigo_repo
from util.auth_decorator import requer_autenticacao, obter_usuario_logado


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
@requer_autenticacao(perfis_autorizados=["admin"])
async def get_root(request: Request):
    categoria_artigo = categoria_artigo_repo.obter_pagina(limite=10, offset=0)
    response = templates.TemplateResponse("administrador/home_administrador.html", {"request": {}, "categoria_artigo": categoria_artigo})
    return response

@router.get("/listar_categorias")
@requer_autenticacao(perfis_autorizados=["admin"])
async def get_listar_categorias(request: Request):
    return templates.TemplateResponse("administrador/listar_categorias.html", {"request": request})

@router.get("/alterar_categoria/{id_categoria}")
@requer_autenticacao(perfis_autorizados=["admin"])
async def get_alterar_categoria(request: Request, id_categoria: int):
    categoria_artigo = categoria_artigo_repo.obter_por_id(id_categoria)
    if categoria_artigo:
        response = templates.TemplateResponse("administrador/alterar_categoria.html", {"request": request, "categoria_artigo": categoria_artigo})
        return response
    return templates.TemplateResponse("administrador/alterar_categoria.html", {"request": {}, "mensagem": "Categoria não encontrada."})

@router.post("/alterar_categoria")
@requer_autenticacao(perfis_autorizados=["admin"])
async def post_categoria_alterar(
    request: Request,
    id_categoria: int = Form(...),
    nome: str = Form(...),
    cor: str = Form(...),
    imagem: str = Form(...)):
    categoria = CategoriaArtigo(id_categoria_artigo=id_categoria, nome=nome, cor=cor, imagem=imagem)
    if categoria_artigo_repo.atualizar(categoria):
        response = RedirectResponse("/administrador/categorias", status_code=303)
        return response
    return templates.TemplateResponse("administrador/alterar_categoria.html", {"request": request, "mensagem": "Erro ao alterar categoria."})


@router.get("/cadastrar_categoria")
@requer_autenticacao(perfis_autorizados=["admin"])
async def get_cadastrar_categoria(request: Request):
    response = templates.TemplateResponse("administrador/cadastrar_categoria.html", {"request": request})
    return response


@router.post("/cadastrar_categoria")
@requer_autenticacao(perfis_autorizados=["admin"])
async def post_categoria_artigor(request: Request, nome: str = Form(...), cor: str = Form(...), imagem: str = Form(...)):
    categoria = CategoriaArtigo(id_categoria_artigo=0, nome=nome, cor=cor, imagem=imagem)
    id_categoria = categoria_artigo_repo.inserir(categoria)
    if id_categoria:
        response = RedirectResponse("/administrador/cadastrar_categoria.html", status_code=303)
        return response
    return templates.TemplateResponse("administrador/cadastrar_categoria.html", {"request": request, "mensagem": "Erro ao cadastrar categoria."})


@router.get("/excluir_categoria/{id_categoria}")
@requer_autenticacao(perfis_autorizados=["admin"])
async def get_categoria_excluir(request: Request, id_categoria: int):
    categoria_artigo = categoria_artigo_repo.obter_por_id(id_categoria)
    if categoria_artigo:
        response = templates.TemplateResponse("administrador/excluir_categoria.html", {"request": request, "categoria_artigo": categoria_artigo})
        return response
    return RedirectResponse("/administrador/categorias", status_code=303)


@router.post("/excluir_categoria")
@requer_autenticacao(perfis_autorizados=["admin"])
async def post_categoria_excluir(
    request: Request,
    id_categoria: int = Form(...)):
    if categoria_artigo_repo.obter_por_id(id_categoria):
        response = RedirectResponse("/administrador/categorias", status_code=303)
        return response
    return templates.TemplateResponse("administrador/excluir_categoria.html", {"request": request, "mensagem": "Erro ao excluir categoria."})