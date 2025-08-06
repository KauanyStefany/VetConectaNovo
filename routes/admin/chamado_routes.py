from fastapi import APIRouter
from fastapi.templating import Jinja2Templates

from model.chamado_model import Chamado
from repo import chamado_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

