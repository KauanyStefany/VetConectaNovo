from fastapi import APIRouter, Request, HTTPException, status, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from model.chamado_model import Chamado
from model.enums import ChamadoStatus
from repo import chamado_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/chamados")
async def listar_chamados(request: Request, offset: int = 0, limite: int = 10):
    chamados = chamado_repo.obter_todos_chamados_paginado(offset, limite)
    return templates.TemplateResponse("chamados/listar.html", {"request": request, "chamados": chamados})

@router.get("/chamados/{id_chamado}")
async def obter_chamado(request: Request, id_chamado: int):
    chamado = chamado_repo.obter_chamado_por_id(id_chamado)
    if not chamado:
        raise HTTPException(status_code=404, detail="Chamado não encontrado")
    return templates.TemplateResponse("chamados/detalhar.html", {"request": request, "chamado": chamado})

@router.get("/admin/chamado/excluir/{id_chamado}")
async def get_excluir_chamado(id_chamado: int):
    if chamado_repo.excluir_chamado(id_chamado):
        return templates.TemplateResponse("admin/listar_chamados.html", {"request": {}, "mensagem": "Chamado excluído com sucesso!"})
    return templates.TemplateResponse("admin/listar_chamados.html", {"request": {}, "mensagem": "Erro ao excluir chamado."})


#METODOS DE POST

# @router.post("/chamados")
# async def criar_chamado(
#     request: Request,
#     id_usuario: int = Form(...),
#     id_admin: int = Form(...),
#     titulo: str = Form(...),
#     descricao: str = Form(...),
#     status: str = Form(...),
#     data: str = Form(...)
# ):
#     chamado = Chamado(
#         id_chamado=0,
#         id_usuario=id_usuario,
#         id_admin=id_admin,
#         titulo=titulo,
#         descricao=descricao,
#         status=ChamadoStatus(status),
#         data=data
#     )
#     chamado_repo.inserir_chamado(chamado)
#     return RedirectResponse(url="/chamados", status_code=status.HTTP_303_SEE_OTHER)

# @router.post("/chamados/{id_chamado}/status")
# async def atualizar_status_chamado(id_chamado: int, novo_status: str = Form(...)):
#     sucesso = chamado_repo.atualizar_status_chamado(id_chamado, ChamadoStatus(novo_status))
#     if not sucesso:
#         raise HTTPException(status_code=404, detail="Chamado não encontrado ou status inválido")
#     return RedirectResponse(url=f"/chamados/{id_chamado}", status_code=status.HTTP_303_SEE_OTHER)

# @router.post("/chamados/{id_chamado}/excluir")
# async def excluir_chamado(id_chamado: int):
#     sucesso = chamado_repo.excluir_chamado(id_chamado)
#     if not sucesso:
#         raise HTTPException(status_code=404, detail="Chamado não encontrado")
#     return RedirectResponse(url="/chamados", status_code=status.HTTP_303_SEE_OTHER)


