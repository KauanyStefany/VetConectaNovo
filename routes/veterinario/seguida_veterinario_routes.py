from fastapi import APIRouter, Request, HTTPException, status, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from model.seguida_model import Seguida
from repo import seguida_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/veterinario/seguida/listar")
async def listar_seguidores(request: Request, id_veterinario: int, pagina: int = 1, tamanho_pagina: int = 10):
    # Lista todos que seguem este veterinário
    seguidas = seguida_repo.obter_seguidores_veterinario(id_veterinario, pagina, tamanho_pagina)
    return templates.TemplateResponse("veterinario/listar_seguidores.html", {"request": request, "seguidas": seguidas})


#O VETERINÁRIO PODE SEGUIR OUTRO VETERINÁRIO

# @router.post("/veterinario/seguida/seguir")
# async def seguir_veterinario(
#     id_veterinario_seguidor: int = Form(...),
#     id_veterinario_seguido: int = Form(...)
# ):
#     # Veterinário segue outro veterinário
#     sucesso = seguida_repo.inserir_seguida(Seguida(id_veterinario=id_veterinario_seguido, id_tutor=id_veterinario_seguidor))
#     if sucesso:
#         return RedirectResponse(url="/veterinario/seguida/listar?id_veterinario={}".format(id_veterinario_seguidor), status_code=status.HTTP_303_SEE_OTHER)
#     return templates.TemplateResponse("veterinario/listar_seguidores.html", {"request": {}, "mensagem": "Erro ao seguir veterinário."})

# @router.get("/veterinario/seguida/excluir/{id_veterinario_seguido}/{id_veterinario_seguidor}")
# async def deixar_de_seguir_veterinario(id_veterinario_seguido: int, id_veterinario_seguidor: int):
#     # Veterinário deixa de seguir outro veterinário
#     sucesso = seguida_repo.excluir_seguida(id_veterinario_seguido, id_veterinario_seguidor)
#     if sucesso:
#         return templates.TemplateResponse("veterinario/listar_seguidores.html", {"request": {}, "mensagem": "Você deixou de seguir este veterinário."})
#     return templates.TemplateResponse("veterinario/listar_seguidores.html", {"request": {}, "mensagem": "Erro ao deixar de seguir veterinário."})