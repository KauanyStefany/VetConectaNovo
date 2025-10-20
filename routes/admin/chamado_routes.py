from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from util.auth_decorator import requer_autenticacao, obter_usuario_logado

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
@requer_autenticacao(perfis_autorizados=["admin"])
async def get_root(request: Request):
    response = templates.TemplateResponse("administrador/home_administrador.html", {"request": request})
    return response

@router.get("/listar_chamados")
@requer_autenticacao(perfis_autorizados=["admin"])
async def get_listar_chamados(request: Request):
    # TODO: Implementar listagem de chamados
    # PASSOS:
    #   1. Importar: from repo import chamado_repo
    #   2. Buscar chamados: chamados = chamado_repo.obter_pagina(limite=20, offset=0)
    #   3. Contar total: total = chamado_repo.contar_total() (criar esta função em repo/chamado_repo.py)
    #   4. Passar para template: {"request": request, "chamados": chamados, "total": total}
    # OPCIONAL: Implementar filtro por status com query param ?status=...
    # Ver PENDENCIAS.md seção 4.2 para código completo
    return templates.TemplateResponse("administrador/listar_chamados.html", {"request": request})

@router.get("/responder_chamado/{id_chamado}")
@requer_autenticacao(perfis_autorizados=["admin"])
async def get_responder_chamado(request: Request, id_chamado: int):
    # TODO: Implementar GET para responder chamado
    # PASSOS:
    #   1. Importar: from repo import chamado_repo, resposta_chamado_repo
    #   2. Buscar chamado: chamado = chamado_repo.obter_por_id(id_chamado)
    #   3. Se não existe: adicionar_mensagem_erro e redirecionar para lista
    #   4. Buscar respostas anteriores: respostas = resposta_chamado_repo.obter_por_chamado(id_chamado)
    #      ATENÇÃO: Criar função obter_por_chamado() em repo/resposta_chamado_repo.py
    #   5. Retornar template com: chamado e respostas
    # Ver PENDENCIAS.md seção 4.2 para código completo
    return templates.TemplateResponse("administrador/responder_chamado.html", {"request": request})

@router.get("/excluir_chamado/{id_chamado}")
@requer_autenticacao(perfis_autorizados=["admin"])
async def get_excluir_chamado(request: Request, id_chamado: int):
    return templates.TemplateResponse("administrador/excluir_chamado.html", {"request": request})





