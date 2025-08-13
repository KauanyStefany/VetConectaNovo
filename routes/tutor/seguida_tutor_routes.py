from fastapi import APIRouter, Request, HTTPException, status, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from model.seguida_model import Seguida
from repo import seguida_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/tutor/seguida/listar")
async def listar_seguidas(request: Request, pagina: int = 1, tamanho_pagina: int = 10):
    seguidas = seguida_repo.obter_seguidas_paginado(pagina, tamanho_pagina)
    return templates.TemplateResponse("tutor/listar_seguida.html", {"request": request, "seguidas": seguidas})

# METODOS DE POST
# @router.post("/tutor/seguida/cadastrar")
# async def cadastrar_seguida(
#     id_veterinario: int = Form(...),
#     id_tutor: int = Form(...)
# ):
#     # Só o veterinário pode ser seguido
#     sucesso = seguida_repo.inserir_seguida(Seguida(id_veterinario=id_veterinario, id_tutor=id_tutor))
#     if sucesso:
#         return RedirectResponse(url="/tutor/seguida/listar", status_code=status.HTTP_303_SEE_OTHER)
#     return templates.TemplateResponse("tutor/listar_seguida.html", {"request": {}, "mensagem": "Erro ao cadastrar seguida."})

@router.get("/tutor/seguida/excluir/{id_veterinario}/{id_tutor}")
async def excluir_seguida(id_veterinario: int, id_tutor: int):
    sucesso = seguida_repo.excluir_seguida(id_veterinario, id_tutor)
    if sucesso:
        return templates.TemplateResponse("tutor/listar_seguida.html", {"request": {}, "mensagem": "Seguida excluída com sucesso!"})
    return templates.TemplateResponse("tutor/listar_seguida.html", {"request": {}, "mensagem": "Erro ao excluir seguida."})
