from fastapi import APIRouter, Request, status, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from model.curtida_artigo_model import CurtidaArtigo
from repo import curtida_artigo_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/veterinario/curtida_artigo/cadastrar")
async def cadastrar_curtida_artigo(
    id_veterinario: int = Form(...),
    id_artigo: int = Form(...)
):
    curtida = CurtidaArtigo(id_veterinario, id_artigo=id_artigo)
    curtida_artigo_repo.inserir_curtida_artigo(curtida)
    return RedirectResponse(url=f"/veterinario/curtida_artigo/listar?id_veterinario={id_veterinario}", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/veterinario/curtida_artigo/excluir/{id_veterinario}/{id_artigo}")
async def excluir_curtida_artigo(id_veterinario: int, id_artigo: int):
    curtida_artigo_repo.excluir_curtida(id_veterinario, id_artigo)
    return RedirectResponse(url=f"/veterinario/curtida_artigo/listar?id_veterinario={id_veterinario}", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/veterinario/curtida_artigo/listar")
async def listar_curtidas_artigo(request: Request, id_veterinario: int, limite: int = 10, offset: int = 0):
    curtidas = curtida_artigo_repo.obter_por_id(id_veterinario, limite, offset)
    return templates.TemplateResponse("veterinario/listar_curtida_artigo.html", {"request": request, "curtidas": curtidas, "id_veterinario": id_veterinario})