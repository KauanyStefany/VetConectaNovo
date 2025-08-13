from fastapi import APIRouter, Request, status, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from model.curtida_feed_model import CurtidaFeed
from repo import curtida_feed_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

#metodo post
# @router.post("/tutor/curtida_feed/cadastrar")
# async def cadastrar_curtida_feed(
#     id_tutor: int = Form(...),
#     id_feed: int = Form(...)
# ):
#     curtida = CurtidaFeed(id_usuario=id_tutor, id_feed=id_feed)
#     curtida_feed_repo.inserir(curtida)
#     return RedirectResponse(url=f"/tutor/curtida_feed/listar?id_tutor={id_tutor}", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/tutor/curtida_feed/excluir/{id_tutor}/{id_feed}")
async def excluir_curtida_feed(id_tutor: int, id_feed: int):
    curtida_feed_repo.excluir(id_tutor, id_feed)
    return RedirectResponse(url=f"/tutor/curtida_feed/listar?id_tutor={id_tutor}", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/tutor/curtida_feed/listar")
async def listar_curtidas_feed(request: Request, id_tutor: int, limite: int = 10, offset: int = 0):
    curtidas = curtida_feed_repo.obter_por_id(id_tutor, limite, offset)
    return templates.TemplateResponse("tutor/listar_curtida_feed.html", {"request": request, "curtidas": curtidas})