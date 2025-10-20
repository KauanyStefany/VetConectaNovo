from typing import List, Optional, Union
from datetime import datetime, date
from jinja2 import FileSystemLoader
from fastapi.templating import Jinja2Templates
from fastapi import Request


def criar_templates(diretorio_especifico: Optional[Union[str, List[str]]] = None) -> Jinja2Templates:
    """
    Cria um objeto Jinja2Templates configurado com múltiplos diretórios.
    
    O diretório raiz "templates" é sempre incluído automaticamente para garantir
    acesso aos templates base como base.html.
    
    Args:
        diretorio_especifico: Diretório(s) específico(s) além do raiz.
                             Pode ser uma string única ou lista de strings.
                             Exemplo: "templates/admin/categorias" ou
                                     ["templates/admin", "templates/public"]
    
    Returns:
        Objeto Jinja2Templates configurado com os diretórios especificados
    
    Exemplo de uso:
        # Para um diretório específico
        templates = criar_templates("templates/admin/categorias")
        
        # Para múltiplos diretórios
        templates = criar_templates(["templates/admin", "templates/admin/produtos"])
        
        # Apenas com o diretório raiz
        templates = criar_templates()
    """
    # Sempre incluir o diretório raiz onde estão os templates base
    diretorios = ["templates"]
    
    # Adicionar diretórios específicos se fornecidos
    if diretorio_especifico:
        if isinstance(diretorio_especifico, str):
            # Se for uma string única, adiciona à lista
            diretorios.append(diretorio_especifico)
        elif isinstance(diretorio_especifico, list):
            # Se for uma lista, estende a lista de diretórios
            diretorios.extend(diretorio_especifico)
    
    # Criar o objeto Jinja2Templates com diretório base como "."
    # Isso é necessário para que o FileSystemLoader funcione corretamente
    templates = Jinja2Templates(directory=".")
    
    # Configurar o loader com múltiplos diretórios
    # O FileSystemLoader tentará encontrar templates em ordem nos diretórios listados
    templates.env.loader = FileSystemLoader(diretorios)

    # Adicionar funções globais ao ambiente Jinja2
    _adicionar_funcoes_globais(templates)

    return templates


def _adicionar_funcoes_globais(templates: Jinja2Templates) -> None:
    """
    Adiciona funções globais e filtros ao ambiente Jinja2
    """
    from util.mensagens import obter_mensagens

    # Adicionar obter_mensagens como função global
    templates.env.globals['obter_mensagens'] = obter_mensagens

    # Adicionar filtros de formatação de data/hora pt-BR
    templates.env.filters['data_br'] = formatar_data_br
    templates.env.filters['hora_br'] = formatar_hora_br
    templates.env.filters['data_hora_br'] = formatar_data_hora_br


def formatar_data_br(valor) -> str:
    """
    Formata uma data para o formato brasileiro (dd/mm/yyyy).

    Args:
        valor: Pode ser datetime, date, ou string no formato ISO (YYYY-MM-DD)

    Returns:
        String formatada no padrão dd/mm/yyyy
    """
    if valor is None:
        return ""

    if isinstance(valor, str):
        valor = valor.strip()
        # Se for string, tenta converter
        try:
            # Tenta formato ISO completo (YYYY-MM-DD HH:MM:SS)
            if len(valor) > 10:
                valor = datetime.strptime(valor[:19], "%Y-%m-%d %H:%M:%S")
            else:
                # Formato apenas data (YYYY-MM-DD)
                valor = datetime.strptime(valor[:10], "%Y-%m-%d")
        except (ValueError, TypeError):
            return str(valor)

    if isinstance(valor, datetime):
        return valor.strftime("%d/%m/%Y")
    elif isinstance(valor, date):
        return valor.strftime("%d/%m/%Y")

    return str(valor)


def formatar_hora_br(valor) -> str:
    """
    Formata uma hora para o formato brasileiro (HH:MM).

    Args:
        valor: Pode ser datetime ou string no formato ISO

    Returns:
        String formatada no padrão HH:MM
    """
    if valor is None:
        return ""

    if isinstance(valor, str):
        valor = valor.strip()
        try:
            # Tenta formato completo primeiro
            if len(valor) > 10:
                valor = datetime.strptime(valor[:19], "%Y-%m-%d %H:%M:%S")
            else:
                # Se for apenas data, retorna 00:00
                valor = datetime.strptime(valor[:10], "%Y-%m-%d")
        except (ValueError, TypeError):
            return str(valor)

    if isinstance(valor, datetime):
        return valor.strftime("%H:%M")

    return str(valor)


def formatar_data_hora_br(valor) -> str:
    """
    Formata uma data e hora para o formato brasileiro (dd/mm/yyyy HH:MM).

    Args:
        valor: Pode ser datetime ou string no formato ISO

    Returns:
        String formatada no padrão dd/mm/yyyy HH:MM
    """
    if valor is None:
        return ""

    if isinstance(valor, str):
        valor = valor.strip()
        try:
            # Tenta formato completo primeiro
            if len(valor) > 10:
                valor = datetime.strptime(valor[:19], "%Y-%m-%d %H:%M:%S")
            else:
                # Se for apenas data, assume 00:00:00
                valor = datetime.strptime(valor[:10], "%Y-%m-%d")
        except (ValueError, TypeError):
            return str(valor)

    if isinstance(valor, datetime):
        return valor.strftime("%d/%m/%Y %H:%M")

    return str(valor)