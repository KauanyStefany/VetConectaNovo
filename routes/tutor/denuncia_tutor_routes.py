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

@router.get("/fazer_denuncia")
async def pagina_fazer_denuncia(request: Request):
    return templates.TemplateResponse("tutor/fazer_denuncia.html", {"request": request})
