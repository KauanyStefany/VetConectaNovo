from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_root(request: Request):
    response = templates.TemplateResponse("administrador/home_administrador.html", {"request": request})
    return response   

@router.get("/listar_chamados")
async def pagina_chamado(request: Request):
    return templates.TemplateResponse("administrador/listar_chamados.html", {"request": request})

@router.get("/responder_chamado/{id_chamado}")
async def pagina_chamado(request: Request, id_chamado: int):
    return templates.TemplateResponse("administrador/responder_chamado.html", {"request": request})

@router.get("/excluir_chamado/{id_chamado}")
async def pagina_chamado(request: Request, id_chamado: int):
    return templates.TemplateResponse("administrador/excluir_chamado.html", {"request": request})





