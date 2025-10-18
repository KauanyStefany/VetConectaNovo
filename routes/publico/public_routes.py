from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_root(request: Request):
    response = templates.TemplateResponse("publico/index.html", {"request": request})
    return response


@router.get("/veterinario/detalhes/{id_veterinario}")
async def get_veterinario(request: Request, id_veterinario: int):
    return templates.TemplateResponse("publico/veterinario.html", {"request": request})


@router.get("/tutor/detalhes/{id_tutor}")
async def get_tutor(request: Request, id_tutor: int):
    return templates.TemplateResponse("publico/tutor.html", {"request": request})


@router.get("/quemsomos")
async def get_sobre(request: Request):
    return templates.TemplateResponse("publico/quemsomos.html", {"request": request})


@router.get("/posts")
async def get_posts(request: Request):
    return templates.TemplateResponse("publico/posts.html", {"request": request})


@router.get("/artigos")
async def get_artigos(request: Request):
    return templates.TemplateResponse("publico/artigos.html", {"request": request})
