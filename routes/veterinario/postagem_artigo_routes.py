from tkinter.tix import Form
from fastapi import APIRouter, File, Request, UploadFile
from fastapi.templating import Jinja2Templates

from repo import postagem_artigo_repo
from util.auth_decorator import requer_autenticacao, obter_usuario_logado
from util.template_util import criar_templates

router = APIRouter(prefix="/veterinario")
templates = criar_templates("templates/veterinario")

@router.get("/")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def get_home_veterinario(request: Request, usuario_logado: dict = None):
    artigos = postagem_artigo_repo.obter_por_veterinario(usuario_logado['id'])  # Criar
    # Calcular estatísticas
    total_visualizacoes = sum(a.visualizacoes for a in artigos)
    # Buscar curtidas totais (criar query)

    return templates.TemplateResponse("veterinario/veterinario_home.html", {
        "request": request,
        "artigos": artigos,
        "total_artigos": len(artigos),
        "total_visualizacoes": total_visualizacoes
    })

@router.get("/listar_postagem_artigo")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def get_listar_postagem_artigo(request: Request):
    return templates.TemplateResponse("veterinario/listar_postagem_artigo.html", {"request": request})

@router.get("/alterar_postagem_artigo/{id_postagem_artigo}")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def get_alterar_postagem_artigo(request: Request, id_postagem_artigo: int):
    return templates.TemplateResponse("veterinario/alterar_postagem_artigo.html", {"request": request})

@router.get("/cadastrar_postagem_artigo")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def get_cadastrar_postagem_artigo(request: Request):
    return templates.TemplateResponse("veterinario/cadastrar_postagem_artigo.html", {"request": request})

@router.post("/cadastrar_postagem_artigo")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def post_cadastrar_artigo(
    request: Request,
    titulo: str = Form(...),
    conteudo: str = Form(...),
    id_categoria_artigo: int = Form(...),
    foto: UploadFile = File(...),
    usuario_logado: dict = None
):
    from model.postagem_artigo_model import PostagemArtigo
    from util.file_util import salvar_arquivo

    # Salvar foto
    caminho_foto = salvar_arquivo(foto, "static/uploads/artigos")

    # Criar nova postagem de artigo
    novo_artigo = PostagemArtigo(
        id_postagem_artigo=0,
        id_veterinario=usuario_logado['id'],
        id_categoria_artigo=id_categoria_artigo,
        titulo=titulo,
        conteudo=conteudo,
        foto=caminho_foto,
        data_publicacao=datetime.now(),
        visualizacoes=0
    )
    postagem_artigo_repo.salvar(novo_artigo)

    adicionar_mensagem_sucesso(request, "Artigo cadastrado com sucesso!")
    return RedirectResponse("/veterinario/listar_postagem_artigo", status_code=303)

@router.get("/excluir_postagem_artigo/{id_postagem_artigo}")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def get_excluir_postagem_artigo(request: Request, id_postagem_artigo: int):
    return templates.TemplateResponse("veterinario/excluir_postagem_artigo.html", {"request": request})