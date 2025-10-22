from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from util.auth_decorator import requer_autenticacao, obter_usuario_logado

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def get_root(request: Request):
    response = templates.TemplateResponse("veterinario/veterinario_home.html", {"request": request})
    return response

# @router.get("/obter_solicitacao_crmv")
# @requer_autenticacao(perfis_autorizados=["veterinario"])
# async def get_obter_solicitacao_crmv(request: Request):
#     return templates.TemplateResponse("veterinario/obter_solicitacao_crmv.html", {"request": request})

# @router.get("/fazer_solicitacao_crmv")
# @requer_autenticacao(perfis_autorizados=["veterinario"])
# async def get_fazer_solicitacao_crmv(request: Request):
#     return templates.TemplateResponse("veterinario/fazer_solicitacao_crmv.html", {"request": request})

@router.get("/obter_solicitacao_crmv")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def get_solicitacao(request: Request, usuario_logado: dict = None):
    """Verifica se já existe solicitação"""
    verificacao = verificacao_crmv_repo.obter_por_veterinario(usuario_logado['id'])  # Criar

    return templates.TemplateResponse("veterinario/obter_solicitacao_crmv.html", {
        "request": request,
        "verificacao": verificacao
    })

@router.get("/fazer_solicitacao_crmv")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def get_fazer_solicitacao(request: Request):
    return templates.TemplateResponse("veterinario/fazer_solicitacao_crmv.html", {
        "request": request
    })

@router.post("/fazer_solicitacao_crmv")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def post_fazer_solicitacao(request: Request, usuario_logado: dict = None):
    from model.verificacao_crmv_model import VerificacaoCRMV

    # Verificar se já existe solicitação
    verificacao_existente = verificacao_crmv_repo.obter_por_veterinario(usuario_logado['id'])
    if verificacao_existente and verificacao_existente.status_verificacao == 'pendente':
        adicionar_mensagem_aviso(request, "Você já possui uma solicitação pendente.")
        return RedirectResponse("/veterinario/obter_solicitacao_crmv", status_code=303)

    # Criar nova solicitação
    verificacao = VerificacaoCRMV(
        id_verificacao_crmv=0,
        id_veterinario=usuario_logado['id'],
        id_administrador=None,
        data_verificacao=datetime.now(),
        status_verificacao='pendente'
    )

    if verificacao_crmv_repo.inserir(verificacao):
        adicionar_mensagem_sucesso(request, "Solicitação enviada! Aguarde análise.")
    else:
        adicionar_mensagem_erro(request, "Erro ao enviar solicitação.")

    return RedirectResponse("/veterinario/obter_solicitacao_crmv", status_code=303)