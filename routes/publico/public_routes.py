import logging
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse

from util.template_util import criar_templates
from util.auth_decorator import obter_usuario_logado, requer_autenticacao
from repo import postagem_artigo_repo, veterinario_repo, categoria_artigo_repo, curtida_artigo_repo, postagem_feed_repo, curtida_feed_repo


logger = logging.getLogger(__name__)
router = APIRouter()
templates = criar_templates()


@router.get("/")
async def get_root(request: Request):
    # Buscar artigos recentes (6 primeiros)
    artigos_recentes = postagem_artigo_repo.obter_recentes_com_dados(6)

    # Adicionar contagem de curtidas para cada artigo
    for artigo in artigos_recentes:
        artigo['total_curtidas'] = curtida_artigo_repo.contar_curtidas_por_artigo(artigo['id_postagem_artigo'])

    # Buscar todas as categorias
    categorias = categoria_artigo_repo.obter_todos()

    # Buscar posts do Petgram recentes (6 primeiros)
    posts_recentes = postagem_feed_repo.obter_recentes_com_dados(6)

    # Adicionar contagem de curtidas para cada post
    for post in posts_recentes:
        post['total_curtidas'] = curtida_feed_repo.contar_curtidas_por_postagem(post['id_postagem_feed'])

    context = {
        "request": request,
        "artigos_recentes": artigos_recentes,
        "categorias": categorias,
        "posts_recentes": posts_recentes
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

    # Adicionar contagem de curtidas para cada artigo
    for artigo in artigos:
        artigo['total_curtidas'] = curtida_artigo_repo.contar_curtidas_por_artigo(artigo['id_postagem_artigo'])

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
        "usuario_curtiu": usuario_curtiu
    }
    # Verificar se usuário curtiu
    usuario_curtiu = False
    if usuario:
        from repo import curtida_artigo_repo
        curtida = curtida_artigo_repo.obter_por_id(usuario['id'], id_postagem_artigo)
        usuario_curtiu = curtida is not None

    # Adicionar ao context:
    return templates.TemplateResponse("publico/detalhes_artigo.html", {
        "request": request,
        "artigo": artigo,
        "total_curtidas": total_curtidas,
        "usuario_curtiu": usuario_curtiu,  # ADICIONAR ESTA LINHA
        "usuario_logado": usuario
    })
    return templates.TemplateResponse("publico/detalhes_artigo.html", context)


@router.get("/petgram", response_class=HTMLResponse)
async def get_petgram(request: Request, pagina: int = 1):
    """Lista todos os posts do Petgram com paginação."""
    tamanho_pagina = 16

    # Buscar posts e contar total
    posts = postagem_feed_repo.obter_pagina_com_dados(pagina, tamanho_pagina)
    total_posts = postagem_feed_repo.contar_total()

    # Adicionar contagem de curtidas para cada post
    for post in posts:
        post['total_curtidas'] = curtida_feed_repo.contar_curtidas_por_postagem(post['id_postagem_feed'])

    # Calcular total de páginas
    import math
    total_paginas = math.ceil(total_posts / tamanho_pagina) if total_posts > 0 else 1

    context = {
        "request": request,
        "posts": posts,
        "pagina": pagina,
        "total_paginas": total_paginas,
    }

    return templates.TemplateResponse("publico/petgram.html", context)


@router.get("/petgram/{id_postagem_feed}", response_class=HTMLResponse)
async def get_detalhes_post(request: Request, id_postagem_feed: int):
    """Exibe detalhes de um post do Petgram."""
    # Buscar post com dados completos
    post = postagem_feed_repo.obter_por_id_com_dados(id_postagem_feed)
    if not post:
        raise HTTPException(status_code=404, detail="Post não encontrado")

    # Incrementar visualizações
    postagem_feed_repo.incrementar_visualizacoes(id_postagem_feed)

    # Contar curtidas do post
    total_curtidas = curtida_feed_repo.contar_curtidas_por_postagem(id_postagem_feed)

    # Verificar se usuário logado curtiu o post
    usuario_curtiu = False
    usuario = obter_usuario_logado(request)
    if usuario:
        id_usuario = usuario.get('id')
        if id_usuario and isinstance(id_usuario, int):
            curtida = curtida_feed_repo.obter_por_id(id_usuario, id_postagem_feed)
            usuario_curtiu = curtida is not None

    context = {
        "request": request,
        "post": post,
        "total_curtidas": total_curtidas,
        "usuario_curtiu": usuario_curtiu,
    }

    return templates.TemplateResponse("publico/detalhes_post.html", context)

@router.post("/petgram/{id_post}/curtir")
@requer_autenticacao()
async def curtir_feed(request: Request, id_postagem_feed: int, usuario_logado: dict = None):
    from model.curtida_feed_model import CurtidaFeed
    from repo import curtida_feed_repo
    from datetime import datetime
    from util.mensagens import adicionar_mensagem_sucesso, adicionar_mensagem_info

    curtida_existente = curtida_feed_repo.obter_por_id(usuario_logado['id'], id_postagem_feed)

    if curtida_existente:
        # Descurtir
        curtida_feed_repo.excluir(usuario_logado['id'], id_postagem_feed)
        adicionar_mensagem_info(request, "Curtida removida.")
    else:
        # Curtir
        curtida = CurtidaFeed(
            id_usuario=usuario_logado['id'],
            id_postagem_feed=id_postagem_feed,
            data_curtida=datetime.now()
        )
        curtida_feed_repo.inserir(curtida)
        adicionar_mensagem_sucesso(request, "Post curtido!")

    return RedirectResponse(f"/petgram/{id_postagem_feed}", status_code=303)


@router.post("/artigos/{id_artigo}/curtir")
@requer_autenticacao()
async def curtir_artigo(request: Request, id_artigo: int, usuario_logado: dict = None):
    from model.curtida_artigo_model import CurtidaArtigo
    from repo import curtida_artigo_repo
    from datetime import datetime
    from util.mensagens import adicionar_mensagem_sucesso, adicionar_mensagem_info

    curtida_existente = curtida_artigo_repo.obter_por_id(usuario_logado['id'], id_artigo)

    if curtida_existente:
        # Descurtir
        curtida_artigo_repo.excluir(usuario_logado['id'], id_artigo)
        adicionar_mensagem_info(request, "Curtida removida.")
    else:
        # Curtir
        curtida = CurtidaArtigo(
            id_usuario=usuario_logado['id'],
            id_postagem_artigo=id_artigo,
            data_curtida=datetime.now()
        )
        curtida_artigo_repo.inserir(curtida)
        adicionar_mensagem_sucesso(request, "Artigo curtido!")

    return RedirectResponse(f"/artigos/{id_artigo}", status_code=303)