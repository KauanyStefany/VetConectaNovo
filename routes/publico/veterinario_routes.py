from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from repo import veterinario_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/publico/veterinario/listar")
async def listar_veterinarios(request: Request, limite: int = 10, offset: int = 0):
    veterinarios = veterinario_repo.obter_por_pagina(limite, offset)
    return templates.TemplateResponse("publico/listar_veterinario.html", {"request": request, "veterinarios": veterinarios})