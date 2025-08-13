from fastapi import APIRouter, Request, status, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from model.comentario_model import Comentario
from repo import comentario_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/tutor/comentario/cadastrar")
async def cadastrar_comentario(
    id_tutor: int = Form(...),
    id_artigo: int = Form(...),
    texto: str = Form(...)
):
    comentario = Comentario(id_tutor=id_tutor, id_artigo=id_artigo, texto=texto)
    comentario_repo.inserir(comentario)
    return RedirectResponse(url=f"/tutor/comentario/listar?id_tutor={id_tutor}", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/tutor/comentario/excluir/{id_comentario}")
async def excluir_comentario(id_comentario: int):
    comentario_repo.excluir(id_comentario)
    return RedirectResponse(url="/tutor/comentario/listar", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/tutor/comentario/listar")
async def listar_comentarios(request: Request, id_tutor: int, limite: int = 10, offset: int = 0):
    comentarios = comentario_repo.obter_todos_paginado(id_tutor, limite, offset)
    return templates.TemplateResponse("tutor/listar_comentario.html", {"request": request, "comentarios": comentarios})




