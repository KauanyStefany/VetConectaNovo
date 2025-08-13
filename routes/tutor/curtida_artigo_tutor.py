from fastapi import APIRouter, Request, status, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from model.curtida_artigo_model import CurtidaArtigo
from repo import curtida_artigo_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/tutor/curtida_artigo/cadastrar")
async def cadastrar_curtida_artigo(
    id_tutor: int = Form(...),
    id_artigo: int = Form(...)
):
    curtida = CurtidaArtigo(id_tutor, id_artigo=id_artigo)
    curtida_artigo_repo.inserir_curtida_artigo(curtida)
    return RedirectResponse(url=f"/tutor/curtida_artigo/listar?id_tutor={id_tutor}", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/tutor/curtida_artigo/excluir/{id_tutor}/{id_artigo}")
async def excluir_curtida_artigo(id_tutor: int, id_artigo: int):
    curtida_artigo_repo.excluir_curtida(id_tutor, id_artigo)
    return RedirectResponse(url=f"/tutor/curtida_artigo/listar?id_tutor={id_tutor}", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/tutor/curtida_artigo/listar")
async def listar_curtidas_artigo(request: Request, id_tutor: int, limite: int = 10, offset: int = 0):
    curtidas = curtida_artigo_repo.obter_por_id(id_tutor, limite, offset)
    return templates.TemplateResponse("tutor/listar_curtida_artigo.html", {"request": request, "curtidas": curtidas, "id_tutor": id_tutor})