import logging
from fastapi import APIRouter, Query, Request, HTTPException
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

    # Buscar dados relacionados
    veterinario = veterinario_repo.obter_por_id(artigo.id_veterinario)
    categoria = categoria_artigo_repo.obter_por_id(artigo.id_categoria_artigo)

    # Contar curtidas
    total_curtidas = curtida_artigo_repo.contar_curtidas_por_artigo(id_postagem_artigo)

    # Usuário logado e se curtiu
    usuario_logado = obter_usuario_logado(request)
    usuario_curtiu = False
    if usuario_logado:
        id_usuario = usuario_logado.get("id_usuario") or usuario_logado.get("id")
        if id_usuario is not None:
            curtida = curtida_artigo_repo.obter_por_id(id_usuario, id_postagem_artigo)
            usuario_curtiu = curtida is not None

    # Incrementar visualizações (não bloquear em erro)
    try:
        postagem_artigo_repo.incrementar_visualizacoes(id_postagem_artigo)
    except Exception as e:
        logger.exception("Erro ao incrementar visualizações: %s", e)

    context = {
        "request": request,
        "artigo": artigo,
        "veterinario": veterinario,
        "categoria": categoria,
        "total_curtidas": total_curtidas,
        "usuario_curtiu": usuario_curtiu,
        "usuario_logado": usuario_logado
    }

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

    # Incrementar visualizações (silencioso em erro)
    try:
        postagem_feed_repo.incrementar_visualizacoes(id_postagem_feed)
    except Exception:
        logger.exception("Erro ao incrementar visualizações para post %s", id_postagem_feed)

    # Contar curtidas do post
    total_curtidas = curtida_feed_repo.contar_curtidas_por_postagem(id_postagem_feed)

    # Verificar se usuário logado curtiu o post
    usuario_logado = obter_usuario_logado(request)
    usuario_curtiu = False
    if usuario_logado:
        id_usuario = usuario_logado.get("id_usuario") or usuario_logado.get("id")
        if id_usuario is not None:
            curtida = curtida_feed_repo.obter_por_id(id_usuario, id_postagem_feed)
            usuario_curtiu = curtida is not None

    context = {
        "request": request,
        "post": post,
        "total_curtidas": total_curtidas,
        "usuario_curtiu": usuario_curtiu,
        "usuario_logado": usuario_logado,
    }

    return templates.TemplateResponse("publico/detalhes_post.html", context)


@router.post("/artigos/{id_artigo}/curtir")
@requer_autenticacao()
async def curtir_artigo(request: Request, id_artigo: int, usuario_logado: dict = None):
    from model.curtida_artigo_model import CurtidaArtigo
    from repo import curtida_artigo_repo
    from datetime import datetime
    from util.mensagens import adicionar_mensagem_sucesso, adicionar_mensagem_info

    # ✅ Obter id de forma consistente
    id_usuario = usuario_logado.get("id_usuario") or usuario_logado.get("id")
    
    # ✅ DEBUG: Log para verificar
    logger.info(f"Tentando curtir/descurtir artigo - Usuario: {id_usuario}, Artigo: {id_artigo}")
    
    curtida_existente = curtida_artigo_repo.obter_por_id(id_usuario, id_artigo)
    
    logger.info(f"Curtida existente: {curtida_existente}")

    if curtida_existente:
        # Descurtir
        resultado = curtida_artigo_repo.excluir(id_usuario, id_artigo)
        logger.info(f"Resultado da exclusão: {resultado}")
        adicionar_mensagem_info(request, "Curtida removida.")
    else:
        # Curtir
        try:
            curtida = CurtidaArtigo(
                id_usuario=id_usuario,
                id_postagem_artigo=id_artigo,
                data_curtida=datetime.now()
            )
            resultado = curtida_artigo_repo.inserir(curtida)
            logger.info(f"Resultado da inserção: {resultado}")
            adicionar_mensagem_sucesso(request, "Artigo curtido!")
        except Exception as e:
            logger.error(f"Erro ao curtir artigo: {e}", exc_info=True)
            adicionar_mensagem_info(request, "Erro ao curtir o artigo.")

    return RedirectResponse(f"/artigos/{id_artigo}", status_code=303)

@router.post("/petgram/{id_postagem_feed}/curtir")
@requer_autenticacao()
async def curtir_feed(request: Request, id_postagem_feed: int, usuario_logado: dict = None):
    from model.curtida_feed_model import CurtidaFeed
    from repo import curtida_feed_repo
    from datetime import datetime
    from util.mensagens import adicionar_mensagem_sucesso, adicionar_mensagem_info

    # ✅ CORRIGIDO: Obter id de forma consistente
    id_usuario = usuario_logado.get("id_usuario") or usuario_logado.get("id")
    
    # ✅ DEBUG: Log para verificar
    logger.info(f"Tentando curtir/descurtir - Usuario: {id_usuario}, Post: {id_postagem_feed}")
    
    curtida_existente = curtida_feed_repo.obter_por_id(id_usuario, id_postagem_feed)
    
    logger.info(f"Curtida existente: {curtida_existente}")

    if curtida_existente:
        # Descurtir
        resultado = curtida_feed_repo.excluir(id_usuario, id_postagem_feed)
        logger.info(f"Resultado da exclusão: {resultado}")
        adicionar_mensagem_info(request, "Curtida removida.")
    else:
        # Curtir
        try:
            curtida = CurtidaFeed(
                id_usuario=id_usuario,
                id_postagem_feed=id_postagem_feed,
                data_curtida=datetime.now()
            )
            resultado = curtida_feed_repo.inserir(curtida)
            logger.info(f"Resultado da inserção: {resultado}")
            adicionar_mensagem_sucesso(request, "Post curtido!")
        except Exception as e:
            logger.error(f"Erro ao curtir post: {e}", exc_info=True)
            adicionar_mensagem_info(request, "Erro ao curtir o post.")

    return RedirectResponse(f"/petgram/{id_postagem_feed}", status_code=303)


# @router.get("/buscar")
# async def buscar(request: Request, q: str = Query(None), tipo: str = Query("artigos")):
#     if not q or len(q.strip()) < 3:
#         return templates.TemplateResponse("publico/buscar.html", {
#             "request": request,
#             "erro": "Digite pelo menos 3 caracteres."
#         })

#     termo = q.strip()
#     resultados = []

#     if tipo == "artigos":
#         from repo import postagem_artigo_repo
#         resultados = postagem_artigo_repo.buscar_por_termo(termo)
#     elif tipo == "petgram":
#         from repo import postagem_feed_repo
#         resultados = postagem_feed_repo.buscar_por_termo(termo)

#     return templates.TemplateResponse("publico/buscar.html", {
#         "request": request,
#         "termo": termo,
#         "tipo": tipo,
#         "resultados": resultados,
#         "total": len(resultados)
#     })

@router.get("/buscar", response_class=HTMLResponse)
async def get_buscar(request: Request, q: str = None, tipo: str = "artigos"):
    """Busca em artigos ou posts do Petgram."""
    
    # Validar termo de busca
    if not q or len(q.strip()) < 3:
        return templates.TemplateResponse("publico/buscar.html", {
            "request": request,
            "termo": q or "",
            "tipo": tipo,
            "resultados": [],
            "total": 0,
            "erro": "Digite pelo menos 3 caracteres para buscar."
        })
    
    termo = q.strip()
    resultados = []
    
    try:
        # Buscar conforme o tipo selecionado
        if tipo == "artigos":
            resultados = postagem_artigo_repo.buscar_por_termo(termo, limite=50)
            # Adicionar contagem de curtidas
            for artigo in resultados:
                artigo['total_curtidas'] = curtida_artigo_repo.contar_curtidas_por_artigo(
                    artigo['id_postagem_artigo']
                )
        
        elif tipo == "petgram":
            resultados = postagem_feed_repo.buscar_por_termo(termo, limite=50)
            # Adicionar contagem de curtidas
            for post in resultados:
                post['total_curtidas'] = curtida_feed_repo.contar_curtidas_por_postagem(
                    post['id_postagem_feed']
                )
        
        return templates.TemplateResponse("publico/buscar.html", {
            "request": request,
            "termo": termo,
            "tipo": tipo,
            "resultados": resultados,
            "total": len(resultados)
        })
    
    except Exception as e:
        logger.exception(f"Erro na busca: {e}")
        return templates.TemplateResponse("publico/buscar.html", {
            "request": request,
            "termo": termo,
            "tipo": tipo,
            "resultados": [],
            "total": 0,
            "erro": "Erro ao realizar a busca. Tente novamente."
        })
