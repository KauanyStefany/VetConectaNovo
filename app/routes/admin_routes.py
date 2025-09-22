from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.database.models.categoria_artigo_model import CategoriaArtigo
from app.database.repositories import categoria_artigo_repo, chamado_repo, comentario_repo, denuncia_repo, verificacao_crmv_repo
from app.core.auth_decorator import requer_autenticacao


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
@requer_autenticacao(perfis_autorizados=["admin", "administrador"])
async def get_root(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("administrador/dashboard.html", {"request": request, "usuario": usuario_logado})
    return response

# Rotas de categorias de artigo
@router.get("/categorias")
@requer_autenticacao(perfis_autorizados=["admin", "administrador"])
async def listar_categorias(request: Request, usuario_logado: dict = None):
    categorias = categoria_artigo_repo.obter_categorias_paginado(limite=10, offset=0)
    return templates.TemplateResponse("administrador/categorias.html", {"request": request, "usuario": usuario_logado, "categorias": categorias})

@router.get("/categorias/alterar/{id_categoria}")
@requer_autenticacao(perfis_autorizados=["admin", "administrador"])
async def alterar_categoria(request: Request, id_categoria: int, usuario_logado: dict = None):
    categoria_artigo = categoria_artigo_repo.obter_categoria_por_id(id_categoria)
    if categoria_artigo:
        return templates.TemplateResponse("administrador/alterar_categoria.html", {"request": request, "usuario": usuario_logado, "categoria_artigo": categoria_artigo})
    return templates.TemplateResponse("administrador/alterar_categoria.html", {"request": request, "usuario": usuario_logado, "mensagem": "Categoria não encontrada."})

@router.post("/categorias/alterar")
@requer_autenticacao(perfis_autorizados=["admin", "administrador"])
async def post_categoria_alterar(
    request: Request,
    id_categoria: int = Form(...),
    nome: str = Form(...),
    descricao: str = Form(...),
    usuario_logado: dict = None
):
    categoria = CategoriaArtigo(id_categoria=id_categoria, nome=nome, descricao=descricao)
    if categoria_artigo_repo.atualizar_categoria(categoria):
        return RedirectResponse("/admin/categorias", status_code=303)
    return templates.TemplateResponse("administrador/alterar_categoria.html", {"request": request, "usuario": usuario_logado, "mensagem": "Erro ao alterar categoria."})

@router.get("/categorias/cadastrar")
@requer_autenticacao(perfis_autorizados=["admin", "administrador"])
async def cadastrar_categoria(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("administrador/cadastrar_categoria.html", {"request": request, "usuario": usuario_logado})

@router.post("/categorias/cadastrar")
@requer_autenticacao(perfis_autorizados=["admin", "administrador"])
async def post_categoria_artigo(
    request: Request,
    nome: str = Form(...),
    descricao: str = Form(...),
    usuario_logado: dict = None
):
    categoria = CategoriaArtigo(id_categoria=0, nome=nome, descricao=descricao)
    if categoria_artigo_repo.inserir_categoria(categoria):
        return RedirectResponse("/admin/categorias", status_code=303)
    return templates.TemplateResponse("administrador/cadastrar_categoria.html", {"request": request, "usuario": usuario_logado, "mensagem": "Erro ao cadastrar categoria."})

# Rotas de chamados
@router.get("/chamados")
@requer_autenticacao(perfis_autorizados=["admin", "administrador"])
async def listar_chamados(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("administrador/chamados.html", {"request": request, "usuario": usuario_logado})

# Rotas de comentários
@router.get("/comentarios")
@requer_autenticacao(perfis_autorizados=["admin", "administrador"])
async def listar_comentarios(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("administrador/comentarios.html", {"request": request, "usuario": usuario_logado})

# Rotas de denúncias
@router.get("/denuncias")
@requer_autenticacao(perfis_autorizados=["admin", "administrador"])
async def listar_denuncias(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("administrador/denuncias.html", {"request": request, "usuario": usuario_logado})

# Rotas de verificação CRMV
@router.get("/verificacao-crmv")
@requer_autenticacao(perfis_autorizados=["admin", "administrador"])
async def verificacao_crmv(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("administrador/verificacao_crmv.html", {"request": request, "usuario": usuario_logado})

# Rotas de usuários
@router.get("/usuarios")
@requer_autenticacao(perfis_autorizados=["admin", "administrador"])
async def listar_usuarios(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("administrador/usuarios/listar.html", {"request": request, "usuario": usuario_logado})

@router.get("/usuarios/editar/{id_usuario}")
@requer_autenticacao(perfis_autorizados=["admin", "administrador"])
async def editar_usuario(request: Request, id_usuario: int, usuario_logado: dict = None):
    return templates.TemplateResponse("administrador/usuarios/editar.html", {"request": request, "usuario": usuario_logado, "id_usuario": id_usuario})