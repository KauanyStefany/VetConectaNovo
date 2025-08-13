from fastapi import APIRouter, Request, HTTPException, status, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from model.denuncia_model import Denuncia
from repo import denuncia_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/admin/denuncia/listar")
async def listar_denuncias(request: Request, limite: int = 10, offset: int = 0):
    denuncias = denuncia_repo.obter_todas_denuncias_paginadas(limite, offset)
    return templates.TemplateResponse("admin/listar_denuncia.html", {"request": request, "denuncias": denuncias})

@router.get("/admin/denuncia/obter/{id_denuncia}")
async def obter_denuncia(request: Request, id_denuncia: int):
    denuncia = denuncia_repo.obter_denuncia_por_id(id_denuncia)
    if not denuncia:
        raise HTTPException(status_code=404, detail="Denúncia não encontrada")
    return templates.TemplateResponse("admin/detalhar_denuncia.html", {"request": request, "denuncia": denuncia})

# METODOS DE POST
# @router.post("/admin/denuncia/cadastrar")
# async def cadastrar_denuncia(
#     request: Request,
#     id_usuario: int = Form(...),
#     motivo: str = Form(...),
#     descricao: str = Form(...),
#     data: str = Form(...)
# ):
#     denuncia = Denuncia(
#         id_usuario=id_usuario,
#         motivo=motivo,
#         descricao=descricao,
#         data=data
#     )
#     denuncia_repo.inserir_denuncia(denuncia)
#     return RedirectResponse(url="/admin/denuncia/listar", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/admin/denuncia/excluir/{id_denuncia}")
async def excluir_denuncia(id_denuncia: int):
    if denuncia_repo.excluir_denuncia(id_denuncia):
        return templates.TemplateResponse("admin/listar_denuncia.html", {"request": {}, "mensagem": "Denúncia excluída com sucesso!"})
    return templates.TemplateResponse("admin/listar_denuncia.html", {"request": {}, "mensagem": "Erro ao excluir denúncia."})