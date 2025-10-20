from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import RedirectResponse
from util.auth_decorator import requer_autenticacao
from util.template_util import criar_templates
from util.mensagens import adicionar_mensagem_sucesso, adicionar_mensagem_erro
from repo import postagem_feed_repo
from model.postagem_feed_model import PostagemFeed
from util.file_validator import FileValidator
from util.file_manager import FileManager
from config.upload_config import UploadConfig
from datetime import datetime

router = APIRouter(prefix="/tutor")
templates = criar_templates("templates/tutor")

@router.get("/")
@requer_autenticacao(perfis_autorizados=["tutor"])
async def get_home_tutor(request: Request, usuario_logado: dict = None):
    """Dashboard do tutor"""
    # Buscar posts do tutor
    posts = postagem_feed_repo.obter_por_tutor(usuario_logado['id'])  # Criar função

    return templates.TemplateResponse("tutor/home_tutor.html", {
        "request": request,
        "posts": posts,
        "total_posts": len(posts)
    })

@router.get("/listar_postagem_feed")
@requer_autenticacao(perfis_autorizados=["tutor"])
async def get_listar_postagens(request: Request, usuario_logado: dict = None):
    """Lista todos os posts do tutor"""
    posts = postagem_feed_repo.obter_por_tutor(usuario_logado['id'])

    return templates.TemplateResponse("tutor/listar_postagens_feed.html", {
        "request": request,
        "posts": posts
    })

@router.get("/fazer_postagem_feed")
@requer_autenticacao(perfis_autorizados=["tutor"])
async def get_fazer_postagem(request: Request):
    """Formulário de nova postagem"""
    return templates.TemplateResponse("tutor/fazer_postagem_feed.html", {
        "request": request
    })

@router.post("/fazer_postagem_feed")
@requer_autenticacao(perfis_autorizados=["tutor"])
async def post_fazer_postagem(
    request: Request,
    descricao: str = Form(...),
    foto: UploadFile = File(...),
    usuario_logado: dict = None
):
    """Cria nova postagem com upload de foto"""
    from dtos.postagem_feed_dto import PostagemFeedDTO

    # 1. Validar campos
    try:
        dto = PostagemFeedDTO(descricao=descricao)
    except Exception as e:
        adicionar_mensagem_erro(request, str(e))
        return RedirectResponse("/tutor/fazer_postagem_feed", status_code=303)

    # 2. Validar imagem
    try:
        conteudo, extensao = await FileValidator.validar_imagem_completo(
            foto, max_size=UploadConfig.MAX_FILE_SIZE
        )
    except Exception as e:
        adicionar_mensagem_erro(request, f"Erro na imagem: {e}")
        return RedirectResponse("/tutor/fazer_postagem_feed", status_code=303)

    # 3. Criar postagem no banco
    post = PostagemFeed(
        id_postagem_feed=0,
        id_tutor=usuario_logado['id'],
        descricao=dto.descricao,
        data_postagem=datetime.now(),
        visualizacoes=0
    )

    id_post = postagem_feed_repo.inserir(post)

    if not id_post:
        adicionar_mensagem_erro(request, "Erro ao criar postagem.")
        return RedirectResponse("/tutor/fazer_postagem_feed", status_code=303)

    # 4. Salvar imagem com ID do post
    nome_arquivo = f"{id_post:08d}{extensao}"
    try:
        FileManager.salvar_arquivo(
            conteudo,
            nome_arquivo,
            id_post,
            subpasta="feeds"
        )
    except Exception as e:
        # Rollback: excluir postagem se falhar upload
        postagem_feed_repo.excluir(id_post)
        adicionar_mensagem_erro(request, "Erro ao salvar imagem.")
        return RedirectResponse("/tutor/fazer_postagem_feed", status_code=303)

    adicionar_mensagem_sucesso(request, "Post publicado com sucesso!")
    return RedirectResponse("/tutor/listar_postagem_feed", status_code=303)

@router.get("/editar_postagem_feed/{id_postagem}")
@requer_autenticacao(perfis_autorizados=["tutor"])
async def get_editar_postagem(
    request: Request,
    id_postagem: int,
    usuario_logado: dict = None
):
    """Formulário de edição (apenas descrição)"""
    post = postagem_feed_repo.obter_por_id(id_postagem)

    if not post or post.id_tutor != usuario_logado['id']:
        adicionar_mensagem_erro(request, "Postagem não encontrada ou sem permissão.")
        return RedirectResponse("/tutor/listar_postagem_feed", status_code=303)

    return templates.TemplateResponse("tutor/editar_postagem_feed.html", {
        "request": request,
        "post": post
    })

@router.post("/editar_postagem_feed")
@requer_autenticacao(perfis_autorizados=["tutor"])
async def post_editar_postagem(
    request: Request,
    id_postagem: int = Form(...),
    descricao: str = Form(...),
    usuario_logado: dict = None
):
    """Atualiza descrição do post"""
    post = postagem_feed_repo.obter_por_id(id_postagem)

    if not post or post.id_tutor != usuario_logado['id']:
        adicionar_mensagem_erro(request, "Sem permissão.")
        return RedirectResponse("/tutor/listar_postagem_feed", status_code=303)

    post.descricao = descricao
    if postagem_feed_repo.atualizar(post):
        adicionar_mensagem_sucesso(request, "Post atualizado!")
    else:
        adicionar_mensagem_erro(request, "Erro ao atualizar.")

    return RedirectResponse("/tutor/listar_postagem_feed", status_code=303)

@router.get("/excluir_postagem_feed/{id_postagem}")
@requer_autenticacao(perfis_autorizados=["tutor"])
async def get_excluir_postagem(
    request: Request,
    id_postagem: int,
    usuario_logado: dict = None
):
    """Confirmação de exclusão"""
    post = postagem_feed_repo.obter_por_id(id_postagem)

    if not post or post.id_tutor != usuario_logado['id']:
        adicionar_mensagem_erro(request, "Postagem não encontrada.")
        return RedirectResponse("/tutor/listar_postagem_feed", status_code=303)

    return templates.TemplateResponse("tutor/excluir_postagem_feed.html", {
        "request": request,
        "post": post
    })

@router.post("/excluir_postagem_feed")
@requer_autenticacao(perfis_autorizados=["tutor"])
async def post_excluir_postagem(
    request: Request,
    id_postagem: int = Form(...),
    usuario_logado: dict = None
):
    """Exclui postagem e imagem"""
    post = postagem_feed_repo.obter_por_id(id_postagem)

    if not post or post.id_tutor != usuario_logado['id']:
        adicionar_mensagem_erro(request, "Sem permissão.")
        return RedirectResponse("/tutor/listar_postagem_feed", status_code=303)

    # Excluir do banco
    if postagem_feed_repo.excluir(id_postagem):
        # Excluir imagem do disco
        FileManager.deletar_imagem_feed(id_postagem)
        adicionar_mensagem_sucesso(request, "Post excluído!")
    else:
        adicionar_mensagem_erro(request, "Erro ao excluir.")

    return RedirectResponse("/tutor/listar_postagem_feed", status_code=303)