from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from pydantic_core import ValidationError
from typing import Optional
import os
import logging
from enum import Enum
from slowapi import Limiter
from slowapi.util import get_remote_address

# Configurar logger
logger = logging.getLogger(__name__)


# Enum para perfis de usuário
class PerfilUsuario(str, Enum):
    TUTOR = "tutor"
    VETERINARIO = "veterinario"

from app.schemas.cadastro_dto import CadastroTutorDTO, CadastroVeterinarioDTO
from app.schemas.login_dto import LoginDTO
from model.tutor_model import Tutor
from model.veterinario_model import Veterinario
from app.repositories import usuario_repo, tutor_repo, veterinario_repo
from util.security import criar_hash_senha, verificar_senha, gerar_token_redefinicao, obter_data_expiracao_token, validar_forca_senha
from util.auth_decorator import criar_sessao, destruir_sessao, esta_logado
from util.template_util import criar_templates

router = APIRouter()
templates = criar_templates("templates/publico")

# Configurar rate limiter
limiter = Limiter(key_func=get_remote_address)


def processar_erros_validacao(e: ValidationError) -> dict:
    """
    Processa erros de validação do Pydantic.

    Args:
        e: Exceção de validação

    Returns:
        Dicionário de erros formatados
    """
    erros = {}
    for erro in e.errors():
        campo = erro['loc'][0] if erro['loc'] else 'campo'
        mensagem = erro['msg'].replace('Value error, ', '')
        erros[str(campo).upper()] = mensagem
    return erros


@router.get("/login")
async def get_login(request: Request, redirect: Optional[str] = None):
    # Se já está logado, redirecionar
    if esta_logado(request):
        return RedirectResponse("/", status.HTTP_303_SEE_OTHER)
    
    return templates.TemplateResponse(
        "login.html", 
        {"request": request, "redirect": redirect}
    )


@router.post("/login")
@limiter.limit("5/minute")  # 5 tentativas por minuto
async def post_login(
    request: Request,
    email: str = Form(),
    senha: str = Form(),
    redirect: str = Form(None)
):
    dados_formulario = {
        "email": email
    }
    
    try:
        login_dto = LoginDTO(email=email, senha=senha)
        
        # Buscar usuário pelo email
        usuario = usuario_repo.obter_por_email(login_dto.email)
        
        if not usuario or not verificar_senha(login_dto.senha, usuario.senha):
            return templates.TemplateResponse(
                "login.html",
                {
                    "request": request,
                    "erros": {"EMAIL": "Credenciais inválidas."},
                    "email": email,
                    "redirect": redirect
                }
            )
        
        # Criar sessão
        usuario_dict = {
            "id": usuario.id_usuario,
            "nome": usuario.nome,
            "email": usuario.email,
            "telefone": usuario.telefone,
            "perfil": usuario.perfil,
            "foto": usuario.foto
        }
        criar_sessao(request, usuario_dict)
        
        # if usuario.perfil == "admin":
        #     url_redirect = "/perfil/{usuario.id_usuario}"
        #     return RedirectResponse(url_redirect, status.HTTP_303_SEE_OTHER)
        
        # Redirecionar para a página solicitada ou home
        # url_redirect = redirect if redirect else "/"
        # return RedirectResponse(url_redirect, status.HTTP_303_SEE_OTHER)
        # url_redirect = f"/perfil/{usuario.id_usuario}"
        # 
        url_redirect = f"/"
        return RedirectResponse(url_redirect, status.HTTP_303_SEE_OTHER)
    
    
    except ValidationError as e:
        erros = processar_erros_validacao(e)
        logger.warning(f"Erro de validação no login - Email: {email} - Erros: {e.errors()}")

        return templates.TemplateResponse("login.html", {
            "request": request,
            "erros": erros,
            "dados": dados_formulario,
            "redirect": redirect
        }, status_code=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"Erro crítico ao processar login - Email: {email} - Erro: {str(e)}", exc_info=True)

        return templates.TemplateResponse("login.html", {
            "request": request,
            "erros": {"GERAL": "Erro ao processar o login. Tente novamente."},
            "dados": dados_formulario
        })


@router.get("/logout")
async def logout(request: Request):
    destruir_sessao(request)
    return RedirectResponse("/", status.HTTP_303_SEE_OTHER)


@router.get("/cadastro")
async def get_cadastro(request: Request):
    # Se já está logado, redirecionar
    if esta_logado(request):
        return RedirectResponse("/", status.HTTP_303_SEE_OTHER)
    
    return templates.TemplateResponse("cadastro.html", {"request": request})


@router.post("/cadastro")
@limiter.limit("3/hour")  # 3 cadastros por hora por IP
async def post_cadastro(
    request: Request,
    nome: str = Form(),
    email: str = Form(),
    telefone: str = Form(),
    senha: str = Form(),
    confirmar_senha: str = Form(),
    perfil: PerfilUsuario = Form(),
    crmv: str = Form(None)
):
    dados_formulario = {
        "nome": nome,
        "email": email,
        "telefone": telefone,
        "perfil": perfil.value,
        "crmv": crmv
    }

    try:
        # Validar força da senha antes de criar DTO
        senha_valida, msg_erro = validar_forca_senha(senha)
        if not senha_valida:
            return templates.TemplateResponse(
                "cadastro.html",
                {
                    "request": request,
                    "erros": {"SENHA": msg_erro},
                    "dados": dados_formulario
                },
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # Verificar se email já existe (mensagem genérica por segurança)
        if usuario_repo.obter_por_email(email.strip().lower()):
            logger.warning(f"Tentativa de cadastro com email existente: {email}")
            return templates.TemplateResponse(
                "cadastro.html",
                {
                    "request": request,
                    "erros": {"GERAL": "Não foi possível completar o cadastro. Verifique os dados."},
                    "dados": dados_formulario
                },
                status_code=status.HTTP_409_CONFLICT
            )

        # Validar usando DTO apropriado e criar usuário
        id_usuario: int | None = None
        cadastro_dto: CadastroTutorDTO | CadastroVeterinarioDTO
        if perfil == PerfilUsuario.TUTOR:
            cadastro_dto = CadastroTutorDTO(
                nome=nome,
                email=email,
                telefone=telefone,
                senha=senha,
                confirmar_senha=confirmar_senha,
                perfil=perfil.value
            )

            tutor = Tutor(
                id_usuario=0,
                nome=cadastro_dto.nome,
                email=cadastro_dto.email,
                senha=criar_hash_senha(cadastro_dto.senha),
                telefone=cadastro_dto.telefone,
                perfil=perfil.value,
                foto=None,
                token_redefinicao=None,
                data_token=None,
                data_cadastro=None,
                quantidade_pets=0,
                descricao_pets=None
            )
            id_usuario = tutor_repo.inserir(tutor)
            assert id_usuario is not None

        else:
            if not crmv:
                raise ValueError("CRMV é obrigatório para veterinários")

            cadastro_dto = CadastroVeterinarioDTO(
                nome=nome,
                email=email,
                telefone=telefone,
                senha=senha,
                confirmar_senha=confirmar_senha,
                perfil=perfil.value,
                crmv=crmv
            )

            veterinario = Veterinario(
                id_usuario=0,
                nome=cadastro_dto.nome,
                email=cadastro_dto.email,
                senha=criar_hash_senha(cadastro_dto.senha),
                telefone=cadastro_dto.telefone,
                perfil=perfil.value,
                foto=None,
                token_redefinicao=None,
                data_token=None,
                data_cadastro=None,
                crmv=cadastro_dto.crmv,
                verificado=False,
                bio=None
            )
            id_usuario = veterinario_repo.inserir(veterinario)
            assert id_usuario is not None

        if not id_usuario:
            raise Exception("Erro ao inserir usuário no banco de dados.")

        logger.info(f"Novo usuário cadastrado com sucesso. ID: {id_usuario}")
        return RedirectResponse("/login?cadastro=sucesso", status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        erros = processar_erros_validacao(e)
        logger.warning(f"Erro de validação no cadastro - Email: {email} - Erros: {e.errors()}")

        return templates.TemplateResponse("cadastro.html", {
            "request": request,
            "erros": erros,
            "dados": dados_formulario
        }, status_code=status.HTTP_400_BAD_REQUEST)

    except ValueError as e:
        logger.warning(f"Erro de valor no cadastro: {str(e)}")
        return templates.TemplateResponse("cadastro.html", {
            "request": request,
            "erros": {"GERAL": str(e)},
            "dados": dados_formulario
        }, status_code=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"Erro crítico ao processar cadastro - Email: {email} - Erro: {str(e)}", exc_info=True)

        return templates.TemplateResponse("cadastro.html", {
            "request": request,
            "erros": {"GERAL": "Erro ao processar o cadastro. Tente novamente."},
            "dados": dados_formulario
        }, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/esqueci-senha")
async def get_esqueci_senha(request: Request):
    return templates.TemplateResponse("esqueci_senha.html", {"request": request})


@router.post("/esqueci-senha")
@limiter.limit("3/hour")  # 3 tentativas por hora
async def post_esqueci_senha(
    request: Request,
    email: str = Form(...)
):
    usuario = usuario_repo.obter_por_email(email)
    
    # Sempre mostrar mensagem de sucesso por segurança (não revelar emails válidos)
    mensagem_sucesso = "Se o email estiver cadastrado, você receberá instruções para redefinir sua senha."
    
    if usuario:
        # Gerar token e salvar no banco
        token = gerar_token_redefinicao()
        data_expiracao = obter_data_expiracao_token(24)  # 24 horas
        usuario_repo.atualizar_token(email, token, data_expiracao)

        # TODO: Enviar email com o link de redefinição
        response_data = {
            "request": request,
            "sucesso": mensagem_sucesso
        }

        # Apenas mostrar debug_link em ambiente de desenvolvimento
        if os.getenv("ENVIRONMENT", "development") == "development":
            link_redefinicao = f"http://localhost:8000/redefinir-senha/{token}"
            response_data["debug_link"] = link_redefinicao

        return templates.TemplateResponse("esqueci_senha.html", response_data)
    
    return templates.TemplateResponse(
        "esqueci_senha.html",
        {
            "request": request,
            "sucesso": mensagem_sucesso
        }
    )


@router.get("/redefinir-senha/{token}")
async def get_redefinir_senha(request: Request, token: str):
    usuario = usuario_repo.obter_por_token(token)
    
    if not usuario:
        return templates.TemplateResponse(
            "redefinir_senha.html",
            {
                "request": request,
                "erro": "Link inválido ou expirado"
            }
        )
    
    return templates.TemplateResponse(
        "redefinir_senha.html",
        {
            "request": request,
            "token": token
        }
    )


@router.post("/redefinir-senha/{token}")
@limiter.limit("5/hour")  # 5 tentativas por hora
async def post_redefinir_senha(
    request: Request,
    token: str,
    senha: str = Form(...),
    confirmar_senha: str = Form(...)
):
    usuario = usuario_repo.obter_por_token(token)
    
    if not usuario:
        return templates.TemplateResponse(
            "redefinir_senha.html",
            {
                "request": request,
                "erro": "Link inválido ou expirado"
            }
        )
    
    # Validações
    if senha != confirmar_senha:
        return templates.TemplateResponse(
            "redefinir_senha.html",
            {
                "request": request,
                "token": token,
                "erro": "As senhas não coincidem"
            }
        )
    
    # Validar força da senha
    senha_valida, msg_erro = validar_forca_senha(senha)
    if not senha_valida:
        return templates.TemplateResponse(
            "redefinir_senha.html",
            {
                "request": request,
                "token": token,
                "erro": msg_erro
            }
        )
    
    # Atualizar senha e limpar token
    senha_hash = criar_hash_senha(senha)
    usuario_repo.atualizar_senha(usuario.id_usuario, senha_hash)
    usuario_repo.limpar_token(usuario.id_usuario)
    
    return templates.TemplateResponse(
        "redefinir_senha.html",
        {
            "request": request,
            "sucesso": "Senha redefinida com sucesso! Você já pode fazer login."
        }
    )
