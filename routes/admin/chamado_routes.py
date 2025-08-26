from fastapi import APIRouter, Request, HTTPException, status, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from model.chamado_model import Chamado
from model.enums import ChamadoStatus
from repo import chamado_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/chamados")
async def listar_chamados(request: Request, offset: int = 0, limite: int = 10):
    chamados = chamado_repo.obter_todos_chamados_paginado(offset, limite)
    return templates.TemplateResponse("chamados/listar.html", {"request": request, "chamados": chamados})

@router.get("/chamados/{id_chamado}")
async def obter_chamado(request: Request, id_chamado: int):
    chamado = chamado_repo.obter_chamado_por_id(id_chamado)
    if not chamado:
        raise HTTPException(status_code=404, detail="Chamado não encontrado")
    return templates.TemplateResponse("chamados/detalhar.html", {"request": request, "chamado": chamado})

@router.get("/admin/chamado/excluir/{id_chamado}")
async def get_excluir_chamado(id_chamado: int):
    if chamado_repo.excluir_chamado(id_chamado):
        return templates.TemplateResponse("admin/listar_chamados.html", {"request": {}, "mensagem": "Chamado excluído com sucesso!"})
    return templates.TemplateResponse("admin/listar_chamados.html", {"request": {}, "mensagem": "Erro ao excluir chamado."})





