from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from pydantic_core import ValidationError

from dtos.login_dto import LoginDTO
from model.tutor_model import Tutor
from model.veterinario_model import Veterinario
from repo import usuario_repo, tutor_repo, veterinario_repo
from util.security import criar_hash_senha, verificar_senha, gerar_token_redefinicao, obter_data_expiracao_token, validar_forca_senha
from util.auth_decorator import criar_sessao, destruir_sessao, esta_logado
from util.template_util import criar_templates

router = APIRouter()
templates = criar_templates("templates/publico")


@router.get("/login")
async def get_login(request: Request, redirect: str = None):
    # Se já está logado, redirecionar
    if esta_logado(request):
        return RedirectResponse("/", status.HTTP_303_SEE_OTHER)
    
    return templates.TemplateResponse(
        "login.html", 
        {"request": request, "redirect": redirect}
    )


@router.post("/login")
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
                    "erro": "Email ou senha inválidos",
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
        
        if usuario.perfil == "admin":
            url_redirect = "/perfil/{usuario.id_usuario}"
            return RedirectResponse(url_redirect, status.HTTP_303_SEE_OTHER)
        
        # Redirecionar para a página solicitada ou home
        # url_redirect = redirect if redirect else "/"
        # return RedirectResponse(url_redirect, status.HTTP_303_SEE_OTHER)
        url_redirect = f"/perfil/{usuario.id_usuario}"
        return RedirectResponse(url_redirect, status.HTTP_303_SEE_OTHER)
    
    
    except ValidationError as e:
        # Extrair mensagens de erro do Pydantic
        erros = []
        for erro in e.errors():
            campo = erro['loc'][0] if erro['loc'] else 'campo'
            mensagem = erro['msg']
            erros.append(f"{campo.capitalize()}: {mensagem}")

        erro_msg = " | ".join(erros)
        # logger.warning(f"Erro de validação no cadastro: {erro_msg}")

        # Retornar template com dados preservados e erro
        return templates.TemplateResponse("login.html", {
            "request": request,
            "erro": erro_msg,
            "dados": dados_formulario  # Preservar dados digitados
        })

    except Exception as e:
        # logger.error(f"Erro ao processar cadastro: {e}")

        return templates.TemplateResponse("login.html", {
            "request": request,
            "erro": "Erro ao processar cadastro. Tente novamente.",
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
async def post_cadastro(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    senha: str = Form(...),
    confirmar_senha: str = Form(...),
    perfil: str = Form(...), # TODO: adicionar restricao para aceitar apenas 'tutor' ou 'veterinario'
    crmv: str = Form(None)
):
    # Veterinario
    # verificado: bool -> definido depois
    # bio: str -> cadastrado depois

    # Tutor
    # quantidade_pets: int = 0 -> cadastrado depois
    # descricao_pets: Optional[str] = None -> cadastrado depois

    # Validações
    if senha != confirmar_senha:
        return templates.TemplateResponse(
            "cadastro.html",
            {
                "request": request,
                "erro": "As senhas não coincidem",
                "nome": nome,
                "email": email,                
                "telefone": telefone,
                "perfil": perfil,
                "crmv": crmv
            }
        )
    
    # Validar força da senha
    senha_valida, msg_erro = validar_forca_senha(senha)
    if not senha_valida:
        return templates.TemplateResponse(
            "cadastro.html",
            {
                "request": request,
                "erro": msg_erro,
                "nome": nome,
                "email": email,
                "telefone": telefone,
                "perfil": perfil,
                "crmv": crmv
            }
        )
    
    # Verificar se email já existe
    if usuario_repo.obter_por_email(email):
        return templates.TemplateResponse(
            "cadastro.html",
            {
                "request": request,
                "erro": msg_erro,
                "nome": nome,
                "email": email,
                "telefone": telefone,
                "perfil": perfil,
                "crmv": crmv
            }
        )
    
    try:
        id_usuario = None
        if perfil == 'tutor':
        # Criar usuário com senha hash
            tutor = Tutor(
                id_usuario=0,
                nome=nome,
                email=email,
                senha=criar_hash_senha(senha),
                telefone=telefone,
                perfil=perfil,
                foto=None,
                token_redefinicao=None,
                data_token=None,
                data_cadastro=None,
                quantidade_pets=0,
                descricao_pets=None
            )
            id_usuario = tutor_repo.inserir_tutor(tutor)
            
        else:
            veterinario = Veterinario(                                
                id_usuario=0,
                nome=nome,
                email=email,
                senha=criar_hash_senha(senha),
                telefone=telefone,
                perfil=perfil,
                foto=None,
                token_redefinicao=None,
                data_token=None,
                data_cadastro=None,
                crmv=crmv, 
                verificado=False,
                bio=None
            )
            id_usuario = veterinario_repo.inserir_veterinario(veterinario)
        
        if not id_usuario:
            raise Exception("Erro ao inserir usuário no banco de dados.")
        
        return RedirectResponse("/login", status.HTTP_303_SEE_OTHER)
        
    except Exception as e:
        return templates.TemplateResponse(
            "cadastro.html",
            {
                "request": request,
                "erro": f"Erro ao criar cadastro. Tente novamente. {e}",
                "nome": nome,
                "email": email,                
                "telefone": telefone,
                "perfil": perfil,
                "crmv": crmv
            }
        )


@router.get("/esqueci-senha")
async def get_esqueci_senha(request: Request):
    return templates.TemplateResponse("esqueci_senha.html", {"request": request})


@router.post("/esqueci-senha")
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
        # Por enquanto, vamos apenas mostrar o link (em produção, remover isso)
        link_redefinicao = f"http://localhost:8000/redefinir-senha/{token}"
        
        return templates.TemplateResponse(
            "esqueci_senha.html",
            {
                "request": request,
                "sucesso": mensagem_sucesso,
                "debug_link": link_redefinicao  # Remover em produção
            }
        )
    
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
    usuario_repo.atualizar_senha_usuario(usuario.id_usuario, senha_hash)
    usuario_repo.limpar_token(usuario.id)
    
    return templates.TemplateResponse(
        "redefinir_senha.html",
        {
            "request": request,
            "sucesso": "Senha redefinida com sucesso! Você já pode fazer login."
        }
    )
