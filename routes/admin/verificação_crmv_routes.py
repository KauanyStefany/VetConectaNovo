from fastapi import APIRouter, Request, HTTPException, status, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from model.verificacao_crmv_model import VerificacaoCRMV
from repo import verificacao_crmv_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/admin/verificacao_crmv/listar")
async def listar_verificacoes(request: Request, limite: int = 10, offset: int = 0):
    verificacoes = verificacao_crmv_repo.obter_todos_paginado(limite, offset)
    return templates.TemplateResponse("admin/listar_verificacao_crmv.html", {"request": request, "verificacoes": verificacoes})

@router.get("/admin/verificacao_crmv/obter/{id_verificacao_crmv}")
async def obter_verificacao(request: Request, id_verificacao_crmv: int):
    verificacao = verificacao_crmv_repo.obter_por_id(id_verificacao_crmv)
    if not verificacao:
        raise HTTPException(status_code=404, detail="Verificação não encontrada")
    return templates.TemplateResponse("admin/detalhar_verificacao_crmv.html", {"request": request, "verificacao": verificacao})

#METODOS DE POST
# @router.post("/admin/verificacao_crmv/cadastrar")
# async def cadastrar_verificacao(
#     request: Request,
#     numero_crmv: str = Form(...),
#     nome_veterinario: str = Form(...),
#     estado: str = Form(...),
#     data_verificacao: str = Form(...)
# ):
#     verificacao = VerificacaoCRMV(
#         numero_crmv=numero_crmv,
#         nome_veterinario=nome_veterinario,
#         estado=estado,
#         data_verificacao=data_verificacao
#     )
#     verificacao_crmv_repo.inserir(verificacao)
#     return RedirectResponse(url="/admin/verificacao_crmv/listar", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/admin/verificacao_crmv/excluir/{id_verificacao_crmv}")
async def excluir_verificacao(id_verificacao_crmv: int):
    if verificacao_crmv_repo.excluir(id_verificacao_crmv):
        return templates.TemplateResponse("admin/listar_verificacao_crmv.html", {"request": {}, "mensagem": "Verificação excluída com sucesso!"})
    return templates.TemplateResponse("admin/listar_verificacao_crmv.html", {"request": {}, "mensagem": "Erro ao excluir verificação."})

@router.get("/admin/verificacao_crmv/alterar/{id_verificacao_crmv}")
async def get_alterar_verificacao(id_verificacao_crmv: int):
    verificacao = verificacao_crmv_repo.obter_por_id(id_verificacao_crmv)
    if verificacao:
        response = templates.TemplateResponse("admin/alterar_verificacao_crmv.html", {"request": {}, "verificacao": verificacao})
        return response
    return templates.TemplateResponse("admin/listar_verificacao_crmv.html", {"request": {}, "mensagem": "Verificação não encontrada."})