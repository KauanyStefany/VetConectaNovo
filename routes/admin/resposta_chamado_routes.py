from fastapi import APIRouter, Request, HTTPException, status, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from model.resposta_chamado_model import RespostaChamado
from repo import resposta_chamado_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/admin/resposta_chamado/listar")
async def listar_respostas(request: Request, limite: int = 10, offset: int = 0):
    respostas = resposta_chamado_repo.obter_todas_respostas_paginado(limite, offset)
    return templates.TemplateResponse("admin/listar_resposta_chamado.html", {"request": request, "respostas": respostas})

@router.get("/admin/resposta_chamado/obter/{id_resposta_chamado}")
async def obter_resposta(request: Request, id_resposta_chamado: int):
    resposta = resposta_chamado_repo.obter_resposta_por_id(id_resposta_chamado)
    if not resposta:
        raise HTTPException(status_code=404, detail="Resposta não encontrada")
    return templates.TemplateResponse("admin/detalhar_resposta_chamado.html", {"request": request, "resposta": resposta})

@router.get("/admin/resposta_chamado/excluir/{id_resposta_chamado}")
async def excluir_resposta(id_resposta_chamado: int):
    if resposta_chamado_repo.excluir_resposta(id_resposta_chamado):
        return templates.TemplateResponse("admin/listar_resposta_chamado.html", {"request": {}, "mensagem": "Resposta excluída com sucesso!"})
    return templates.TemplateResponse("admin/listar_resposta_chamado.html", {"request": {}, "mensagem": "Erro ao excluir resposta."})

#METODOS DE POST
# @router.post("/admin/resposta_chamado/cadastrar")
# async def cadastrar_resposta(
#     request: Request,
#     id_chamado: int = Form(...),
#     titulo: str = Form(...),
#     descricao: str = Form(...),
#     data: str = Form(...)
# ):
#     resposta = RespostaChamado(
#         id_chamado=id_chamado,
#         titulo=titulo,
#         descricao=descricao,
#         data=data
#     )
#     resposta_chamado_repo.inserir_resposta(resposta)
#     return RedirectResponse(url="/admin/resposta_chamado/listar", status_code=status.HTTP_303_SEE_OTHER)
