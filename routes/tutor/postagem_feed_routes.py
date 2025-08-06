from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from model.postagem_feed_model import PostagemFeed
from repo import postagem_feed_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/feed/{id_postagem_feed}")
async def get_feed_id(id_postagem_feed: int):
    postagem_feed = postagem_feed_repo.obter_por_id(id_postagem_feed)
    response = templates.TemplateResponse("tutor/feed.html", {"request": {}, "postagem_feed": postagem_feed})
    return response

@router.get("/tutor/feeds")
async def get_feeds():
    feeds = postagem_feed_repo.obter_todos_paginado()
    response = templates.TemplateResponse("tutor/listar_feeds.html", {"request": {}, "feeds": feeds})
    return response

@router.get("/tutor/feed/postar")
async def get_feed_postar():
    response = templates.TemplateResponse("tutor/postar_feed.html", {"request": {}})
    return response

@router.get("/tutor/feed/excluir/{id_postagem_feed}")
async def get_excluir_feed(id_postagem_feed: int):
    if postagem_feed_repo.excluir(id_postagem_feed):
        return RedirectResponse("/tutor/feeds", status_code=303)

