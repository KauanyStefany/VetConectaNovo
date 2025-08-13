from fastapi import APIRouter, Request, status, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from model.comentario_model import Comentario
from repo import comentario_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/veterinario/comentario/cadastrar")
async def cadastrar_comentario(
    id_veterinario: int = Form(...),
    id_artigo: int = Form(...),
    texto: str = Form(...)
):
    comentario = Comentario(id_veterinario=id_veterinario, id_artigo=id_artigo, texto=texto)
    comentario_repo.inserir(comentario)
    return RedirectResponse(url=f"/veterinario/comentario/listar?id_veterinario={id_veterinario}", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/veterinario/comentario/excluir/{id_comentario}")
async def excluir_comentario(id_comentario: int):
    comentario_repo.excluir(id_comentario)
    return RedirectResponse(url="/veterinario/comentario/listar", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/veterinario/comentario/listar")
async def listar_comentarios(request: Request, id_veterinario: int, limite: int = 10, offset: int = 0):
    comentarios = comentario_repo.obter_todos_paginado(id_veterinario, limite, offset)
    return templates.TemplateResponse("veterinario/listar_comentario.html", {"request": request, "comentarios": comentarios, "id_veterinario": id_veterinario})
