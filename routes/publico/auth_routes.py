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
from repo import usuario_repo, tutor_repo, veterinario_repo
from util.security import (
    criar_hash_senha,
    verificar_senha,
    gerar_token_redefinicao,
    obter_data_expiracao_token
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
    # Se já está logado, redirecionar
    if esta_logado(request):
        return RedirectResponse("/", status.HTTP_303_SEE_OTHER)

    # Retornar o template de login
    return templates.TemplateResponse(
        "login.html", {"request": request, "redirect": redirect}
    )


@router.post("/login")
@limiter.limit("5/minute")  # limite de 5 tentativas por minuto
async def post_login(
    request: Request,
    email: str = Form(),
    senha: str = Form(),
    redirect: str = Form(None),
):
    # Se já está logado, redirecionar
    if esta_logado(request):
        return RedirectResponse("/", status.HTTP_303_SEE_OTHER)

    # Armazenar dados do formulário para reexibir em caso de erro
    dados_formulario = {"email": email}

    try:
        # Validar usando DTO apropriado
        login_dto = LoginDTO(email=email, senha=senha)

        # Buscar usuário pelo email
        usuario = usuario_repo.obter_por_email(login_dto.email)

        # Verificar credenciais
        if not usuario or not verificar_senha(login_dto.senha, usuario.senha):
            return templates.TemplateResponse(
                "publico/login.html",
                {
                    "request": request,
                    "erros": {"geral": "Credenciais inválidas."},
                    "email": email,
                    "redirect": redirect,
                },
            )

        # Criar sessão
        usuario_dict = {
            "id": usuario.id_usuario,
            "nome": usuario.nome,
            "email": usuario.email,
            "telefone": usuario.telefone,
            "perfil": usuario.perfil,
            "foto": usuario.foto,
        }
        criar_sessao(request, usuario_dict)

        # Redirecionar após login de acordo com perfil
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

    # Processar erros de validação do DTO
    except ValidationError as e:
        # Obter dicionário com erros de validação
        erros = processar_erros_validacao(e)

        # Logar os erros de validação para auditoria
        logger.warning(
            f"Erros de validação no login: {' | '.join([f'{erro.key}: {erro.value}' for erro in erros])}"
        )

        # Retornar template com erros
        return templates.TemplateResponse(
            "publico/login.html",
            {
                "request": request,
                "erros": erros,
                "dados": dados_formulario,
                "redirect": redirect,
            },
        )


@router.get("/logout")
async def logout(request: Request):
    # Remover sessão e redirecionar para a página inicial
    destruir_sessao(request)
    return RedirectResponse("/", status.HTTP_303_SEE_OTHER)


@router.get("/cadastro")
async def get_cadastro(request: Request):
    # Se já está logado, redirecionar
    if esta_logado(request):
        return RedirectResponse("/", status.HTTP_303_SEE_OTHER)

    # Retornar o template de cadastro
    return templates.TemplateResponse("publico/cadastro.html", {"request": request})


@router.post("/cadastro")
@limiter.limit("3/hour")  # limite de 3 cadastros por hora
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
    # Se já está logado, redirecionar
    if esta_logado(request):
        return RedirectResponse("/", status.HTTP_303_SEE_OTHER)

    # Armazenar dados do formulário para reexibir em caso de erro
    dados_formulario = {
        "nome": nome,
        "email": email,
        "telefone": telefone,
        "perfil": perfil,
        "crmv": crmv,
    }

    try:
        # Verificar se email já existe (mensagem genérica por segurança)
        if usuario_repo.obter_por_email(email.strip().lower()):
            logger.warning(f"Tentativa de cadastro com email existente: {email}")
            return templates.TemplateResponse(
                "publico/cadastro.html",
                {
                    "request": request,
                    "erros": {
                        "geral": "Não foi possível completar o cadastro. Verifique os dados."
                    },
                    "dados": dados_formulario,
                },
                status_code=status.HTTP_409_CONFLICT,
            )

        # O id do usuário a ser criado
        id_usuario: int | None = None

        # O cadastro público pode ser de tutor ou veterinário
        cadastro_dto: CadastroTutorDTO | CadastroVeterinarioDTO

        # Se o perfil escolhido for tutor
        if perfil == PerfilUsuario.TUTOR.value:
            # Validar usando DTO apropriado
            cadastro_dto = CadastroTutorDTO(
                nome=nome,
                email=email,
                telefone=telefone,
                senha=senha,
                confirmar_senha=confirmar_senha,
                perfil=perfil,
            )

            # Criar objeto Tutor para inserção no banco
            tutor = Tutor(
                id_usuario=0,
                nome=cadastro_dto.nome,
                email=cadastro_dto.email,
                senha=criar_hash_senha(cadastro_dto.senha),
                telefone=cadastro_dto.telefone,
                perfil=perfil,
                foto=None,
                token_redefinicao=None,
                data_token=None,
                data_cadastro=None,
                quantidade_pets=0,
                descricao_pets=None,
            )

            # Inserir tutor no banco de dados e obter o id gerado
            id_usuario = tutor_repo.inserir(tutor)
            assert id_usuario is not None

        # Se o perfil escolhido for veterinário
        elif perfil == PerfilUsuario.VETERINARIO.value:
            # Validar usando DTO apropriado
            cadastro_dto = CadastroVeterinarioDTO(
                nome=nome,
                email=email,
                telefone=telefone,
                senha=senha,
                confirmar_senha=confirmar_senha,
                perfil=perfil,
                crmv=crmv,
            )

            # Criar objeto Veterinario para inserção no banco
            veterinario = Veterinario(
                id_usuario=0,
                nome=cadastro_dto.nome,
                email=cadastro_dto.email,
                senha=criar_hash_senha(cadastro_dto.senha),
                telefone=cadastro_dto.telefone,
                perfil=perfil,
                foto=None,
                token_redefinicao=None,
                data_token=None,
                data_cadastro=None,
                crmv=cadastro_dto.crmv,
                verificado=False,
                bio=None,
            )
            id_usuario = veterinario_repo.inserir(veterinario)

        # Verificar se o usuário foi inserido corretamente
        if not id_usuario:
            raise Exception("Ocorreu um erro desconhecido ao processar o cadastro.")

        logger.info(f"Novo usuário cadastrado com sucesso. ID: {id_usuario}")
        return RedirectResponse("/login?cadastro=sucesso", status.HTTP_303_SEE_OTHER)

    # Processar erros de validação do DTO
    except ValidationError as e:
        # Obter dicionário com erros de validação
        erros = processar_erros_validacao(e)

        # Logar os erros de validação para auditoria
        logger.warning(
            f"Erro de validação no cadastro - Email: {email} - Erros: {e.errors()}"
        )

        # Retornar template com erros
        return templates.TemplateResponse(
            "publico/cadastro.html",
            {"request": request, "erros": erros, "dados": dados_formulario},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.get("/esqueci-senha")
async def get_esqueci_senha(request: Request):
    # Retornar o template de esquecimento de senha
    return templates.TemplateResponse(
        "publico/esqueci_senha.html",
        {"request": request},
    )


@router.post("/esqueci-senha")
@limiter.limit("3/hour")  # limite de 3 tentativas por hora
async def post_esqueci_senha(
    request: Request,
    email: str = Form(),
):
    # Armazenar dados do formulário para reexibir em caso de erro
    dados_formulario = {
        "email": email,
    }

    try:
        # Validar usando DTO apropriado
        esqueci_senha_dto = EsqueciSenhaDTO(email=email)

        # Buscar usuário pelo email
        usuario = usuario_repo.obter_por_email(esqueci_senha_dto.email)

        # Sempre mostrar mensagem de sucesso por segurança (não revelar emails válidos)
        mensagem = "Se o e-mail estiver cadastrado, você receberá uma mensagem contendo instruções para redefinir sua senha. Cheque sua caixa de entrada e a pasta de spam e siga as instruções para redefinir sua senha."

        # Se não encontrar usuário, não informar ao usuário por segurança
        if not usuario:
            # Logar a tentativa para auditoria
            logger.warning(
                f"Solicitação de redefinição de senha para e-mail não cadastrado: {esqueci_senha_dto.email}"
            )

            # Retornar template com mensagem de sucesso fictícia
            return templates.TemplateResponse(
                "publico/esqueci_senha.html", {"request": request, "mensagem": mensagem}
            )

        # Se encontrar o usuário, gerar token e enviar email
        else:
            # Logar a solicitação para auditoria
            logger.info(
                f"Solicitação de redefinição de senha para email: {esqueci_senha_dto.email}"
            )
            # Gerar token de redefinição de senha
            token = gerar_token_redefinicao()
            # Obter data de expiração (24 horas)
            data_expiracao = obter_data_expiracao_token(24)
            # Atualizar usuário com token e data de expiração
            usuario_repo.atualizar_token(email, token, data_expiracao)

            # TODO: Enviar email com o link de redefinição

            # Dados para retornar template com mensagem de sucesso
            response_data = {
                "request": request,
                "sucesso": mensagem,
            }

            # Se o site não estiver publicado, mostrar o link de redefinição para facilitar testes
            if os.getenv("ENVIRONMENT", "development") == "development":
                link_redefinicao = f"http://localhost:8000/redefinir-senha/{token}"
                response_data["debug_link"] = link_redefinicao

            # Retornar template com mensagem de sucesso
            return templates.TemplateResponse(
                "publico/esqueci_senha.html", response_data
            )

    # Processar erros de validação do DTO
    except ValidationError as e:
        # Obter dicionário com erros de validação
        erros = processar_erros_validacao(e)

        # Logar os erros de validação para auditoria
        logger.warning(
            f"Erros de validação na solicitação de redefinição de senha: {' | '.join([f'{erro.key}: {erro.value}' for erro in erros])}"
        )

        # Retornar template com erros
        return templates.TemplateResponse(
            "publico/esqueci_senha.html",
            {"request": request, "erros": erros, "dados": dados_formulario},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.get("/redefinir-senha/{token}")
async def get_redefinir_senha(request: Request, token: str):
    # Verificar se existe um usuário com o token fornecido
    usuario = usuario_repo.obter_por_token(token)

    # Se não encontrar, informar erro
    if not usuario:
        return templates.TemplateResponse(
            "redefinir_senha.html",
            {
                "request": request,
                "erros": {"geral": "Link de redefinição de senha inválido ou expirado"},
            },
        )

    # Se encontrar, mostrar formulário de redefinição de senha
    else:
        return templates.TemplateResponse(
            "redefinir_senha.html", {"request": request, "token": token}
        )


@router.post("/redefinir-senha/{token}")
@limiter.limit("5/hour")  # limite de 5 tentativas por hora
async def post_redefinir_senha(
    request: Request,
    token: str,
    senha: str = Form(...),
    confirmar_senha: str = Form(...),
):
    try:
        # Validar usando DTO apropriado
        redefinir_senha_dto = RedefinirSenhaDTO(
            senha=senha, confirmar_senha=confirmar_senha
        )

        # Verificar se existe um usuário com o token fornecido
        usuario = usuario_repo.obter_por_token(token)

        # Se não encontrar, informar erro
        if not usuario:
            return templates.TemplateResponse(
                "redefinir_senha.html",
                {
                    "request": request,
                    "erros": {
                        "geral": "Link de redefinição de senha inválido ou expirado"
                    },
                },
            )

        # Se encontrar, prosseguir com a redefinição de senha
        else:
            # Atualizar senha e limpar token
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

    # Processar erros de validação do DTO
    except ValidationError as e:
        # Obter dicionário com erros de validação
        erros = processar_erros_validacao(e)

        # Logar os erros de validação para auditoria
        logger.warning(
            f"Erros de validação na redefinição de senha: {' | '.join([f'{erro.key}: {erro.value}' for erro in erros])}"
        )

        # Retornar template com erros
        return templates.TemplateResponse(
            "publico/redefinir_senha.html",
            {
                "request": request,
                "erros": erros,
                "token": token,
            },
        )
