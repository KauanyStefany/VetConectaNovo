from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/alterar_dados")
async def get_alterar_dados(request: Request):
    response = templates.TemplateResponse("usuario/alterar_dados.html", {"request": request})
    return response

@router.get("/alterar_senha")
async def get_alterar_senha(request: Request):
    response = templates.TemplateResponse("usuario/alterar_senha.html", {"request": request})
    return response

@router.get("/solicitar_chamado")
async def get_solicitar_chamado(request: Request):
    response = templates.TemplateResponse("usuario/solicitar_chamado.html", {"request": request})
    return response

@router.get("/solicitacoes_chamado")
async def get_solicitacoes_chamado(request: Request):
    response = templates.TemplateResponse("usuario/solicitacoes_chamado.html", {"request": request})
    return response

@router.get("/denunciar")
async def get_denunciar(request: Request):
    response = templates.TemplateResponse("usuario/denunciar.html", {"request": request})
    return response

@router.get("/comentar")
async def get_comentar(request: Request):
    response = templates.TemplateResponse("usuario/comentar.html", {"request": request})
    return response

@router.get("/excluir_comentario/{id_comentario}")
async def get_excluir_comentario(request: Request, id_comentario: int):
    return templates.TemplateResponse("usuario/excluir_comentario.html", {"request": request})


@router.get("/comentarios")
async def get_comentarios(request: Request):
    response = templates.TemplateResponse("usuario/comentarios.html", {"request": request})
    return response

@router.get("/curtidas")
async def get_curtidas(request: Request):
    response = templates.TemplateResponse("usuario/curtidas.html", {"request": request})
    return response
