from fastapi import APIRouter, Request, status, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from model.curtida_feed_model import CurtidaFeed
from repo import curtida_feed_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

#metodo post
# @router.post("/veterinario/curtida_feed/cadastrar")
# async def cadastrar_curtida_feed(
#     id_veterinario: int = Form(...),
#     id_feed: int = Form(...)
# ):
#     curtida = CurtidaFeed(id_usuario=id_veterinario, id_feed=id_feed)
#     curtida_feed_repo.inserir(curtida)
#     return RedirectResponse(url=f"/veterinario/curtida_feed/listar?id_veterinario={id_veterinario}", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/veterinario/curtida_feed/excluir/{id_veterinario}/{id_feed}")
async def excluir_curtida_feed(id_veterinario: int, id_feed: int):
    curtida_feed_repo.excluir(id_veterinario, id_feed)
    return RedirectResponse(url=f"/veterinario/curtida_feed/listar?id_veterinario={id_veterinario}", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/veterinario/curtida_feed/listar")
async def listar_curtidas_feed(request: Request, id_veterinario: int, limite: int = 10, offset: int = 0):
    curtidas = curtida_feed_repo.obter_por_id(id_veterinario, limite, offset)
    return templates.TemplateResponse("veterinario/listar_curtida_feed.html", {"request": request, "curtidas": curtidas, "id_veterinario": id_veterinario})