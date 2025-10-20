import logging
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse

from util.template_util import criar_templates
from util.auth_decorator import obter_usuario_logado
from repo import postagem_artigo_repo, veterinario_repo, categoria_artigo_repo, curtida_artigo_repo


logger = logging.getLogger(__name__)
router = APIRouter()
templates = criar_templates()


@router.get("/")
async def get_root(request: Request):
    # Buscar artigos recentes (6 primeiros)
    artigos_recentes = postagem_artigo_repo.obter_recentes_com_dados(6)

    # Buscar todas as categorias
    categorias = categoria_artigo_repo.obter_todos()

    context = {
        "request": request,
        "artigos_recentes": artigos_recentes,
        "categorias": categorias
    }

    response = templates.TemplateResponse("publico/index.html", context)
    return response


@router.get("/quemsomos")
async def get_sobre(request: Request):
    return templates.TemplateResponse("publico/quem_somos.html", {"request": request})


@router.get("/artigos", response_class=HTMLResponse)
async def get_artigos(request: Request, pagina: int = 1, categoria: int = None):
    """Lista todos os artigos com paginação e filtro por categoria."""
    tamanho_pagina = 12

    # Buscar artigos e contar total
    if categoria:
        artigos = postagem_artigo_repo.obter_por_categoria_com_dados(categoria, pagina, tamanho_pagina)
        categoria_selecionada = categoria_artigo_repo.obter_por_id(categoria)
        total_artigos = postagem_artigo_repo.contar_por_categoria(categoria)
    else:
        artigos = postagem_artigo_repo.obter_pagina_com_dados(pagina, tamanho_pagina)
        categoria_selecionada = None
        total_artigos = postagem_artigo_repo.contar_total()

    # Calcular total de páginas
    import math
    total_paginas = math.ceil(total_artigos / tamanho_pagina) if total_artigos > 0 else 1

    # Buscar todas as categorias
    categorias = categoria_artigo_repo.obter_todos()

    context = {
        "request": request,
        "artigos": artigos,
        "categorias": categorias,
        "categoria_selecionada": categoria_selecionada,
        "pagina": pagina,
        "total_paginas": total_paginas,
    }

    return templates.TemplateResponse("publico/artigos.html", context)


@router.get("/artigos/{id_postagem_artigo}", response_class=HTMLResponse)
async def get_detalhes_artigo(request: Request, id_postagem_artigo: int):
    # Buscar artigo
    artigo = postagem_artigo_repo.obter_por_id(id_postagem_artigo)
    if not artigo:
        raise HTTPException(status_code=404, detail="Artigo não encontrado")

    # Buscar informações do veterinário
    veterinario = veterinario_repo.obter_por_id(artigo.id_veterinario)
    if not veterinario:
        raise HTTPException(status_code=404, detail="Veterinário não encontrado")

    # Buscar informações da categoria
    categoria = categoria_artigo_repo.obter_por_id(artigo.id_categoria_artigo)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    # Contar curtidas do artigo
    total_curtidas = curtida_artigo_repo.contar_curtidas_por_artigo(id_postagem_artigo)

    # Verificar se usuário logado curtiu o artigo
    usuario_curtiu = False
    usuario = obter_usuario_logado(request)
    if usuario:
        id_usuario = usuario.get('id_usuario')
        if id_usuario and isinstance(id_usuario, int):
            curtida = curtida_artigo_repo.obter_por_id(id_usuario, id_postagem_artigo)
            usuario_curtiu = curtida is not None

    # Incrementar visualizações
    postagem_artigo_repo.incrementar_visualizacoes(id_postagem_artigo)

    # Preparar dados para o template
    context = {
        "request": request,
        "artigo": artigo,
        "veterinario": veterinario,
        "categoria": categoria,
        "total_curtidas": total_curtidas,
        "usuario_curtiu": usuario_curtiu,
    }

    return templates.TemplateResponse("publico/detalhes_artigo.html", context)
