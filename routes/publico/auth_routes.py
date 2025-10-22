from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from pydantic_core import ValidationError
from typing import Optional
import os
import logging
from slowapi import Limiter
from slowapi.util import get_remote_address

from dtos.auth_dto import (
    EsqueciSenhaDTO,
    LoginDTO,
    CadastroTutorDTO,
    CadastroVeterinarioDTO,
    RedefinirSenhaDTO,
)
from model.enums import PerfilUsuario
from model.tutor_model import Tutor
from model.veterinario_model import Veterinario
from repo import administrador_repo, usuario_repo, tutor_repo, veterinario_repo
from util.security import (
    criar_hash_senha,
    verificar_senha,
    gerar_token_redefinicao,
    obter_data_expiracao_token,
)
from util.auth_decorator import criar_sessao, destruir_sessao, esta_logado
from util.template_util import criar_templates
from util.validacoes_dto import processar_erros_validacao

logger = logging.getLogger(__name__)
router = APIRouter()
templates = criar_templates("templates/publico")
limiter = Limiter(key_func=get_remote_address)


@router.get("/login")
async def get_login(request: Request, redirect: Optional[str] = None):
    if esta_logado(request):
        return RedirectResponse("/", status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse(
        "login.html", {"request": request, "redirect": redirect}
    )


@router.post("/login")
@limiter.limit("5/minute")
async def post_login(
    request: Request,
    email: str = Form(),
    senha: str = Form(),
    redirect: str = Form(None),
):
    if esta_logado(request):
        return RedirectResponse("/", status.HTTP_303_SEE_OTHER)

    dados_formulario = {"email": email}

    try:
        login_dto = LoginDTO(email=email, senha=senha)

        usuario = administrador_repo.obter_por_email(login_dto.email)
        if usuario:
            usuario.perfil = PerfilUsuario.ADMIN.value
            usuario.id_usuario = usuario.id_admin
            usuario.telefone = ""
        else:
            usuario = usuario_repo.obter_por_email(login_dto.email)

        if not usuario or not verificar_senha(login_dto.senha, usuario.senha):
            return templates.TemplateResponse(
                "login.html",
                {
                    "request": request,
                    "erros": {"geral": "Credenciais inválidas."},
                    "dados": dados_formulario,
                    "redirect": redirect,
                },
            )

        usuario_dict = {
            "id": usuario.id_usuario,
            "nome": usuario.nome,
            "email": usuario.email,
            "telefone": usuario.telefone,
            "perfil": usuario.perfil,
            "foto": f"/static/img/usuarios/{usuario.id_usuario:08d}.jpg",
        }
        criar_sessao(request, usuario_dict)

        url_redirect = "/"
        if redirect:
            url_redirect = redirect
        elif usuario.perfil == PerfilUsuario.VETERINARIO.value:
            url_redirect = f"/veterinario/dashboard"
        elif usuario.perfil == PerfilUsuario.TUTOR.value:
            url_redirect = f"/tutor/dashboard"
        elif usuario.perfil == PerfilUsuario.ADMIN.value:
            url_redirect = f"/admin/dashboard"
        return RedirectResponse(url_redirect, status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        erros = processar_erros_validacao(e)
        logger.warning(f"Erros de validação no login: {erros}")
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "erros": erros,
                "dados": dados_formulario,
                "redirect": redirect,
            },
        )
    except Exception as e:
        logger.error(f"Erro geral no login: {str(e)}", exc_info=True)
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "erros": {"geral": "Ocorreu um erro ao processar o login."},
                "dados": dados_formulario,
                "redirect": redirect,
            },
        )


@router.get("/logout")
async def logout(request: Request):
    destruir_sessao(request)
    return RedirectResponse("/", status.HTTP_303_SEE_OTHER)


@router.get("/cadastro")
async def get_cadastro(request: Request):
    if esta_logado(request):
        return RedirectResponse("/", status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("cadastro.html", {"request": request})


@router.post("/cadastro")
@limiter.limit("3/hour")
async def post_cadastro(
    request: Request,
    nome: str = Form(),
    email: str = Form(),
    telefone: str = Form(),
    senha: str = Form(),
    confirmar_senha: str = Form(),
    perfil: str = Form(),
    crmv: str = Form(None),
):
    if esta_logado(request):
        return RedirectResponse("/", status.HTTP_303_SEE_OTHER)

    # Dados do formulário para reexibir
    dados_formulario = {
        "nome": nome,
        "email": email,
        "telefone": telefone,
        "perfil": perfil,
        "crmv": crmv,
    }

    try:
        # LOG: Início do cadastro
        logger.info(f"Iniciando cadastro - Email: {email}, Perfil: {perfil}")

        # Validar perfil antes de prosseguir
        if perfil not in [PerfilUsuario.TUTOR.value, PerfilUsuario.VETERINARIO.value]:
            logger.warning(f"Perfil inválido recebido: {perfil}")
            return templates.TemplateResponse(
                "cadastro.html",
                {
                    "request": request,
                    "erros": {"geral": "Perfil inválido selecionado."},
                    "dados": dados_formulario,
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # Normalizar email para verificação
        email_normalizado = email.strip().lower()
        
        # Verificar se email já existe
        usuario_existente = usuario_repo.obter_por_email(email_normalizado)
        if usuario_existente:
            logger.warning(f"Tentativa de cadastro com email existente: {email_normalizado}")
            return templates.TemplateResponse(
                "cadastro.html",
                {
                    "request": request,
                    "erros": {
                        "geral": "Este e-mail já está cadastrado. Tente fazer login ou use outro e-mail."
                    },
                    "dados": dados_formulario,
                },
                status_code=status.HTTP_409_CONFLICT,
            )

        # Variável para armazenar o ID do usuário criado
        id_usuario: int | None = None

        # CADASTRO DE TUTOR
        if perfil == PerfilUsuario.TUTOR.value:
            logger.info(f"Validando dados de tutor - Email: {email}")
            
            # Validar usando DTO
            cadastro_dto = CadastroTutorDTO(
                nome=nome.strip(),
                email=email_normalizado,
                telefone=telefone.strip(),
                senha=senha,
                confirmar_senha=confirmar_senha,
                perfil=perfil,
            )

            # Criar objeto Tutor
            tutor = Tutor(
                id_usuario=0,
                nome=cadastro_dto.nome,
                email=cadastro_dto.email,
                senha=criar_hash_senha(cadastro_dto.senha),
                telefone=cadastro_dto.telefone,
                perfil=perfil,
                token_redefinicao=None,
                data_token=None,
                data_cadastro=None,
                quantidade_pets=0,
                descricao_pets=None,
            )

            logger.info(f"Inserindo tutor no banco - Email: {email}")
            id_usuario = tutor_repo.inserir(tutor)

        # CADASTRO DE VETERINÁRIO
        elif perfil == PerfilUsuario.VETERINARIO.value:
            logger.info(f"Validando dados de veterinário - Email: {email}, CRMV: {crmv}")
            
            # Validar usando DTO
            cadastro_dto = CadastroVeterinarioDTO(
                nome=nome.strip(),
                email=email_normalizado,
                telefone=telefone.strip(),
                senha=senha,
                confirmar_senha=confirmar_senha,
                perfil=perfil,
                crmv=crmv.strip() if crmv else "",
            )

            # Criar objeto Veterinario
            veterinario = Veterinario(
                id_usuario=0,
                nome=cadastro_dto.nome,
                email=cadastro_dto.email,
                senha=criar_hash_senha(cadastro_dto.senha),
                telefone=cadastro_dto.telefone,
                perfil=perfil,
                token_redefinicao=None,
                data_token=None,
                data_cadastro=None,
                crmv=cadastro_dto.crmv,
                verificado=False,
                bio=None,
            )

            logger.info(f"Inserindo veterinário no banco - Email: {email}")
            id_usuario = veterinario_repo.inserir(veterinario)

        # Verificar se inserção foi bem-sucedida
        if not id_usuario or id_usuario <= 0:
            logger.error(f"Falha ao inserir usuário no banco - ID retornado: {id_usuario}")
            raise Exception("Falha ao criar usuário no banco de dados.")

        logger.info(f"✅ Cadastro concluído com sucesso! ID: {id_usuario}, Email: {email}")
        return RedirectResponse("/login?cadastro=sucesso", status.HTTP_303_SEE_OTHER)

    # Erros de validação do DTO (Pydantic)
    except ValidationError as e:
        erros = processar_erros_validacao(e)
        logger.warning(f"❌ Erro de validação no cadastro - Email: {email} | Erros: {e.errors()}")
        return templates.TemplateResponse(
            "cadastro.html",
            {
                "request": request,
                "erros": erros,
                "dados": dados_formulario,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # Erros gerais (banco de dados, etc)
    except Exception as e:
        logger.error(f"❌ Erro GERAL no cadastro - Email: {email} | Erro: {str(e)}", exc_info=True)
        return templates.TemplateResponse(
            "cadastro.html",
            {
                "request": request,
                "erros": {"geral": f"Ocorreu um erro ao processar o cadastro: {str(e)}"},
                "dados": dados_formulario,
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/esqueci-senha")
async def get_esqueci_senha(request: Request):
    return templates.TemplateResponse("esqueci_senha.html", {"request": request})


@router.post("/esqueci-senha")
@limiter.limit("3/hour")
async def post_esqueci_senha(request: Request, email: str = Form()):
    dados_formulario = {"email": email}

    try:
        esqueci_senha_dto = EsqueciSenhaDTO(email=email)
        usuario = usuario_repo.obter_por_email(esqueci_senha_dto.email)

        mensagem = "Se o e-mail estiver cadastrado, você receberá uma mensagem contendo instruções para redefinir sua senha. Cheque sua caixa de entrada e a pasta de spam e siga as instruções para redefinir sua senha."

        if not usuario:
            logger.warning(f"Solicitação de redefinição para e-mail não cadastrado: {esqueci_senha_dto.email}")
            return templates.TemplateResponse(
                "esqueci_senha.html", {"request": request, "mensagem": mensagem}
            )
        else:
            logger.info(f"Solicitação de redefinição para email: {esqueci_senha_dto.email}")
            token = gerar_token_redefinicao()
            data_expiracao = obter_data_expiracao_token(24)
            usuario_repo.atualizar_token(email, token, data_expiracao)

            response_data = {"request": request, "sucesso": mensagem}
            if os.getenv("ENVIRONMENT", "development") == "development":
                link_redefinicao = f"http://localhost:8000/redefinir-senha/{token}"
                response_data["debug_link"] = link_redefinicao

            return templates.TemplateResponse("esqueci_senha.html", response_data)

    except ValidationError as e:
        erros = processar_erros_validacao(e)
        logger.warning(f"Erros de validação na redefinição de senha: {erros}")
        return templates.TemplateResponse(
            "esqueci_senha.html",
            {"request": request, "erros": erros, "dados": dados_formulario},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.get("/redefinir-senha/{token}")
async def get_redefinir_senha(request: Request, token: str):
    usuario = usuario_repo.obter_por_token(token)
    if not usuario:
        return templates.TemplateResponse(
            "redefinir_senha.html",
            {
                "request": request,
                "erros": {"geral": "Link de redefinição de senha inválido ou expirado"},
            },
        )
    return templates.TemplateResponse(
        "redefinir_senha.html", {"request": request, "token": token}
    )


@router.post("/redefinir-senha/{token}")
@limiter.limit("5/hour")
async def post_redefinir_senha(
    request: Request,
    token: str,
    senha: str = Form(...),
    confirmar_senha: str = Form(...),
):
    try:
        redefinir_senha_dto = RedefinirSenhaDTO(senha=senha, confirmar_senha=confirmar_senha)
        usuario = usuario_repo.obter_por_token(token)

        if not usuario:
            return templates.TemplateResponse(
                "redefinir_senha.html",
                {
                    "request": request,
                    "erros": {"geral": "Link de redefinição de senha inválido ou expirado"},
                },
            )

        senha_hash = criar_hash_senha(redefinir_senha_dto.senha)
        usuario_repo.atualizar_senha(usuario.id_usuario, senha_hash)
        usuario_repo.limpar_token(usuario.id_usuario)

        return templates.TemplateResponse(
            "redefinir_senha.html",
            {
                "request": request,
                "mensagem": "Senha redefinida com sucesso! Você já pode fazer login.",
            },
        )

    except ValidationError as e:
        erros = processar_erros_validacao(e)
        logger.warning(f"Erros de validação na redefinição de senha: {erros}")
        return templates.TemplateResponse(
            "redefinir_senha.html",
            {"request": request, "erros": erros, "token": token},
        )