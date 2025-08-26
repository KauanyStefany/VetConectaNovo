from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from model.comentario_model import Comentario
from repo import comentario_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_root(request: Request):
    response = templates.TemplateResponse("tutor/home_tutor.html", {"request": request})
    return response

@router.get("/listar_postagem_feed")
async def pagina_listar_postagem_feed(request: Request):
    return templates.TemplateResponse("tutor/listar_postagens_feed.html", {"request": request})

@router.get("/fazer_postagem_feed")
async def pagina_fazer_postagem_feed(request: Request):
    return templates.TemplateResponse("tutor/fazer_postagem_feed.html", {"request": request})

@router.get("/excluir_postagem_feed")
async def pagina_excluir_postagem_feed(request: Request):
    return templates.TemplateResponse("tutor/excluir_postagem_feed.html", {"request": request})