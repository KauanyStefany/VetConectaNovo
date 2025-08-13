from fastapi import APIRouter, status, Form
from fastapi.responses import RedirectResponse

from model.denuncia_model import Denuncia
from repo import denuncia_repo

router = APIRouter()

@router.post("/veterinario/denuncia/cadastrar")
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
    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)