from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from model.categoria_artigo_model import CategoriaArtigo
from repo import categoria_artigo_repo
from util.auth_decorator import requer_autenticacao, obter_usuario_logado
from util.mensagens import adicionar_mensagem_sucesso
from util.mensagens import adicionar_mensagem_sucesso, adicionar_mensagem_erro


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
@requer_autenticacao(perfis_autorizados=["admin"])
async def get_root(request: Request):
    # TODO: BUG #3 - Corrigir objeto request vazio
    # PROBLEMA: Na linha abaixo, "request": {} está vazio (dicionário vazio)
    # SOLUÇÃO: Trocar {} por request (sem aspas, é a variável request do parâmetro)
    # CORRETO: {"request": request, "categoria_artigo": categoria_artigo}
    categoria_artigo = categoria_artigo_repo.obter_pagina(limite=10, offset=0)
    response = templates.TemplateResponse("administrador/home_administrador.html", {"request": request, "categoria_artigo": categoria_artigo})
    return response

@router.get("/listar_categorias")
@requer_autenticacao(perfis_autorizados=["admin"])
async def get_listar_categorias(request: Request):
    # TODO: Buscar todas as categorias do banco de dados
    # PASSO 1: Chamar categoria_artigo_repo.obter_todos()
    # PASSO 2: Adicionar a variável 'categorias' no context do template
    # EXEMPLO: categorias = categoria_artigo_repo.obter_todos()
    #          return templates.TemplateResponse("...", {"request": request, "categorias": categorias})
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
        # TODO: BUG #1 - Redirect aponta para arquivo HTML em vez de rota
        # PROBLEMA: "/administrador/cadastrar_categoria.html" é um caminho de arquivo, não uma rota
        # SOLUÇÃO: Trocar por "/administrador/listar_categorias" (rota que lista as categorias)
        # OPCIONAL: Adicionar mensagem de sucesso com util.mensagens.adicionar_mensagem_sucesso()
        adicionar_mensagem_sucesso(request, "Categoria cadastrada com sucesso!")
        response = RedirectResponse("/administrador/listar_categorias", status_code=303)
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
    # TODO: BUG #2 - A exclusão não está sendo executada
    # PROBLEMA: O código apenas verifica se a categoria existe, mas não exclui
    # SOLUÇÃO:
    #   1. Verificar se categoria existe (já feito)
    #   2. SE NÃO EXISTIR: retornar erro
    #   3. SE EXISTIR: chamar categoria_artigo_repo.excluir(id_categoria)
    #   4. Verificar se exclusão foi bem sucedida
    #   5. Adicionar mensagem de sucesso ou erro
    # EXEMPLO:
    #   from util.mensagens import adicionar_mensagem_sucesso, adicionar_mensagem_erro
    #   categoria = categoria_artigo_repo.obter_por_id(id_categoria)
    #   if not categoria:
    #       adicionar_mensagem_erro(request, "Categoria não encontrada.")
    #   elif categoria_artigo_repo.excluir(id_categoria):
    #       adicionar_mensagem_sucesso(request, "Categoria excluída com sucesso!")
    #   else:
    #       adicionar_mensagem_erro(request, "Erro ao excluir. Pode haver artigos vinculados.")
    #   return RedirectResponse("/administrador/listar_categorias", status_code=303)
    categoria = categoria_artigo_repo.obter_por_id(id_categoria)
    if not categoria:
        adicionar_mensagem_erro(request, "Categoria não encontrada.")
    elif categoria_artigo_repo.excluir(id_categoria):
        adicionar_mensagem_sucesso(request, "Categoria excluída com sucesso!")
    else:
        adicionar_mensagem_erro(request, "Erro ao excluir. Pode haver artigos vinculados.")

    return RedirectResponse("/administrador/listar_categorias", status_code=303)