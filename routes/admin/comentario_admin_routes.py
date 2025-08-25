from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from repo import comentario_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_root(request: Request):
    response = templates.TemplateResponse("administrador/home_administrador.html", {"request": request})
    return response   

@router.get("/listar_comentarios")
async def pagina_comentario(request: Request):
    return templates.TemplateResponse("administrador/listar_comentarios.html", {"request": request})

@router.get("/moderar_comentarios/{id_comentario}")
async def pagina_comentario(request: Request, id_comentario: int):
    return templates.TemplateResponse("administrador/moderar_comentarios.html", {"request": request})