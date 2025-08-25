from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from model.denuncia_model import Denuncia
from repo import denuncia_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_root(request: Request):
    response = templates.TemplateResponse("administrador/home_administrador.html", {"request": request})
    return response   

@router.get("/listar_denuncias")
async def pagina_denuncia(request: Request):
    return templates.TemplateResponse("administrador/listar_denuncias.html", {"request": request})

@router.get("/excluir_denuncia/{id_denuncia}")
async def pagina_denuncia(request: Request, id_denuncia: int):
    return templates.TemplateResponse("administrador/excluir_denuncia.html", {"request": request})