from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_root(request: Request):
    response = templates.TemplateResponse("veterinario/veterinario_home.html", {"request": request})
    return response   

@router.get("/listar_postagem_artigo")
async def get_listar_postagem_artigo(request: Request):
    return templates.TemplateResponse("veterinario/listar_postagem_artigo.html", {"request": request})

@router.get("/alterar_postagem_artigo/{id_postagem_artigo}")
async def get_alterar_postagem_artigo(request: Request, id_postagem_artigo: int):
    return templates.TemplateResponse("veterinario/alterar_postagem_artigo.html", {"request": request})

@router.get("/cadastrar_postagem_artigo")
async def get_cadastrar_postagem_artigo(request: Request):
    return templates.TemplateResponse("veterinario/cadastrar_postagem_artigo.html", {"request": request})

@router.get("/excluir_postagem_artigo/{id_postagem_artigo}")
async def get_excluir_postagem_artigo(request: Request, id_postagem_artigo: int):
    return templates.TemplateResponse("veterinario/excluir_postagem_artigo.html", {"request": request})