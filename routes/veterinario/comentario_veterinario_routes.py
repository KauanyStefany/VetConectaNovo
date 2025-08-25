from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_root(request: Request):
    response = templates.TemplateResponse("veterinario/veterinario_home.html", {"request": request})
    return response   

@router.get("/listar_comentario")
async def pagina_comentario(request: Request):
    return templates.TemplateResponse("veterinario/listar_comentario.html", {"request": request})

@router.get("/excluir_comentario/{id_comentario}")
async def pagina_comentario(request: Request, id_comentario: int):
    return templates.TemplateResponse("veterinario/excluir_comentario.html", {"request": request})

@router.get("/fazer_comentario")
async def pagina_comentario(request: Request):
    return templates.TemplateResponse("veterinario/fazer_comentario.html", {"request": request})
