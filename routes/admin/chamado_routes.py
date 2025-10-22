from datetime import datetime
from fastapi import APIRouter, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from repo import chamado_repo

from dtos.resposta_chamado_dto import RespostaChamadoDTO
from model.resposta_chamado_model import RespostaChamado
from util.auth_decorator import requer_autenticacao, obter_usuario_logado
from util.mensagens import adicionar_mensagem_erro, adicionar_mensagem_sucesso

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
    chamados = chamado_repo.obter_pagina(limite=20, offset=0)
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

@router.post("/responder_chamado")
@requer_autenticacao(perfis_autorizados=["admin"])
async def post_responder_chamado(
    request: Request, 
    id_chamado: int = Form(...),
    titulo: str = Form(...), 
    descricao: str = Form(...),
    usuario_logado: dict = None
):
    try:
        # Validar dados com DTO
        dto = RespostaChamadoDTO(titulo=titulo, descricao=descricao)
        
        # Criar objeto RespostaChamado
        resposta = RespostaChamado(
            id_chamado=id_chamado,
            id_admin=usuario_logado["id_usuario"],
            titulo=dto.titulo,
            descricao=dto.descricao,
            data_resposta=datetime.now()
        )
        
        # Inserir resposta no banco
        resposta_chamado_repo = RespostaChamadoRepositorio()
        await resposta_chamado_repo.inserir(resposta)
        
        # Atualizar status do chamado
        chamado_repo = ChamadoRepositorio()
        await chamado_repo.atualizar_status(id_chamado, "em_andamento")
        
        adicionar_mensagem_sucesso(request, "Resposta enviada com sucesso!")
        return RedirectResponse(
            url=f"/admin/responder_chamado/{id_chamado}",
            status_code=303
        )
        
    except Exception as erro:
        adicionar_mensagem_erro(request, str(erro))
        return RedirectResponse(
            url=f"/admin/responder_chamado/{id_chamado}",
            status_code=303
        )

@router.post("/fechar_chamado")
@requer_autenticacao(perfis_autorizados=["admin"]) 
async def post_fechar_chamado(
    request: Request,
    id_chamado: int = Form(...)
):
    try:
        # Atualizar status para resolvido
        chamado_repo = ChamadoRepositorio()
        await chamado_repo.atualizar_status(id_chamado, "resolvido")
        
        adicionar_mensagem_sucesso(request, "Chamado fechado com sucesso!")
        return RedirectResponse(
            url="/admin/listar_chamados",
            status_code=303
        )
        
    except Exception as erro:
        adicionar_mensagem_erro(request, str(erro))
        return RedirectResponse(
            url=f"/admin/responder_chamado/{id_chamado}",
            status_code=303
        )

@router.get("/excluir_chamado/{id_chamado}")
@requer_autenticacao(perfis_autorizados=["admin"])
async def get_excluir_chamado(request: Request, id_chamado: int):
    return templates.TemplateResponse("administrador/excluir_chamado.html", {"request": request})





