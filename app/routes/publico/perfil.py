import os
import logging
from fastapi import APIRouter, Form, Request, status, UploadFile, File
from fastapi.responses import RedirectResponse
from typing import Optional

from model.usuario_model import Usuario
from model.tutor_model import Tutor
from model.veterinario_model import Veterinario
from repo import usuario_repo, tutor_repo
from util.security import criar_hash_senha, verificar_senha, validar_forca_senha
from util.auth_decorator import requer_autenticacao, obter_usuario_logado
from util.template_util import criar_templates
from repo import veterinario_repo
from util.file_validator import FileValidator, FileValidationError
from util.file_manager import FileManager
from config.upload_config import UploadConfig

logger = logging.getLogger(__name__)

router = APIRouter()
templates = criar_templates("templates/publico")

@router.get("/")
@requer_autenticacao()
async def perfil(request: Request, usuario_logado: Optional[dict] = None):
    from typing import Union
    usuario: Union[Tutor, Veterinario, None] = None
    if usuario_logado and usuario_logado['perfil'] == 'tutor':
        usuario = tutor_repo.obter_por_id(usuario_logado['id'])
    elif usuario_logado and usuario_logado['perfil'] == 'veterinario':
        usuario = veterinario_repo.obter_por_id(usuario_logado['id'])
    return templates.TemplateResponse(
        "perfil.html",
        {
            "request": request,
            "usuario": usuario,
        }
    )

@router.get("/alterar")
@requer_autenticacao()
async def get_perfil(request: Request, usuario_logado: Optional[dict] = None):
    if not usuario_logado:
        return RedirectResponse("/", status.HTTP_303_SEE_OTHER)

    usuario = usuario_repo.obter_usuario_por_id(usuario_logado['id'])
    if not usuario:
        return RedirectResponse("/", status.HTTP_303_SEE_OTHER)

    from typing import Union, Any
    dados_perfil: Union[Tutor, Veterinario, Any, None] = None
    perfil = usuario.perfil.lower()

    if perfil == 'tutor':
        dados_perfil = tutor_repo.obter_por_id(usuario.id_usuario)
    elif perfil == 'veterinario':
        dados_perfil = veterinario_repo.obter_por_id(usuario.id_usuario)
    elif perfil == 'administrador':
        from repo import administrador_repo
        dados_perfil = administrador_repo.obter_administrador_por_id(usuario.id_usuario)

    return templates.TemplateResponse(
        "dados.html",
        {
            "request": request,
            "usuario": usuario,
            "dados_perfil": dados_perfil
        }
    )

@router.post("/alterar")
@requer_autenticacao()
async def post_perfil(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(None),
    usuario_logado: Optional[dict] = None
):
    if not usuario_logado:
        return RedirectResponse("/", status.HTTP_303_SEE_OTHER)

    usuario = usuario_repo.obter_usuario_por_id(usuario_logado['id'])
    if not usuario:
        return RedirectResponse("/", status.HTTP_303_SEE_OTHER)

    # Verificar se o email já está em uso por outro usuário
    usuario_existente = usuario_repo.obter_por_email(email)
    if usuario_existente and usuario_existente.id_usuario != usuario.id_usuario:
        tutor_dados = None
        if usuario.perfil == 'tutor':
            try:
                from util.db_util import get_connection
                with get_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT cpf, telefone FROM cliente WHERE id=?", (usuario.id_usuario,))
                    row = cursor.fetchone()
                    if row:
                        tutor_dados = {
                            'telefone': row['telefone']
                        }
            except:
                pass
        
        return templates.TemplateResponse(
            "dados.html",
            {
                "request": request,
                "usuario": usuario,
                "tutor_dados":tutor_dados,
                "erro": "Este email já está em uso"
            }
        )
    
    # Atualizar dados do usuário
    usuario.nome = nome
    usuario.email = email
    usuario_repo.atualizar_usuario(usuario)
    
    # Se for cliente, atualizar dados adicionais
    if usuario.perfil == 'tutor' and telefone:
        try:
            from util.db_util import get_connection
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE cliente SET telefone=? WHERE id=?",
                    (telefone, usuario.id_usuario)
                )
                conn.commit()
        except Exception as e:
            print(f"Erro ao atualizar telefone do tutor: {e}")

    # Atualizar sessão
    from util.auth_decorator import criar_sessao
    usuario_dict = {
        "id": usuario.id_usuario,
        "nome": nome,
        "email": email,
        "perfil": usuario.perfil,
        "foto": usuario.foto
    }
    criar_sessao(request, usuario_dict)
    
    return RedirectResponse("/perfil?sucesso=1", status.HTTP_303_SEE_OTHER)


@router.get("/alterar-senha")
@requer_autenticacao()
async def get_alterar_senha(request: Request, usuario_logado: Optional[dict] = None):
    return templates.TemplateResponse(
        "alterar_senha.html",
        {"request": request}
    )


@router.post("/alterar-senha")
@requer_autenticacao()
async def post_alterar_senha(
    request: Request,
    senha_atual: str = Form(...),
    senha_nova: str = Form(...),
    confirmar_senha: str = Form(...),
    usuario_logado: Optional[dict] = None
):
    if not usuario_logado:
        return RedirectResponse("/", status.HTTP_303_SEE_OTHER)

    usuario = usuario_repo.obter_usuario_por_id(usuario_logado['id'])
    if not usuario:
        return RedirectResponse("/", status.HTTP_303_SEE_OTHER)

    # Verificar senha atual
    if not verificar_senha(senha_atual, usuario.senha):
        return templates.TemplateResponse(
            "alterar_senha.html",
            {
                "request": request,
                "erro": "Senha atual incorreta"
            }
        )
    
    # Verificar se as novas senhas coincidem
    if senha_nova != confirmar_senha:
        return templates.TemplateResponse(
            "alterar_senha.html",
            {
                "request": request,
                "erro": "As novas senhas não coincidem"
            }
        )
    
    # Validar força da nova senha
    senha_valida, msg_erro = validar_forca_senha(senha_nova)
    if not senha_valida:
        return templates.TemplateResponse(
            "alterar_senha.html",
            {
                "request": request,
                "erro": msg_erro
            }
        )
    
    # Atualizar senha
    senha_hash = criar_hash_senha(senha_nova)
    usuario_repo.atualizar_senha_usuario(usuario.id_usuario, senha_hash)
    
    return templates.TemplateResponse(
        "alterar_senha.html",
        {
            "request": request,
            "sucesso": "Senha alterada com sucesso!"
        }
    )


@router.post("/alterar-foto")
@requer_autenticacao()
async def alterar_foto(
    request: Request,
    foto: UploadFile = File(...),
    usuario_logado: Optional[dict] = None
):
    """
    Endpoint para alteração de foto de perfil

    Validações realizadas:
    - Tipo de arquivo (magic bytes)
    - Tamanho do arquivo
    - Dimensões da imagem
    - Nome do arquivo (path traversal)
    - Permissões do sistema
    """
    if not usuario_logado:
        logger.warning("Tentativa de upload sem autenticação")
        return RedirectResponse("/", status.HTTP_303_SEE_OTHER)

    usuario_id = usuario_logado['id']
    logger.info(f"Iniciando upload de foto para usuário {usuario_id}")

    try:
        # 1. Validação completa do arquivo
        try:
            conteudo, extensao = await FileValidator.validar_imagem_completo(
                foto,
                max_size=UploadConfig.MAX_FILE_SIZE
            )
        except FileValidationError as e:
            logger.warning(f"Validação falhou para usuário {usuario_id}: {e}")
            return RedirectResponse(
                f"/perfil?erro={str(e)}",
                status.HTTP_303_SEE_OTHER
            )

        # 2. Verificar espaço em disco
        if not FileManager.verificar_espaco_disco(len(conteudo)):
            logger.error("Espaço em disco insuficiente")
            return RedirectResponse(
                "/perfil?erro=Espaço em disco insuficiente",
                status.HTTP_303_SEE_OTHER
            )

        # 3. Obter foto atual do usuário
        usuario = usuario_repo.obter_usuario_por_id(usuario_id)
        if not usuario:
            logger.error(f"Usuário {usuario_id} não encontrado")
            return RedirectResponse("/", status.HTTP_303_SEE_OTHER)

        foto_antiga = usuario.foto

        # 4. Gerar nome seguro para novo arquivo
        nome_arquivo = FileValidator.gerar_nome_arquivo_seguro(extensao)

        # 5. Salvar novo arquivo
        try:
            caminho_relativo = FileManager.salvar_arquivo(
                conteudo,
                nome_arquivo,
                usuario_id
            )
        except (PermissionError, OSError) as e:
            logger.error(f"Erro ao salvar arquivo: {e}", exc_info=True)
            return RedirectResponse(
                "/perfil?erro=Erro ao salvar arquivo. Contate o administrador.",
                status.HTTP_303_SEE_OTHER
            )

        # 6. Atualizar banco de dados
        try:
            usuario_repo.atualizar_foto(usuario_id, caminho_relativo)
        except Exception as e:
            logger.error(f"Erro ao atualizar banco: {e}", exc_info=True)
            # Rollback: deletar arquivo recém-criado
            FileManager.deletar_foto_antiga(caminho_relativo)
            return RedirectResponse(
                "/perfil?erro=Erro ao atualizar perfil",
                status.HTTP_303_SEE_OTHER
            )

        # 7. Deletar foto antiga (LGPD compliance)
        if foto_antiga:
            FileManager.deletar_foto_antiga(foto_antiga)

        # 8. Atualizar sessão
        usuario_logado['foto'] = caminho_relativo
        from util.auth_decorator import criar_sessao
        criar_sessao(request, usuario_logado)

        logger.info(f"Upload concluído com sucesso para usuário {usuario_id}")
        return RedirectResponse("/perfil?foto_sucesso=1", status.HTTP_303_SEE_OTHER)

    except Exception as e:
        # Catch-all para erros inesperados
        logger.error(
            f"Erro inesperado no upload do usuário {usuario_id}: {e}",
            exc_info=True
        )
        return RedirectResponse(
            "/perfil?erro=Erro inesperado. Tente novamente.",
            status.HTTP_303_SEE_OTHER
        )
