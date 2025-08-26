from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_root(request: Request):
    response = templates.TemplateResponse("administrador/home_administrador.html", {"request": request})
    return response   

@router.get("/listar_categorias")
async def pagina_categoria_artigo(request: Request):
    return templates.TemplateResponse("administrador/listar_categorias.html", {"request": request})

@router.get("/alterar_categoria/{id_categoria}")
async def pagina_categoria_artigo(request: Request, id_categoria: int):
    return templates.TemplateResponse("administrador/alterar_categoria.html", {"request": request})

@router.get("/cadastrar_categoria")
async def pagina_categoria_artigo(request: Request):
    return templates.TemplateResponse("administrador/cadastrar_categoria.html", {"request": request})

@router.get("/excluir_categoria/{id_categoria}")
async def pagina_categoria_artigo(request: Request, id_categoria: int):
    return templates.TemplateResponse("administrador/excluir_categoria.html", {"request": request})

