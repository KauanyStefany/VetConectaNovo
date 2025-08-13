from fastapi import APIRouter, Request, status, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from model.denuncia_model import Denuncia
from repo import denuncia_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/tutor/denuncia/cadastrar")
async def cadastrar_denuncia(
    id_usuario: int = Form(...),
    motivo: str = Form(...),
    descricao: str = Form(...),
    data: str = Form(...)
):
    denuncia = Denuncia(
        id_usuario=id_usuario,
        motivo=motivo,
        descricao=descricao,
        data=data
    )
    denuncia_repo.inserir_denuncia(denuncia)
    return RedirectResponse(url="/tutor/denuncia/listar?id_usuario={}".format(id_usuario), status_code=status.HTTP_303_SEE_OTHER)

