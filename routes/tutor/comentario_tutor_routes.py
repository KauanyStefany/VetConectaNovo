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

@router.get("/fazer_comentario")
async def pagina_comentario(request: Request):
    return templates.TemplateResponse("tutor/fazer_comentario.html", {"request": request})


@router.get("/excluir_comentario{id_comentario}")
async def pagina_comentario(request: Request, id_comentario: int):
    return templates.TemplateResponse("tutor/excluir_comentario.html", {"request": request})

