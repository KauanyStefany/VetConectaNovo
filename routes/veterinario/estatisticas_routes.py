from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_root(request: Request):
    response = templates.TemplateResponse("veterinario/veterinario_home.html", {"request": request})
    return response   

@router.get("/listar_estatisticas")
async def pagina_postagem_artigo(request: Request):
    return templates.TemplateResponse("veterinario/listar_estatisticas.html", {"request": request})
