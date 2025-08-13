from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from repo import comentario_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/admin/comentario/listar")
async def listar_comentarios(request: Request, limite: int = 10, offset: int = 0):
    comentarios = comentario_repo.obter_todos_paginado(limite, offset)
    return templates.TemplateResponse("admin/listar_comentario.html", {"request": request, "comentarios": comentarios})

@router.get("/admin/comentario/excluir/{id_comentario}")
async def excluir_comentario(id_comentario: int):
    if comentario_repo.excluir(id_comentario):
        return templates.TemplateResponse("admin/listar_comentario.html", {"request": {}, "mensagem": "Comentário excluído com sucesso!"})
    return templates.TemplateResponse("admin/listar_comentario.html", {"request": {}, "mensagem": "Erro ao excluir comentário."})

@router.get("/admin/comentario/obter/{id_comentario}")
async def obter_comentario(request: Request, id_comentario: int):
    comentario = comentario_repo.obter_por_id(id_comentario)
    if not comentario:
        return templates.TemplateResponse("admin/listar_comentario.html", {"request": request, "mensagem": "Comentário não encontrado."})
    return templates.TemplateResponse("admin/detalhar_comentario.html", {"request": request, "comentario": comentario})