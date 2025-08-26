from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from model.comentario_model import Comentario
from repo import comentario_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_root(request: Request):
    response = templates.TemplateResponse("veterinario/veterinario_home.html", {"request": request})
    return response

@router.get("/alterar_dados")
async def pagina_alterar_dados(request: Request):
    return templates.TemplateResponse("veterinario/alterar_dados.html", {"request": request})

@router.get("/alterar_senha")
async def pagina_alterar_dados(request: Request):
    return templates.TemplateResponse("veterinario/alterar_senha.html", {"request": request})