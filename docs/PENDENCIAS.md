# RELATÓRIO DE PENDÊNCIAS - VetConecta

**Projeto**: VetConecta - Plataforma de Conexão Veterinária

**Stack**: FastAPI + SQLite + Jinja2 + Bootstrap 5

**Data**: 2025

**Objetivo**: Guia completo para conclusão do projeto

---

## 📋 ÍNDICE

1. [Visão Geral](#1-visão-geral)
2. [Correções de Bugs Prioritárias](#2-correções-de-bugs-prioritárias)
3. [Templates Faltantes](#3-templates-faltantes)
4. [Área do Administrador](#4-área-do-administrador)
5. [Área do Tutor](#5-área-do-tutor)
6. [Área do Veterinário](#6-área-do-veterinário)
7. [Funcionalidades Gerais de Usuário](#7-funcionalidades-gerais-de-usuário)
8. [Funcionalidades Públicas Pendentes](#8-funcionalidades-públicas-pendentes)
9. [Melhorias no Banco de Dados](#9-melhorias-no-banco-de-dados)
10. [Checklist Final](#10-checklist-final)

---

## 1. VISÃO GERAL

### 1.1 Status Atual do Projeto

**Funcionalidades Implementadas (26% concluído):**
- ✅ Rotas públicas (home, artigos, petgram, detalhes)
- ✅ Sistema de autenticação e registro
- ✅ Recuperação de senha (sem envio de email)
- ✅ Perfil de usuário (alterar dados, senha, foto)
- ✅ Sistema de paginação
- ✅ Sistema de toasts/notificações
- ✅ View tracking (contagem de visualizações)
- ✅ Database completo com 16 entidades
- ✅ Repositórios com CRUD básico

**Funcionalidades Pendentes (74% a implementar):**
- ❌ Área administrativa completa
- ❌ Área do tutor (gerenciar posts Petgram)
- ❌ Área do veterinário (gerenciar artigos)
- ❌ Sistema de curtidas (backend)
- ❌ Sistema de comentários (backend)
- ❌ Sistema de chamados
- ❌ Sistema de denúncias
- ❌ Verificação de CRMV
- ❌ Sistema de busca
- ❌ Dashboard de estatísticas

### 1.2 Arquitetura do Projeto

```
VetConecta/
├── model/          # Dataclasses (16 modelos completos)
├── repo/           # Repositórios (16 repositórios com CRUD básico)
├── sql/            # Queries SQL (16 arquivos)
├── dtos/           # DTOs Pydantic (11 DTOs existentes)
├── routes/         # Rotas FastAPI
│   ├── publico/    # 4 arquivos (2 completos, 2 com templates faltantes)
│   ├── admin/      # 5 arquivos (1 parcial, 4 stubs)
│   ├── tutor/      # 1 arquivo (stub)
│   ├── veterinario/# 3 arquivos (stubs)
│   └── usuario/    # 1 arquivo (stub, sem auth)
├── templates/      # Templates Jinja2
│   ├── publico/    # 11 templates (3 faltantes)
│   └── componentes/# 7 componentes reutilizáveis
├── util/           # Utilitários (completos)
├── config/         # Configurações (completas)
└── static/         # CSS, JS, imagens (completos)
```

### 1.3 Padrões do Projeto

**Padrão de Rotas:**
```python
from fastapi import APIRouter, Request, Form
from util.auth_decorator import requer_autenticacao
from util.template_util import criar_templates
from util.mensagens import adicionar_mensagem_sucesso, adicionar_mensagem_erro
from util.error_handlers import tratar_erro_rota

router = APIRouter(prefix="/prefixo")
templates = criar_templates("templates/diretorio")

@router.get("/rota")
@requer_autenticacao(perfis_autorizados=['perfil'])
async def funcao(request: Request, usuario_logado: dict = None):
    # Lógica aqui
    return templates.TemplateResponse("template.html", {"request": request})
```

**Padrão de DTO:**
```python
from pydantic import BaseModel, field_validator

class MeuDTO(BaseModel):
    campo: str

    @field_validator('campo')
    @classmethod
    def validate_campo(cls, v):
        if not v or not v.strip():
            raise ValueError('Campo é obrigatório')
        return v.strip()
```

**Padrão de Template:**
```html
{% extends "base_publica.html" %}
{% block conteudo %}
<div class="container my-5">
    <!-- Conteúdo aqui -->
</div>
{% endblock %}
```

---

## 2. CORREÇÕES DE BUGS PRIORITÁRIAS

### 🐛 BUG #1: Redirect incorreto após criar categoria

**Arquivo:** `routes/admin/categoria_artigo_routes.py`
**Linha:** 62
**Problema:** Após criar uma categoria, o redirect aponta para um arquivo HTML em vez de uma rota.

**Código atual (errado):**
```python
response = RedirectResponse("/administrador/cadastrar_categoria.html", status_code=303)
```

**Correção:**
```python
response = RedirectResponse("/administrador/listar_categorias", status_code=303)
# OU adicionar mensagem de sucesso:
from util.mensagens import adicionar_mensagem_sucesso
adicionar_mensagem_sucesso(request, "Categoria cadastrada com sucesso!")
response = RedirectResponse("/administrador/listar_categorias", status_code=303)
```

---

### 🐛 BUG #2: Exclusão de categoria não funciona

**Arquivo:** `routes/admin/categoria_artigo_routes.py`
**Linha:** 77-85
**Problema:** O endpoint POST de exclusão apenas verifica se a categoria existe, mas não a exclui.

**Código atual (errado):**
```python
@router.post("/excluir_categoria")
async def post_categoria_excluir(request: Request, id_categoria: int = Form(...)):
    if categoria_artigo_repo.obter_por_id(id_categoria):
        response = RedirectResponse("/administrador/categorias", status_code=303)
        return response
```

**Correção:**
```python
@router.post("/excluir_categoria")
@requer_autenticacao(perfis_autorizados=["admin"])
async def post_categoria_excluir(request: Request, id_categoria: int = Form(...)):
    from util.mensagens import adicionar_mensagem_sucesso, adicionar_mensagem_erro

    categoria = categoria_artigo_repo.obter_por_id(id_categoria)
    if not categoria:
        adicionar_mensagem_erro(request, "Categoria não encontrada.")
        return RedirectResponse("/administrador/listar_categorias", status_code=303)

    # Tentar excluir
    if categoria_artigo_repo.excluir(id_categoria):
        adicionar_mensagem_sucesso(request, "Categoria excluída com sucesso!")
    else:
        adicionar_mensagem_erro(request, "Erro ao excluir categoria. Pode haver artigos vinculados.")

    return RedirectResponse("/administrador/listar_categorias", status_code=303)
```

---

### 🐛 BUG #3: Objeto request vazio na home do admin

**Arquivo:** `routes/admin/categoria_artigo_routes.py`
**Linha:** 17
**Problema:** O objeto `request` está sendo substituído por um dicionário vazio `{}`.

**Código atual (errado):**
```python
response = templates.TemplateResponse("administrador/home_administrador.html",
    {"request": {}, "categoria_artigo": categoria_artigo})
```

**Correção:**
```python
response = templates.TemplateResponse("administrador/home_administrador.html",
    {"request": request, "categoria_artigo": categoria_artigo})
```

---

## 3. TEMPLATES FALTANTES

### 3.1 Templates Públicos (Perfil)

Os templates de perfil são referenciados nas rotas mas não existem fisicamente.

#### 📄 Template: `templates/publico/perfil.html`

**Localização:** `/Volumes/Externo/Ifes/VetConectaNovo/templates/publico/perfil.html`

**Descrição:** Página de visualização do perfil do usuário logado.

**Estrutura necessária:**
```html
{% extends "base_publica.html" %}
{% block titulo %}Meu Perfil{% endblock %}
{% block conteudo %}
<div class="container my-5">
    <div class="row">
        <div class="col-md-4">
            <!-- Avatar do usuário -->
            <img src="/static/img/usuarios/{{ '%08d' % usuario.id_usuario }}.jpg"
                 class="avatar-xl mb-3"
                 onerror="this.src='/static/img/default-avatar.jpg'">

            <!-- Botão alterar foto -->
            <form method="post" action="/perfil/alterar-foto" enctype="multipart/form-data">
                <input type="file" name="foto" accept="image/*">
                <button type="submit" class="btn btn-roxo">Alterar Foto</button>
            </form>
        </div>
        <div class="col-md-8">
            <!-- Informações do usuário -->
            <h2>{{ usuario.nome }}</h2>
            <p><strong>Email:</strong> {{ usuario.email }}</p>
            <p><strong>Perfil:</strong> {{ usuario.perfil|capitalize }}</p>

            {% if usuario.perfil == 'tutor' %}
                <p><strong>Quantidade de Pets:</strong> {{ usuario.quantidade_pets }}</p>
            {% elif usuario.perfil == 'veterinario' %}
                <p><strong>CRMV:</strong> {{ usuario.crmv }}</p>
                <p><strong>Verificado:</strong> {{ 'Sim' if usuario.verificado else 'Não' }}</p>
            {% endif %}

            <!-- Links de ação -->
            <a href="/perfil/alterar" class="btn btn-outline-roxo">Editar Dados</a>
            <a href="/perfil/alterar-senha" class="btn btn-outline-laranja">Alterar Senha</a>
        </div>
    </div>
</div>
{% endblock %}
```

**Variáveis recebidas do backend:**
- `usuario`: Objeto Tutor ou Veterinario (com todos os campos de Usuario)

---

#### 📄 Template: `templates/publico/dados.html`

**Localização:** `/Volumes/Externo/Ifes/VetConectaNovo/templates/publico/dados.html`

**Descrição:** Formulário de edição de dados pessoais.

**Estrutura necessária:**
```html
{% extends "base_publica.html" %}
{% block titulo %}Editar Dados{% endblock %}
{% block conteudo %}
<div class="container my-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <h2 class="mb-4">Editar Dados Pessoais</h2>

            {% if erro %}
            <div class="alert alert-danger">{{ erro }}</div>
            {% endif %}

            <form method="post" action="/perfil/alterar">
                <div class="mb-3">
                    <label class="form-label">Nome</label>
                    <input type="text" name="nome" class="form-control"
                           value="{{ usuario.nome }}" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Email</label>
                    <input type="email" name="email" class="form-control"
                           value="{{ usuario.email }}" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Telefone</label>
                    <input type="text" name="telefone" class="form-control"
                           value="{{ usuario.telefone or '' }}">
                </div>

                <button type="submit" class="btn btn-roxo">Salvar Alterações</button>
                <a href="/perfil" class="btn btn-outline-secondary">Cancelar</a>
            </form>
        </div>
    </div>
</div>
{% endblock %}
```

**Variáveis recebidas:**
- `usuario`: Objeto Usuario
- `dados_perfil`: Objeto Tutor/Veterinario/Administrador (opcional)
- `erro`: Mensagem de erro (opcional)

---

#### 📄 Template: `templates/publico/alterar_senha.html`

**Localização:** `/Volumes/Externo/Ifes/VetConectaNovo/templates/publico/alterar_senha.html`

**Descrição:** Formulário de alteração de senha.

**Estrutura necessária:**
```html
{% extends "base_publica.html" %}
{% block titulo %}Alterar Senha{% endblock %}
{% block conteudo %}
<div class="container my-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <h2 class="mb-4">Alterar Senha</h2>

            {% if erro %}
            <div class="alert alert-danger">{{ erro }}</div>
            {% endif %}

            {% if sucesso %}
            <div class="alert alert-success">{{ sucesso }}</div>
            {% endif %}

            <form method="post" action="/perfil/alterar-senha">
                <div class="mb-3">
                    <label class="form-label">Senha Atual</label>
                    <input type="password" name="senha_atual" class="form-control" required>
                </div>

                <div class="mb-3">
                    <label class="form-label">Nova Senha</label>
                    <input type="password" name="senha_nova" class="form-control" required>
                    <small class="form-text text-muted">Mínimo 6 caracteres</small>
                </div>

                <div class="mb-3">
                    <label class="form-label">Confirmar Nova Senha</label>
                    <input type="password" name="confirmar_senha" class="form-control" required>
                </div>

                <button type="submit" class="btn btn-roxo">Alterar Senha</button>
                <a href="/perfil" class="btn btn-outline-secondary">Cancelar</a>
            </form>
        </div>
    </div>
</div>
{% endblock %}
```

**Variáveis recebidas:**
- `erro`: Mensagem de erro (opcional)
- `sucesso`: Mensagem de sucesso (opcional)

---

## 4. ÁREA DO ADMINISTRADOR

### 4.1 Funcionalidade: Gerenciar Categorias de Artigos

**Status:** ⚠️ 70% implementado (com bugs)

**Pendências:**
- ✅ Rota GET/POST implementada (com bugs a corrigir)
- ❌ Templates faltando
- ❌ Registro em main.py

#### Arquivos a corrigir:

**1. Rota:** `routes/admin/categoria_artigo_routes.py`
- Corrigir os 3 bugs descritos na seção 2

**2. Registro em main.py:**
```python
# Adicionar após linha 62:
from routes.admin import categoria_artigo_routes

# Adicionar após linha 62:
app.include_router(
    categoria_artigo_routes.router,
    prefix="/administrador",
    tags=["admin-categorias"]
)
```

#### Templates a criar:

**📄 `templates/admin/home_administrador.html`**

**Descrição:** Dashboard do administrador com resumo de atividades.

**Estrutura:**
```html
{% extends "base_publica.html" %}
{% block conteudo %}
<div class="container my-5">
    <h1 class="mb-4">Painel Administrativo</h1>

    <div class="row">
        <div class="col-md-3">
            <div class="card">
                <div class="card-body text-center">
                    <i class="bi bi-folder icon-lg text-roxo"></i>
                    <h5 class="mt-3">Categorias</h5>
                    <p class="display-6">{{ categoria_artigo|length }}</p>
                    <a href="/administrador/listar_categorias" class="btn btn-sm btn-outline-roxo">
                        Gerenciar
                    </a>
                </div>
            </div>
        </div>

        <!-- Cards similares para: Chamados, Denúncias, Verificações CRMV -->
    </div>
</div>
{% endblock %}
```

**Variáveis:** `categoria_artigo` (lista de categorias)

---

**📄 `templates/admin/listar_categorias.html`**

**Descrição:** Lista todas as categorias com ações.

**Estrutura:**
```html
{% extends "base_publica.html" %}
{% block conteudo %}
<div class="container my-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2>Categorias de Artigos</h2>
        <a href="/administrador/cadastrar_categoria" class="btn btn-roxo">
            <i class="bi bi-plus-circle"></i> Nova Categoria
        </a>
    </div>

    <div class="table-responsive">
        <table class="table table-hover">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nome</th>
                    <th>Cor</th>
                    <th>Ações</th>
                </tr>
            </thead>
            <tbody>
                {% for categoria in categorias %}
                <tr>
                    <td>{{ categoria.id_categoria_artigo }}</td>
                    <td>
                        <span class="badge" style="background-color: {{ categoria.cor }}">
                            {{ categoria.nome }}
                        </span>
                    </td>
                    <td>{{ categoria.cor }}</td>
                    <td>
                        <a href="/administrador/alterar_categoria/{{ categoria.id_categoria_artigo }}"
                           class="btn btn-sm btn-outline-roxo">
                            Editar
                        </a>
                        <a href="/administrador/excluir_categoria/{{ categoria.id_categoria_artigo }}"
                           class="btn btn-sm btn-outline-danger">
                            Excluir
                        </a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
```

**Implementação da rota GET:**
```python
@router.get("/listar_categorias")
@requer_autenticacao(perfis_autorizados=["admin"])
async def get_listar_categorias(request: Request):
    categorias = categoria_artigo_repo.obter_todos()
    return templates.TemplateResponse("admin/listar_categorias.html", {
        "request": request,
        "categorias": categorias
    })
```

---

**📄 `templates/admin/cadastrar_categoria.html`**

**Descrição:** Formulário para criar nova categoria.

**Estrutura:**
```html
{% extends "base_publica.html" %}
{% block conteudo %}
<div class="container my-5">
    <h2 class="mb-4">Nova Categoria</h2>

    {% if mensagem %}
    <div class="alert alert-danger">{{ mensagem }}</div>
    {% endif %}

    <form method="post" action="/administrador/cadastrar_categoria">
        <div class="mb-3">
            <label class="form-label">Nome</label>
            <input type="text" name="nome" class="form-control" required>
        </div>

        <div class="mb-3">
            <label class="form-label">Cor (hexadecimal)</label>
            <input type="color" name="cor" class="form-control" required>
        </div>

        <div class="mb-3">
            <label class="form-label">Imagem (nome do arquivo)</label>
            <input type="text" name="imagem" class="form-control"
                   placeholder="Ex: 01.jpg" required>
            <small class="form-text">Arquivo deve estar em static/img/categorias/</small>
        </div>

        <button type="submit" class="btn btn-roxo">Cadastrar</button>
        <a href="/administrador/listar_categorias" class="btn btn-outline-secondary">
            Cancelar
        </a>
    </form>
</div>
{% endblock %}
```

**Nota:** O POST já está implementado, apenas corrigir o redirect (BUG #1).

---

**📄 `templates/admin/alterar_categoria.html`**

**Descrição:** Formulário para editar categoria existente.

**Estrutura:** Similar ao cadastrar_categoria.html, mas com campos preenchidos:
```html
<input type="hidden" name="id_categoria" value="{{ categoria_artigo.id_categoria_artigo }}">
<input type="text" name="nome" value="{{ categoria_artigo.nome }}" required>
<input type="color" name="cor" value="{{ categoria_artigo.cor }}" required>
<input type="text" name="imagem" value="{{ categoria_artigo.imagem }}" required>
```

**Nota:** O GET e POST já estão implementados.

---

**📄 `templates/admin/excluir_categoria.html`**

**Descrição:** Confirmação de exclusão de categoria.

**Estrutura:**
```html
{% extends "base_publica.html" %}
{% block conteudo %}
<div class="container my-5">
    <h2 class="mb-4 text-danger">Excluir Categoria</h2>

    <div class="alert alert-warning">
        <strong>Atenção!</strong> Esta ação não pode ser desfeita.
    </div>

    <div class="card">
        <div class="card-body">
            <h5>Categoria a ser excluída:</h5>
            <p><strong>Nome:</strong> {{ categoria_artigo.nome }}</p>
            <p><strong>Cor:</strong>
                <span class="badge" style="background-color: {{ categoria_artigo.cor }}">
                    {{ categoria_artigo.cor }}
                </span>
            </p>
        </div>
    </div>

    <form method="post" action="/administrador/excluir_categoria" class="mt-3">
        <input type="hidden" name="id_categoria" value="{{ categoria_artigo.id_categoria_artigo }}">
        <button type="submit" class="btn btn-danger">Confirmar Exclusão</button>
        <a href="/administrador/listar_categorias" class="btn btn-outline-secondary">
            Cancelar
        </a>
    </form>
</div>
{% endblock %}
```

**Nota:** O GET está implementado, mas o POST precisa ser corrigido (BUG #2).

---

### 4.2 Funcionalidade: Gerenciar Chamados (Suporte)

**Status:** ❌ 0% implementado (apenas stubs)

**Descrição:** Administradores podem visualizar, responder e fechar chamados de usuários.

#### Arquivos a implementar:

**1. Rota:** `routes/admin/chamado_routes.py`

**Estrutura atual:** Apenas stubs GET que retornam templates

**Implementação necessária:**

```python
from fastapi import APIRouter, Request, Form
from util.auth_decorator import requer_autenticacao
from util.template_util import criar_templates
from util.mensagens import adicionar_mensagem_sucesso, adicionar_mensagem_erro
from repo import chamado_repo, resposta_chamado_repo
from model.resposta_chamado_model import RespostaChamado
from datetime import datetime

router = APIRouter(prefix="/administrador")
templates = criar_templates("templates/admin")

@router.get("/listar_chamados")
@requer_autenticacao(perfis_autorizados=["admin"])
async def get_listar_chamados(request: Request, usuario_logado: dict = None):
    """Lista todos os chamados com paginação"""
    chamados = chamado_repo.obter_pagina(limite=20, offset=0)
    total = chamado_repo.contar_total()  # Precisa criar esta função

    return templates.TemplateResponse("admin/listar_chamados.html", {
        "request": request,
        "chamados": chamados,
        "total": total
    })

@router.get("/responder_chamado/{id_chamado}")
@requer_autenticacao(perfis_autorizados=["admin"])
async def get_responder_chamado(request: Request, id_chamado: int, usuario_logado: dict = None):
    """Exibe formulário para responder chamado"""
    chamado = chamado_repo.obter_por_id(id_chamado)
    if not chamado:
        adicionar_mensagem_erro(request, "Chamado não encontrado.")
        return RedirectResponse("/administrador/listar_chamados", status_code=303)

    # Buscar respostas anteriores
    respostas = resposta_chamado_repo.obter_por_chamado(id_chamado)  # Criar função

    return templates.TemplateResponse("admin/responder_chamado.html", {
        "request": request,
        "chamado": chamado,
        "respostas": respostas
    })

@router.post("/responder_chamado")
@requer_autenticacao(perfis_autorizados=["admin"])
async def post_responder_chamado(
    request: Request,
    id_chamado: int = Form(...),
    titulo: str = Form(...),
    descricao: str = Form(...),
    usuario_logado: dict = None
):
    """Salva resposta do administrador"""
    from dtos.resposta_chamado_dto import RespostaChamadoDTO

    # Validar com DTO
    try:
        dto = RespostaChamadoDTO(titulo=titulo, descricao=descricao)
    except Exception as e:
        adicionar_mensagem_erro(request, str(e))
        return RedirectResponse(f"/administrador/responder_chamado/{id_chamado}", status_code=303)

    # Criar resposta
    resposta = RespostaChamado(
        id_resposta_chamado=0,
        id_chamado=id_chamado,
        titulo=dto.titulo,
        descricao=dto.descricao,
        data=datetime.now()
    )

    if resposta_chamado_repo.inserir(resposta):
        # Atualizar status do chamado para "em_andamento"
        chamado_repo.atualizar_status(id_chamado, "em_andamento")
        adicionar_mensagem_sucesso(request, "Resposta enviada com sucesso!")
    else:
        adicionar_mensagem_erro(request, "Erro ao enviar resposta.")

    return RedirectResponse("/administrador/listar_chamados", status_code=303)

@router.post("/fechar_chamado")
@requer_autenticacao(perfis_autorizados=["admin"])
async def post_fechar_chamado(
    request: Request,
    id_chamado: int = Form(...),
    usuario_logado: dict = None
):
    """Marca chamado como resolvido"""
    if chamado_repo.atualizar_status(id_chamado, "resolvido"):
        adicionar_mensagem_sucesso(request, "Chamado marcado como resolvido!")
    else:
        adicionar_mensagem_erro(request, "Erro ao fechar chamado.")

    return RedirectResponse("/administrador/listar_chamados", status_code=303)
```

**2. DTO:** Já existe `dtos/resposta_chamado_dto.py` ✅

**3. Repositório:** Adicionar funções em `repo/resposta_chamado_repo.py`

```python
def obter_por_chamado(id_chamado: int) -> list[RespostaChamado]:
    """Retorna todas as respostas de um chamado"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM resposta_chamado
            WHERE id_chamado = ?
            ORDER BY data ASC
        """, (id_chamado,))
        rows = cursor.fetchall()
        return [RespostaChamado(**row) for row in rows]
```

**4. SQL:** Adicionar em `sql/resposta_chamado_sql.py`

```python
OBTER_POR_CHAMADO = """
SELECT * FROM resposta_chamado
WHERE id_chamado = ?
ORDER BY data ASC
"""
```

**5. Templates:**

**📄 `templates/admin/listar_chamados.html`**

```html
{% extends "base_publica.html" %}
{% block conteudo %}
<div class="container my-5">
    <h2 class="mb-4">Chamados de Suporte</h2>

    <!-- Filtros por status -->
    <div class="btn-group mb-3" role="group">
        <a href="?status=todos" class="btn btn-outline-roxo">Todos ({{ total }})</a>
        <a href="?status=aberto" class="btn btn-outline-warning">Abertos</a>
        <a href="?status=em_andamento" class="btn btn-outline-info">Em Andamento</a>
        <a href="?status=resolvido" class="btn btn-outline-success">Resolvidos</a>
    </div>

    <div class="table-responsive">
        <table class="table table-hover">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Usuário</th>
                    <th>Título</th>
                    <th>Status</th>
                    <th>Data</th>
                    <th>Ações</th>
                </tr>
            </thead>
            <tbody>
                {% for chamado in chamados %}
                <tr>
                    <td>{{ chamado.id_chamado }}</td>
                    <td>{{ chamado.nome_usuario }}</td>
                    <td>{{ chamado.titulo }}</td>
                    <td>
                        {% if chamado.status == 'aberto' %}
                            <span class="badge bg-warning">Aberto</span>
                        {% elif chamado.status == 'em_andamento' %}
                            <span class="badge bg-info">Em Andamento</span>
                        {% else %}
                            <span class="badge bg-success">Resolvido</span>
                        {% endif %}
                    </td>
                    <td>{{ chamado.data | data_br }}</td>
                    <td>
                        <a href="/administrador/responder_chamado/{{ chamado.id_chamado }}"
                           class="btn btn-sm btn-outline-roxo">
                            Ver/Responder
                        </a>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
```

**Variáveis:** `chamados` (lista), `total` (int)

---

**📄 `templates/admin/responder_chamado.html`**

```html
{% extends "base_publica.html" %}
{% block conteudo %}
<div class="container my-5">
    <h2 class="mb-4">Chamado #{{ chamado.id_chamado }}</h2>

    <!-- Informações do chamado -->
    <div class="card mb-4">
        <div class="card-header bg-roxo text-white">
            <h5>{{ chamado.titulo }}</h5>
        </div>
        <div class="card-body">
            <p><strong>Usuário:</strong> {{ chamado.nome_usuario }}</p>
            <p><strong>Email:</strong> {{ chamado.email_usuario }}</p>
            <p><strong>Data:</strong> {{ chamado.data | data_br }}</p>
            <p><strong>Status:</strong>
                <span class="badge bg-{{ 'warning' if chamado.status == 'aberto' else 'info' }}">
                    {{ chamado.status|capitalize }}
                </span>
            </p>
            <hr>
            <p><strong>Descrição:</strong></p>
            <p>{{ chamado.descricao }}</p>
        </div>
    </div>

    <!-- Respostas anteriores -->
    {% if respostas %}
    <h4>Respostas</h4>
    {% for resposta in respostas %}
    <div class="card mb-3">
        <div class="card-header">
            <strong>{{ resposta.titulo }}</strong>
            <small class="text-muted float-end">{{ resposta.data | data_hora_br }}</small>
        </div>
        <div class="card-body">
            {{ resposta.descricao }}
        </div>
    </div>
    {% endfor %}
    {% endif %}

    <!-- Formulário de nova resposta -->
    {% if chamado.status != 'resolvido' %}
    <h4 class="mt-4">Nova Resposta</h4>
    <form method="post" action="/administrador/responder_chamado">
        <input type="hidden" name="id_chamado" value="{{ chamado.id_chamado }}">

        <div class="mb-3">
            <label class="form-label">Título</label>
            <input type="text" name="titulo" class="form-control" required>
        </div>

        <div class="mb-3">
            <label class="form-label">Descrição</label>
            <textarea name="descricao" class="form-control" rows="5" required></textarea>
        </div>

        <button type="submit" class="btn btn-roxo">Enviar Resposta</button>
    </form>

    <!-- Botão para fechar chamado -->
    <form method="post" action="/administrador/fechar_chamado" class="mt-3">
        <input type="hidden" name="id_chamado" value="{{ chamado.id_chamado }}">
        <button type="submit" class="btn btn-success">Marcar como Resolvido</button>
    </form>
    {% endif %}

    <a href="/administrador/listar_chamados" class="btn btn-outline-secondary mt-3">
        Voltar para Lista
    </a>
</div>
{% endblock %}
```

**Variáveis:** `chamado` (objeto), `respostas` (lista)

---

**6. Registro em main.py:**

```python
from routes.admin import chamado_routes

app.include_router(
    chamado_routes.router,
    prefix="/administrador",
    tags=["admin-chamados"]
)
```

---

### 4.3 Funcionalidade: Moderar Comentários

**Status:** ❌ 0% implementado

**Descrição:** Visualizar e moderar comentários de artigos.

#### Implementação (resumida):

**Rota:** `routes/admin/comentario_admin_routes.py`

```python
@router.get("/moderar_comentarios")
@requer_autenticacao(perfis_autorizados=["admin"])
async def get_moderar_comentarios(request: Request):
    comentarios = comentario_artigo_repo.obter_pagina(limite=50, offset=0)
    return templates.TemplateResponse("admin/moderar_comentarios.html", {
        "request": request,
        "comentarios": comentarios
    })

@router.post("/excluir_comentario")
@requer_autenticacao(perfis_autorizados=["admin"])
async def post_excluir_comentario(request: Request, id_comentario: int = Form(...)):
    if comentario_artigo_repo.excluir(id_comentario):
        adicionar_mensagem_sucesso(request, "Comentário excluído.")
    return RedirectResponse("/administrador/moderar_comentarios", status_code=303)
```

**Template:** `templates/admin/moderar_comentarios.html`
- Tabela com: ID, Usuário, Artigo, Texto, Data
- Botão "Excluir" para cada comentário

---

### 4.4 Funcionalidade: Gerenciar Denúncias

**Status:** ❌ 0% implementado

**Descrição:** Visualizar e processar denúncias de conteúdo.

#### Implementação (resumida):

**Rota:** `routes/admin/denuncia_admin_routes.py`

```python
@router.get("/listar_denuncias")
@requer_autenticacao(perfis_autorizados=["admin"])
async def get_listar_denuncias(request: Request):
    denuncias = denuncia_repo.obter_pagina(limite=20, offset=0)
    return templates.TemplateResponse("admin/listar_denuncias.html", {
        "request": request,
        "denuncias": denuncias
    })

@router.post("/analisar_denuncia")
@requer_autenticacao(perfis_autorizados=["admin"])
async def post_analisar_denuncia(
    request: Request,
    id_denuncia: int = Form(...),
    novo_status: str = Form(...),  # 'em_analise', 'resolvida', 'rejeitada'
    usuario_logado: dict = None
):
    denuncia = denuncia_repo.obter_por_id(id_denuncia)
    denuncia.status = novo_status
    denuncia.id_admin = usuario_logado['id']
    denuncia_repo.atualizar(denuncia)

    adicionar_mensagem_sucesso(request, f"Denúncia marcada como {novo_status}.")
    return RedirectResponse("/administrador/listar_denuncias", status_code=303)

@router.post("/excluir_denuncia")
@requer_autenticacao(perfis_autorizados=["admin"])
async def post_excluir_denuncia(request: Request, id_denuncia: int = Form(...)):
    denuncia_repo.excluir(id_denuncia)
    return RedirectResponse("/administrador/listar_denuncias", status_code=303)
```

**Template:** `templates/admin/listar_denuncias.html`
- Tabela com filtros por status
- Ações: Analisar, Resolver, Rejeitar, Excluir

---

### 4.5 Funcionalidade: Verificar CRMV

**Status:** ❌ 0% implementado

**Descrição:** Aprovar/rejeitar solicitações de verificação de CRMV de veterinários.

#### Implementação (resumida):

**Rota:** `routes/admin/verificacao_crmv_routes.py`

```python
@router.get("/listar_verificacao_crmv")
@requer_autenticacao(perfis_autorizados=["admin"])
async def get_listar_verificacao(request: Request):
    verificacoes = verificacao_crmv_repo.obter_pagina(limite=20, offset=0)
    return templates.TemplateResponse("admin/listar_verificacao_crmv.html", {
        "request": request,
        "verificacoes": verificacoes
    })

@router.post("/responder_verificacao_crmv")
@requer_autenticacao(perfis_autorizados=["admin"])
async def post_responder_verificacao(
    request: Request,
    id_verificacao: int = Form(...),
    status_verificacao: str = Form(...),  # 'aprovado' ou 'rejeitado'
    usuario_logado: dict = None
):
    verificacao = verificacao_crmv_repo.obter_por_id(id_verificacao)
    verificacao.status_verificacao = status_verificacao
    verificacao.id_administrador = usuario_logado['id']

    if verificacao_crmv_repo.atualizar(verificacao):
        # Se aprovado, atualizar veterinário
        if status_verificacao == 'aprovado':
            from repo import veterinario_repo
            veterinario_repo.atualizar_verificacao(verificacao.id_veterinario, True)

        adicionar_mensagem_sucesso(request, f"Verificação {status_verificacao}.")

    return RedirectResponse("/administrador/listar_verificacao_crmv", status_code=303)
```

**Template:** `templates/admin/listar_verificacao_crmv.html`
- Lista de solicitações pendentes
- Informações do veterinário (nome, CRMV, data de solicitação)
- Botões: Aprovar / Rejeitar

**Template:** `templates/admin/responder_verificacao_crmv.html`
- Detalhes da solicitação
- Formulário com radio buttons (Aprovar/Rejeitar)

---

## 5. ÁREA DO TUTOR

### 5.1 Funcionalidade: Gerenciar Posts do Petgram

**Status:** ❌ 0% implementado (apenas stubs)

**Descrição:** Tutores podem criar, listar, editar e excluir posts com fotos de seus pets.

#### Arquivos a implementar:

**1. Rota:** `routes/tutor/postagem_feed_routes.py`

```python
from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import RedirectResponse
from util.auth_decorator import requer_autenticacao
from util.template_util import criar_templates
from util.mensagens import adicionar_mensagem_sucesso, adicionar_mensagem_erro
from repo import postagem_feed_repo
from model.postagem_feed_model import PostagemFeed
from util.file_validator import FileValidator
from util.file_manager import FileManager
from config.upload_config import UploadConfig
from datetime import datetime

router = APIRouter(prefix="/tutor")
templates = criar_templates("templates/tutor")

@router.get("/")
@requer_autenticacao(perfis_autorizados=["tutor"])
async def get_home_tutor(request: Request, usuario_logado: dict = None):
    """Dashboard do tutor"""
    # Buscar posts do tutor
    posts = postagem_feed_repo.obter_por_tutor(usuario_logado['id'])  # Criar função

    return templates.TemplateResponse("tutor/home_tutor.html", {
        "request": request,
        "posts": posts,
        "total_posts": len(posts)
    })

@router.get("/listar_postagem_feed")
@requer_autenticacao(perfis_autorizados=["tutor"])
async def get_listar_postagens(request: Request, usuario_logado: dict = None):
    """Lista todos os posts do tutor"""
    posts = postagem_feed_repo.obter_por_tutor(usuario_logado['id'])

    return templates.TemplateResponse("tutor/listar_postagens_feed.html", {
        "request": request,
        "posts": posts
    })

@router.get("/fazer_postagem_feed")
@requer_autenticacao(perfis_autorizados=["tutor"])
async def get_fazer_postagem(request: Request):
    """Formulário de nova postagem"""
    return templates.TemplateResponse("tutor/fazer_postagem_feed.html", {
        "request": request
    })

@router.post("/fazer_postagem_feed")
@requer_autenticacao(perfis_autorizados=["tutor"])
async def post_fazer_postagem(
    request: Request,
    descricao: str = Form(...),
    foto: UploadFile = File(...),
    usuario_logado: dict = None
):
    """Cria nova postagem com upload de foto"""
    from dtos.postagem_feed_dto import PostagemFeedDTO

    # 1. Validar campos
    try:
        dto = PostagemFeedDTO(descricao=descricao)
    except Exception as e:
        adicionar_mensagem_erro(request, str(e))
        return RedirectResponse("/tutor/fazer_postagem_feed", status_code=303)

    # 2. Validar imagem
    try:
        conteudo, extensao = await FileValidator.validar_imagem_completo(
            foto, max_size=UploadConfig.MAX_FILE_SIZE
        )
    except Exception as e:
        adicionar_mensagem_erro(request, f"Erro na imagem: {e}")
        return RedirectResponse("/tutor/fazer_postagem_feed", status_code=303)

    # 3. Criar postagem no banco
    post = PostagemFeed(
        id_postagem_feed=0,
        id_tutor=usuario_logado['id'],
        descricao=dto.descricao,
        data_postagem=datetime.now(),
        visualizacoes=0
    )

    id_post = postagem_feed_repo.inserir(post)

    if not id_post:
        adicionar_mensagem_erro(request, "Erro ao criar postagem.")
        return RedirectResponse("/tutor/fazer_postagem_feed", status_code=303)

    # 4. Salvar imagem com ID do post
    nome_arquivo = f"{id_post:08d}{extensao}"
    try:
        FileManager.salvar_arquivo(
            conteudo,
            nome_arquivo,
            id_post,
            subpasta="feeds"
        )
    except Exception as e:
        # Rollback: excluir postagem se falhar upload
        postagem_feed_repo.excluir(id_post)
        adicionar_mensagem_erro(request, "Erro ao salvar imagem.")
        return RedirectResponse("/tutor/fazer_postagem_feed", status_code=303)

    adicionar_mensagem_sucesso(request, "Post publicado com sucesso!")
    return RedirectResponse("/tutor/listar_postagem_feed", status_code=303)

@router.get("/editar_postagem_feed/{id_postagem}")
@requer_autenticacao(perfis_autorizados=["tutor"])
async def get_editar_postagem(
    request: Request,
    id_postagem: int,
    usuario_logado: dict = None
):
    """Formulário de edição (apenas descrição)"""
    post = postagem_feed_repo.obter_por_id(id_postagem)

    if not post or post.id_tutor != usuario_logado['id']:
        adicionar_mensagem_erro(request, "Postagem não encontrada ou sem permissão.")
        return RedirectResponse("/tutor/listar_postagem_feed", status_code=303)

    return templates.TemplateResponse("tutor/editar_postagem_feed.html", {
        "request": request,
        "post": post
    })

@router.post("/editar_postagem_feed")
@requer_autenticacao(perfis_autorizados=["tutor"])
async def post_editar_postagem(
    request: Request,
    id_postagem: int = Form(...),
    descricao: str = Form(...),
    usuario_logado: dict = None
):
    """Atualiza descrição do post"""
    post = postagem_feed_repo.obter_por_id(id_postagem)

    if not post or post.id_tutor != usuario_logado['id']:
        adicionar_mensagem_erro(request, "Sem permissão.")
        return RedirectResponse("/tutor/listar_postagem_feed", status_code=303)

    post.descricao = descricao
    if postagem_feed_repo.atualizar(post):
        adicionar_mensagem_sucesso(request, "Post atualizado!")
    else:
        adicionar_mensagem_erro(request, "Erro ao atualizar.")

    return RedirectResponse("/tutor/listar_postagem_feed", status_code=303)

@router.get("/excluir_postagem_feed/{id_postagem}")
@requer_autenticacao(perfis_autorizados=["tutor"])
async def get_excluir_postagem(
    request: Request,
    id_postagem: int,
    usuario_logado: dict = None
):
    """Confirmação de exclusão"""
    post = postagem_feed_repo.obter_por_id(id_postagem)

    if not post or post.id_tutor != usuario_logado['id']:
        adicionar_mensagem_erro(request, "Postagem não encontrada.")
        return RedirectResponse("/tutor/listar_postagem_feed", status_code=303)

    return templates.TemplateResponse("tutor/excluir_postagem_feed.html", {
        "request": request,
        "post": post
    })

@router.post("/excluir_postagem_feed")
@requer_autenticacao(perfis_autorizados=["tutor"])
async def post_excluir_postagem(
    request: Request,
    id_postagem: int = Form(...),
    usuario_logado: dict = None
):
    """Exclui postagem e imagem"""
    post = postagem_feed_repo.obter_por_id(id_postagem)

    if not post or post.id_tutor != usuario_logado['id']:
        adicionar_mensagem_erro(request, "Sem permissão.")
        return RedirectResponse("/tutor/listar_postagem_feed", status_code=303)

    # Excluir do banco
    if postagem_feed_repo.excluir(id_postagem):
        # Excluir imagem do disco
        FileManager.deletar_imagem_feed(id_postagem)
        adicionar_mensagem_sucesso(request, "Post excluído!")
    else:
        adicionar_mensagem_erro(request, "Erro ao excluir.")

    return RedirectResponse("/tutor/listar_postagem_feed", status_code=303)
```

**2. DTO:** Já existe `dtos/postagem_feed_dto.py` ✅

**3. Repositório:** Adicionar em `repo/postagem_feed_repo.py`

```python
def obter_por_tutor(id_tutor: int) -> list[PostagemFeed]:
    """Retorna todos os posts de um tutor"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM postagem_feed
            WHERE id_tutor = ?
            ORDER BY data_postagem DESC
        """, (id_tutor,))
        rows = cursor.fetchall()
        return [PostagemFeed(**row) for row in rows]
```

**4. Templates:**

**📄 `templates/tutor/home_tutor.html`**

```html
{% extends "base_publica.html" %}
{% block conteudo %}
<div class="container my-5">
    <h1 class="mb-4">Meu Painel - Tutor</h1>

    <div class="row mb-4">
        <div class="col-md-4">
            <div class="card text-center">
                <div class="card-body">
                    <i class="bi bi-image icon-lg text-laranja"></i>
                    <h3 class="mt-3">{{ total_posts }}</h3>
                    <p>Posts Publicados</p>
                </div>
            </div>
        </div>
    </div>

    <div class="d-flex justify-content-between align-items-center mb-3">
        <h3>Meus Posts</h3>
        <a href="/tutor/fazer_postagem_feed" class="btn btn-laranja">
            <i class="bi bi-plus-circle"></i> Novo Post
        </a>
    </div>

    <div class="row">
        {% for post in posts[:6] %}
        <div class="col-md-4 mb-4">
            {% include "componentes/petgram_card.html" %}
        </div>
        {% endfor %}
    </div>

    <a href="/tutor/listar_postagem_feed" class="btn btn-outline-roxo">
        Ver Todos os Posts
    </a>
</div>
{% endblock %}
```

**📄 `templates/tutor/fazer_postagem_feed.html`**

```html
{% extends "base_publica.html" %}
{% block conteudo %}
<div class="container my-5">
    <h2 class="mb-4">Nova Postagem no Petgram</h2>

    <form method="post" action="/tutor/fazer_postagem_feed" enctype="multipart/form-data">
        <div class="mb-3">
            <label class="form-label">Foto do Pet</label>
            <input type="file" name="foto" class="form-control"
                   accept="image/*" required>
            <small class="form-text">Tamanho máximo: 5MB. Formatos: JPG, PNG, WEBP</small>
        </div>

        <div class="mb-3">
            <label class="form-label">Descrição</label>
            <textarea name="descricao" class="form-control" rows="4"
                      placeholder="Conte sobre seu pet..." required></textarea>
        </div>

        <button type="submit" class="btn btn-laranja">Publicar</button>
        <a href="/tutor/" class="btn btn-outline-secondary">Cancelar</a>
    </form>
</div>
{% endblock %}
```

**📄 `templates/tutor/listar_postagens_feed.html`**

```html
{% extends "base_publica.html" %}
{% block conteudo %}
<div class="container my-5">
    <div class="d-flex justify-content-between mb-4">
        <h2>Meus Posts</h2>
        <a href="/tutor/fazer_postagem_feed" class="btn btn-laranja">Novo Post</a>
    </div>

    <div class="row">
        {% for post in posts %}
        <div class="col-md-4 mb-4">
            <div class="card">
                <img src="/static/img/feeds/{{ '%08d' % post.id_postagem_feed }}.jpg"
                     class="img-card-top" onerror="this.src='/static/img/default-post.jpg'">
                <div class="card-body">
                    <p class="card-text">{{ post.descricao }}</p>
                    <p class="text-muted">
                        <small>{{ post.data_postagem | data_hora_br }}</small>
                    </p>
                    <div class="d-flex gap-2">
                        <a href="/tutor/editar_postagem_feed/{{ post.id_postagem_feed }}"
                           class="btn btn-sm btn-outline-roxo">Editar</a>
                        <a href="/tutor/excluir_postagem_feed/{{ post.id_postagem_feed }}"
                           class="btn btn-sm btn-outline-danger">Excluir</a>
                    </div>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}
```

**📄 `templates/tutor/editar_postagem_feed.html`** e **`excluir_postagem_feed.html`**
- Formulários similares aos de admin (alterar_categoria e excluir_categoria)

**5. Registro em main.py:**

```python
from routes.tutor import postagem_feed_routes

app.include_router(
    postagem_feed_routes.router,
    prefix="/tutor",
    tags=["tutor"]
)
```

---

## 6. ÁREA DO VETERINÁRIO

### 6.1 Funcionalidade: Gerenciar Artigos

**Status:** ❌ 0% implementado

**Descrição:** Veterinários podem criar, listar, editar e excluir artigos educativos.

#### Implementação:

**Estrutura similar à área do tutor**, com as seguintes diferenças:

**Rota:** `routes/veterinario/postagem_artigo_routes.py`

```python
router = APIRouter(prefix="/veterinario")
templates = criar_templates("templates/veterinario")

@router.get("/")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def get_home_veterinario(request: Request, usuario_logado: dict = None):
    artigos = postagem_artigo_repo.obter_por_veterinario(usuario_logado['id'])  # Criar
    # Calcular estatísticas
    total_visualizacoes = sum(a.visualizacoes for a in artigos)
    # Buscar curtidas totais (criar query)

    return templates.TemplateResponse("veterinario/veterinario_home.html", {
        "request": request,
        "artigos": artigos,
        "total_artigos": len(artigos),
        "total_visualizacoes": total_visualizacoes
    })

@router.post("/cadastrar_postagem_artigo")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def post_cadastrar_artigo(
    request: Request,
    titulo: str = Form(...),
    conteudo: str = Form(...),
    id_categoria_artigo: int = Form(...),
    foto: UploadFile = File(...),
    usuario_logado: dict = None
):
    # Validar com PostagemArtigoDTO
    # Validar imagem
    # Criar artigo
    # Salvar imagem em /static/img/artigos/{ID:08d}.jpg
    # Redirecionar com mensagem de sucesso
```

**Repositório:** Adicionar `obter_por_veterinario()` em `repo/postagem_artigo_repo.py`

**Templates:**
- `templates/veterinario/veterinario_home.html` - Dashboard
- `templates/veterinario/listar_postagem_artigo.html` - Lista artigos
- `templates/veterinario/cadastrar_postagem_artigo.html` - Form criar
- `templates/veterinario/alterar_postagem_artigo.html` - Form editar
- `templates/veterinario/excluir_postagem_artigo.html` - Confirmação

**Registro:**
```python
from routes.veterinario import postagem_artigo_routes

app.include_router(postagem_artigo_routes.router, prefix="/veterinario", tags=["veterinario"])
```

---

### 6.2 Funcionalidade: Solicitar Verificação CRMV

**Status:** ❌ 0% implementado

**Descrição:** Veterinário solicita verificação do CRMV para obter selo verificado.

**Rota:** `routes/veterinario/solicitacao_crmv_routes.py`

```python
@router.get("/obter_solicitacao_crmv")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def get_solicitacao(request: Request, usuario_logado: dict = None):
    """Verifica se já existe solicitação"""
    verificacao = verificacao_crmv_repo.obter_por_veterinario(usuario_logado['id'])  # Criar

    return templates.TemplateResponse("veterinario/obter_solicitacao_crmv.html", {
        "request": request,
        "verificacao": verificacao
    })

@router.get("/fazer_solicitacao_crmv")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def get_fazer_solicitacao(request: Request):
    return templates.TemplateResponse("veterinario/fazer_solicitacao_crmv.html", {
        "request": request
    })

@router.post("/fazer_solicitacao_crmv")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def post_fazer_solicitacao(request: Request, usuario_logado: dict = None):
    from model.verificacao_crmv_model import VerificacaoCRMV

    # Verificar se já existe solicitação
    verificacao_existente = verificacao_crmv_repo.obter_por_veterinario(usuario_logado['id'])
    if verificacao_existente and verificacao_existente.status_verificacao == 'pendente':
        adicionar_mensagem_aviso(request, "Você já possui uma solicitação pendente.")
        return RedirectResponse("/veterinario/obter_solicitacao_crmv", status_code=303)

    # Criar nova solicitação
    verificacao = VerificacaoCRMV(
        id_verificacao_crmv=0,
        id_veterinario=usuario_logado['id'],
        id_administrador=None,
        data_verificacao=datetime.now(),
        status_verificacao='pendente'
    )

    if verificacao_crmv_repo.inserir(verificacao):
        adicionar_mensagem_sucesso(request, "Solicitação enviada! Aguarde análise.")
    else:
        adicionar_mensagem_erro(request, "Erro ao enviar solicitação.")

    return RedirectResponse("/veterinario/obter_solicitacao_crmv", status_code=303)
```

**Repositório:** Adicionar em `repo/verificacao_crmv_repo.py`

```python
def obter_por_veterinario(id_veterinario: int) -> Optional[VerificacaoCRMV]:
    """Retorna última verificação do veterinário"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM verificacao_crmv
            WHERE id_veterinario = ?
            ORDER BY data_verificacao DESC
            LIMIT 1
        """, (id_veterinario,))
        row = cursor.fetchone()
        return VerificacaoCRMV(**row) if row else None
```

**Templates:**
- `templates/veterinario/obter_solicitacao_crmv.html` - Status da solicitação
- `templates/veterinario/fazer_solicitacao_crmv.html` - Botão solicitar

---

### 6.3 Funcionalidade: Estatísticas

**Status:** ❌ 0% implementado

**Descrição:** Dashboard com estatísticas dos artigos do veterinário.

**Rota:** `routes/veterinario/estatisticas_routes.py`

```python
@router.get("/listar_estatisticas")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def get_estatisticas(request: Request, usuario_logado: dict = None):
    artigos = postagem_artigo_repo.obter_por_veterinario(usuario_logado['id'])

    # Calcular métricas
    total_artigos = len(artigos)
    total_visualizacoes = sum(a.visualizacoes for a in artigos)

    # Buscar curtidas (criar query agregada)
    from repo import curtida_artigo_repo
    total_curtidas = curtida_artigo_repo.contar_curtidas_veterinario(usuario_logado['id'])  # Criar

    # Artigo mais visto
    artigo_mais_visto = max(artigos, key=lambda a: a.visualizacoes) if artigos else None

    return templates.TemplateResponse("veterinario/listar_estatisticas.html", {
        "request": request,
        "total_artigos": total_artigos,
        "total_visualizacoes": total_visualizacoes,
        "total_curtidas": total_curtidas,
        "artigo_mais_visto": artigo_mais_visto,
        "artigos": artigos
    })
```

**Template:** `templates/veterinario/listar_estatisticas.html`
- Cards com métricas (total artigos, visualizações, curtidas)
- Gráfico ou tabela de artigos mais populares

---

## 7. FUNCIONALIDADES GERAIS DE USUÁRIO

### 7.1 Funcionalidade: Criar Chamado

**Status:** ❌ 0% implementado (stub sem autenticação)

**Arquivo:** `routes/usuario/usuario_routes.py`

**PROBLEMA CRÍTICO:** As rotas não têm `@requer_autenticacao` - ADICIONAR!

```python
@router.get("/solicitar_chamado")
@requer_autenticacao()  # ADICIONAR!
async def get_solicitar_chamado(request: Request):
    return templates.TemplateResponse("usuario/solicitar_chamado.html", {
        "request": request
    })

@router.post("/solicitar_chamado")
@requer_autenticacao()  # ADICIONAR!
async def post_solicitar_chamado(
    request: Request,
    titulo: str = Form(...),
    descricao: str = Form(...),
    usuario_logado: dict = None
):
    from dtos.chamado_dto import ChamadoDTO
    from model.chamado_model import Chamado

    try:
        dto = ChamadoDTO(titulo=titulo, descricao=descricao)
    except Exception as e:
        adicionar_mensagem_erro(request, str(e))
        return RedirectResponse("/usuario/solicitar_chamado", status_code=303)

    chamado = Chamado(
        id_chamado=0,
        id_usuario=usuario_logado['id'],
        id_admin=None,
        titulo=dto.titulo,
        descricao=dto.descricao,
        status='aberto',
        data=datetime.now()
    )

    if chamado_repo.inserir(chamado):
        adicionar_mensagem_sucesso(request, "Chamado criado! Responderemos em breve.")
    else:
        adicionar_mensagem_erro(request, "Erro ao criar chamado.")

    return RedirectResponse("/usuario/solicitacoes_chamado", status_code=303)

@router.get("/solicitacoes_chamado")
@requer_autenticacao()
async def get_solicitacoes_chamado(request: Request, usuario_logado: dict = None):
    """Lista chamados do usuário"""
    chamados = chamado_repo.obter_por_usuario(usuario_logado['id'])  # Criar função

    return templates.TemplateResponse("usuario/solicitacoes_chamado.html", {
        "request": request,
        "chamados": chamados
    })
```

**Repositório:** Adicionar em `repo/chamado_repo.py`

```python
def obter_por_usuario(id_usuario: int) -> list[Chamado]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM chamado
            WHERE id_usuario = ?
            ORDER BY data DESC
        """, (id_usuario,))
        return [Chamado(**row) for row in cursor.fetchall()]
```

**Templates:**
- `templates/usuario/solicitar_chamado.html` - Form criar chamado
- `templates/usuario/solicitacoes_chamado.html` - Lista chamados do usuário

---

### 7.2 Funcionalidade: Denunciar Conteúdo

**Status:** ❌ 0% implementado

```python
@router.get("/denunciar")
@requer_autenticacao()
async def get_denunciar(
    request: Request,
    tipo: str = Query(...),  # 'artigo' ou 'feed'
    id_conteudo: int = Query(...)
):
    return templates.TemplateResponse("usuario/denunciar.html", {
        "request": request,
        "tipo": tipo,
        "id_conteudo": id_conteudo
    })

@router.post("/denunciar")
@requer_autenticacao()
async def post_denunciar(
    request: Request,
    tipo: str = Form(...),
    id_conteudo: int = Form(...),
    motivo: str = Form(...),
    usuario_logado: dict = None
):
    from dtos.denuncia_dto import DenunciaDTO
    from model.denuncia_model import Denuncia

    try:
        dto = DenunciaDTO(motivo=motivo)
    except Exception as e:
        adicionar_mensagem_erro(request, str(e))
        return RedirectResponse(f"/usuario/denunciar?tipo={tipo}&id_conteudo={id_conteudo}",
                                status_code=303)

    denuncia = Denuncia(
        id_denuncia=0,
        id_usuario=usuario_logado['id'],
        id_admin=None,
        motivo=dto.motivo,
        data_denuncia=datetime.now(),
        status='pendente'
    )

    if denuncia_repo.inserir(denuncia):
        adicionar_mensagem_sucesso(request, "Denúncia enviada. Obrigado!")
    else:
        adicionar_mensagem_erro(request, "Erro ao enviar denúncia.")

    # Redirecionar para o conteúdo denunciado
    if tipo == 'artigo':
        return RedirectResponse(f"/artigos/{id_conteudo}", status_code=303)
    else:
        return RedirectResponse(f"/petgram/{id_conteudo}", status_code=303)
```

**Template:** `templates/usuario/denunciar.html`
- Formulário com textarea para motivo
- Hidden inputs para tipo e id_conteudo

**DTO:** Já existe `dtos/denuncia_dto.py` ✅

---

### 7.3 Funcionalidade: Comentar em Artigos

**Status:** ❌ Backend não implementado (front existe mas mostra "em breve")

**Localização do front:** `templates/publico/detalhes_artigo.html` linha ~94

```python
@router.get("/comentar")
@requer_autenticacao()
async def get_comentar(
    request: Request,
    id_artigo: int = Query(...)
):
    # Buscar artigo
    artigo = postagem_artigo_repo.obter_por_id(id_artigo)
    if not artigo:
        adicionar_mensagem_erro(request, "Artigo não encontrado.")
        return RedirectResponse("/artigos", status_code=303)

    return templates.TemplateResponse("usuario/comentar.html", {
        "request": request,
        "artigo": artigo
    })

@router.post("/comentar")
@requer_autenticacao()
async def post_comentar(
    request: Request,
    id_artigo: int = Form(...),
    texto: str = Form(...),
    usuario_logado: dict = None
):
    from dtos.comentario_dto import ComentarioDTO
    from model.comentario_model import ComentarioArtigo

    try:
        dto = ComentarioDTO(texto=texto)
    except Exception as e:
        adicionar_mensagem_erro(request, str(e))
        return RedirectResponse(f"/usuario/comentar?id_artigo={id_artigo}", status_code=303)

    comentario = ComentarioArtigo(
        id_comentario_artigo=0,
        id_usuario=usuario_logado['id'],
        id_postagem_artigo=id_artigo,
        texto=dto.texto,
        data_comentario=datetime.now(),
        data_moderacao=None
    )

    if comentario_artigo_repo.inserir(comentario):
        adicionar_mensagem_sucesso(request, "Comentário publicado!")
    else:
        adicionar_mensagem_erro(request, "Erro ao publicar comentário.")

    return RedirectResponse(f"/artigos/{id_artigo}", status_code=303)

@router.get("/comentarios")
@requer_autenticacao()
async def get_comentarios(request: Request, usuario_logado: dict = None):
    """Lista comentários do usuário"""
    comentarios = comentario_artigo_repo.obter_por_usuario(usuario_logado['id'])  # Criar

    return templates.TemplateResponse("usuario/comentarios.html", {
        "request": request,
        "comentarios": comentarios
    })

@router.post("/excluir_comentario/{id_comentario}")
@requer_autenticacao()
async def post_excluir_comentario(
    request: Request,
    id_comentario: int,
    usuario_logado: dict = None
):
    """Usuário pode excluir apenas seus próprios comentários"""
    comentario = comentario_artigo_repo.obter_por_id(id_comentario)

    if not comentario or comentario.id_usuario != usuario_logado['id']:
        adicionar_mensagem_erro(request, "Sem permissão.")
        return RedirectResponse("/usuario/comentarios", status_code=303)

    if comentario_artigo_repo.excluir(id_comentario):
        adicionar_mensagem_sucesso(request, "Comentário excluído.")
    else:
        adicionar_mensagem_erro(request, "Erro ao excluir.")

    return RedirectResponse("/usuario/comentarios", status_code=303)
```

**Repositório:** Adicionar em `repo/comentario_artigo_repo.py`

```python
def obter_por_usuario(id_usuario: int) -> list[ComentarioArtigo]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.*, a.titulo as titulo_artigo
            FROM comentario_artigo c
            JOIN postagem_artigo a ON c.id_postagem_artigo = a.id_postagem_artigo
            WHERE c.id_usuario = ?
            ORDER BY c.data_comentario DESC
        """, (id_usuario,))
        return [ComentarioArtigo(**row) for row in cursor.fetchall()]

def obter_por_artigo(id_artigo: int) -> list[ComentarioArtigo]:
    """Retorna comentários de um artigo com dados do autor"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.*, u.nome as nome_usuario
            FROM comentario_artigo c
            JOIN usuario u ON c.id_usuario = u.id_usuario
            WHERE c.id_postagem_artigo = ?
            ORDER BY c.data_comentario DESC
        """, (id_artigo,))
        return [ComentarioArtigo(**row) for row in cursor.fetchall()]
```

**Templates:**
- `templates/usuario/comentar.html` - Form comentário
- `templates/usuario/comentarios.html` - Lista comentários do usuário

**Integração:** Atualizar `templates/publico/detalhes_artigo.html`
- Remover linha 94: "Sistema de comentários em breve!"
- Adicionar formulário de comentário
- Listar comentários existentes usando `comentario_artigo_repo.obter_por_artigo()`

**DTO:** Já existe `dtos/comentario_dto.py` ✅

---

## 8. FUNCIONALIDADES PÚBLICAS PENDENTES

### 8.1 Sistema de Curtidas (Backend)

**Status:** ❌ Front existe (botões), mas alerta "em breve"

**Localização do front:**
- `templates/publico/detalhes_artigo.html` linha 71
- `templates/publico/detalhes_post.html` linha 73

#### Implementação necessária:

**1. Criar rotas em `routes/publico/public_routes.py`:**

```python
@router.post("/artigos/{id_artigo}/curtir")
@requer_autenticacao()
async def curtir_artigo(request: Request, id_artigo: int, usuario_logado: dict = None):
    from model.curtida_artigo_model import CurtidaArtigo
    from repo import curtida_artigo_repo
    from datetime import datetime

    # Verificar se já curtiu
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

@router.post("/petgram/{id_post}/curtir")
@requer_autenticacao()
async def curtir_post(request: Request, id_post: int, usuario_logado: dict = None):
    from model.curtida_feed_model import CurtidaFeed
    from repo import curtida_feed_repo

    curtida_existente = curtida_feed_repo.obter_por_id(usuario_logado['id'], id_post)

    if curtida_existente:
        curtida_feed_repo.excluir(usuario_logado['id'], id_post)
        adicionar_mensagem_info(request, "Curtida removida.")
    else:
        curtida = CurtidaFeed(
            id_usuario=usuario_logado['id'],
            id_postagem_feed=id_post,
            data_curtida=datetime.now()
        )
        curtida_feed_repo.inserir(curtida)
        adicionar_mensagem_sucesso(request, "Post curtido!")

    return RedirectResponse(f"/petgram/{id_post}", status_code=303)
```

**2. Atualizar templates:**

**Em `templates/publico/detalhes_artigo.html`:**

Substituir linha 71:
```html
<!-- ANTES: -->
<button class="btn btn-outline-laranja" onclick="alert('Funcionalidade de curtir em breve!')">

<!-- DEPOIS: -->
<form method="post" action="/artigos/{{ artigo.id_postagem_artigo }}/curtir" style="display: inline;">
    <button type="submit" class="btn {{ 'btn-laranja' if usuario_curtiu else 'btn-outline-laranja' }}">
        <i class="bi bi-heart{{ '-fill' if usuario_curtiu else '' }}"></i>
        {{ total_curtidas }}
    </button>
</form>
```

**Em `templates/publico/detalhes_post.html`:**

Substituir linha 73 com estrutura similar.

**3. Atualizar rotas GET para verificar se usuário curtiu:**

Em `routes/publico/public_routes.py`, nas funções `get_detalhes_artigo()` e `get_detalhes_post()`:

```python
# Verificar se usuário logado curtiu
usuario_curtiu = False
if usuario_logado:
    from repo import curtida_artigo_repo
    curtida = curtida_artigo_repo.obter_por_id(usuario_logado['id'], id_artigo)
    usuario_curtiu = curtida is not None

return templates.TemplateResponse("publico/detalhes_artigo.html", {
    "request": request,
    "artigo": artigo,
    "total_curtidas": total_curtidas,
    "usuario_curtiu": usuario_curtiu  # Adicionar esta variável
})
```

**Nota:** Os repositórios de curtida já estão implementados ✅

---

### 8.2 Sistema de Busca

**Status:** ❌ Form existe no navbar, mas sem action

**Localização:** `templates/base_publica.html` linhas 50-58

#### Implementação necessária:

**1. Criar rota em `routes/publico/public_routes.py`:**

```python
@router.get("/buscar")
async def buscar(request: Request, q: str = Query(None), tipo: str = Query("artigos")):
    """Busca em artigos ou posts"""
    if not q or len(q.strip()) < 3:
        return templates.TemplateResponse("publico/buscar.html", {
            "request": request,
            "erro": "Digite pelo menos 3 caracteres para buscar."
        })

    termo = q.strip()
    resultados = []

    if tipo == "artigos":
        from repo import postagem_artigo_repo
        resultados = postagem_artigo_repo.buscar_por_termo(termo)  # Criar função
    elif tipo == "petgram":
        from repo import postagem_feed_repo
        resultados = postagem_feed_repo.buscar_por_termo(termo)  # Criar função

    return templates.TemplateResponse("publico/buscar.html", {
        "request": request,
        "termo": termo,
        "tipo": tipo,
        "resultados": resultados,
        "total": len(resultados)
    })
```

**2. Adicionar funções de busca nos repositórios:**

**Em `repo/postagem_artigo_repo.py`:**

```python
def buscar_por_termo(termo: str) -> list[PostagemArtigo]:
    """Busca artigos por título ou conteúdo"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT pa.*, v.nome as nome_veterinario, ca.nome as nome_categoria, ca.cor as cor_categoria
            FROM postagem_artigo pa
            JOIN veterinario vet ON pa.id_veterinario = vet.id_veterinario
            JOIN usuario v ON vet.id_veterinario = v.id_usuario
            JOIN categoria_artigo ca ON pa.id_categoria_artigo = ca.id_categoria_artigo
            WHERE pa.titulo LIKE ? OR pa.conteudo LIKE ?
            ORDER BY pa.data_publicacao DESC
            LIMIT 50
        """, (f"%{termo}%", f"%{termo}%"))
        return [PostagemArtigo(**row) for row in cursor.fetchall()]
```

**Em `repo/postagem_feed_repo.py`:**

```python
def buscar_por_termo(termo: str) -> list[PostagemFeed]:
    """Busca posts por descrição"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT pf.*, t.nome as nome_tutor, t.quantidade_pets
            FROM postagem_feed pf
            JOIN tutor tut ON pf.id_tutor = tut.id_tutor
            JOIN usuario t ON tut.id_tutor = t.id_usuario
            WHERE pf.descricao LIKE ?
            ORDER BY pf.data_postagem DESC
            LIMIT 50
        """, (f"%{termo}%",))
        return [PostagemFeed(**row) for row in cursor.fetchall()]
```

**3. Atualizar form no navbar:**

Em `templates/base_publica.html` linha 50:

```html
<!-- ANTES: -->
<form class="d-flex">

<!-- DEPOIS: -->
<form class="d-flex" method="get" action="/buscar">
    <input class="form-control me-2" type="search" name="q"
           placeholder="Buscar..." required minlength="3">
    <select name="tipo" class="form-select me-2" style="max-width: 120px;">
        <option value="artigos">Artigos</option>
        <option value="petgram">Petgram</option>
    </select>
    <button class="btn btn-outline-laranja" type="submit">
        <i class="bi bi-search"></i>
    </button>
</form>
```

**4. Criar template:**

**📄 `templates/publico/buscar.html`**

```html
{% extends "base_publica.html" %}
{% block titulo %}Busca: {{ termo }}{% endblock %}
{% block conteudo %}
<div class="container my-5">
    {% if erro %}
    <div class="alert alert-warning">{{ erro }}</div>
    {% else %}
    <h2 class="mb-4">Resultados da busca: "{{ termo }}"</h2>
    <p class="text-muted">{{ total }} resultado(s) encontrado(s) em {{ tipo }}</p>

    {% if total == 0 %}
    <div class="alert alert-info">
        Nenhum resultado encontrado. Tente outros termos.
    </div>
    {% endif %}

    <div class="row">
        {% if tipo == 'artigos' %}
            {% for artigo in resultados %}
            <div class="col-md-4 mb-4">
                {% include "componentes/artigo_card.html" %}
            </div>
            {% endfor %}
        {% elif tipo == 'petgram' %}
            {% for post in resultados %}
            <div class="col-md-4 mb-4">
                {% include "componentes/petgram_card.html" %}
            </div>
            {% endfor %}
        {% endif %}
    </div>
    {% endif %}
</div>
{% endblock %}
```

---

## 9. MELHORIAS NO BANCO DE DADOS

### 9.1 Operações de Repositório Faltantes

#### `repo/chamado_repo.py`

```python
def contar_total() -> int:
    """Conta total de chamados"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as total FROM chamado")
        return cursor.fetchone()["total"]

def contar_por_status(status: str) -> int:
    """Conta chamados por status"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as total FROM chamado WHERE status = ?", (status,))
        return cursor.fetchone()["total"]

def obter_por_status(status: str, limite: int = 20, offset: int = 0) -> list[Chamado]:
    """Busca chamados por status com paginação"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.*, u.nome as nome_usuario, u.email as email_usuario
            FROM chamado c
            JOIN usuario u ON c.id_usuario = u.id_usuario
            WHERE c.status = ?
            ORDER BY c.data DESC
            LIMIT ? OFFSET ?
        """, (status, limite, offset))
        return [Chamado(**row) for row in cursor.fetchall()]
```

#### `repo/denuncia_repo.py`

```python
def contar_por_status(status: str) -> int:
    """Conta denúncias por status"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as total FROM denuncia WHERE status = ?", (status,))
        return cursor.fetchone()["total"]

def obter_por_status(status: str, limite: int = 20, offset: int = 0) -> list[Denuncia]:
    """Busca denúncias por status"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT d.*, u.nome as nome_usuario
            FROM denuncia d
            JOIN usuario u ON d.id_usuario = u.id_usuario
            WHERE d.status = ?
            ORDER BY d.data_denuncia DESC
            LIMIT ? OFFSET ?
        """, (status, limite, offset))
        return [Denuncia(**row) for row in cursor.fetchall()]
```

#### `repo/curtida_artigo_repo.py`

```python
def contar_curtidas_veterinario(id_veterinario: int) -> int:
    """Conta total de curtidas em artigos de um veterinário"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) as total
            FROM curtida_artigo ca
            JOIN postagem_artigo pa ON ca.id_postagem_artigo = pa.id_postagem_artigo
            WHERE pa.id_veterinario = ?
        """, (id_veterinario,))
        return cursor.fetchone()["total"]
```

#### `repo/postagem_artigo_repo.py`

```python
def obter_por_veterinario(id_veterinario: int) -> list[PostagemArtigo]:
    """Retorna todos os artigos de um veterinário"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT pa.*, v.nome as nome_veterinario, ca.nome as nome_categoria, ca.cor as cor_categoria,
                   (SELECT COUNT(*) FROM curtida_artigo WHERE id_postagem_artigo = pa.id_postagem_artigo) as total_curtidas
            FROM postagem_artigo pa
            JOIN veterinario vet ON pa.id_veterinario = vet.id_veterinario
            JOIN usuario v ON vet.id_veterinario = v.id_usuario
            JOIN categoria_artigo ca ON pa.id_categoria_artigo = ca.id_categoria_artigo
            WHERE pa.id_veterinario = ?
            ORDER BY pa.data_publicacao DESC
        """, (id_veterinario,))
        return [PostagemArtigo(**row) for row in cursor.fetchall()]

def obter_mais_vistos(limite: int = 10) -> list[PostagemArtigo]:
    """Retorna artigos mais vistos"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT pa.*, v.nome as nome_veterinario, ca.nome as nome_categoria, ca.cor as cor_categoria
            FROM postagem_artigo pa
            JOIN veterinario vet ON pa.id_veterinario = vet.id_veterinario
            JOIN usuario v ON vet.id_veterinario = v.id_usuario
            JOIN categoria_artigo ca ON pa.id_categoria_artigo = ca.id_categoria_artigo
            ORDER BY pa.visualizacoes DESC
            LIMIT ?
        """, (limite,))
        return [PostagemArtigo(**row) for row in cursor.fetchall()]
```

### 9.2 SQL Queries Faltantes

Adicionar as seguintes constantes nos arquivos SQL correspondentes:

**`sql/chamado_sql.py`:**
```python
CONTAR_TOTAL = "SELECT COUNT(*) as total FROM chamado"
CONTAR_POR_STATUS = "SELECT COUNT(*) as total FROM chamado WHERE status = ?"
OBTER_POR_STATUS = """
SELECT c.*, u.nome as nome_usuario, u.email as email_usuario
FROM chamado c
JOIN usuario u ON c.id_usuario = u.id_usuario
WHERE c.status = ?
ORDER BY c.data DESC
LIMIT ? OFFSET ?
"""
OBTER_POR_USUARIO = """
SELECT * FROM chamado WHERE id_usuario = ? ORDER BY data DESC
"""
```

**`sql/resposta_chamado_sql.py`:**
```python
OBTER_POR_CHAMADO = """
SELECT * FROM resposta_chamado
WHERE id_chamado = ?
ORDER BY data ASC
"""
```

**`sql/postagem_artigo_sql.py`:**
```python
OBTER_POR_VETERINARIO = """
SELECT pa.*, v.nome as nome_veterinario, ca.nome as nome_categoria, ca.cor as cor_categoria,
       (SELECT COUNT(*) FROM curtida_artigo WHERE id_postagem_artigo = pa.id_postagem_artigo) as total_curtidas
FROM postagem_artigo pa
JOIN veterinario vet ON pa.id_veterinario = vet.id_veterinario
JOIN usuario v ON vet.id_veterinario = v.id_usuario
JOIN categoria_artigo ca ON pa.id_categoria_artigo = ca.id_categoria_artigo
WHERE pa.id_veterinario = ?
ORDER BY pa.data_publicacao DESC
"""

BUSCAR_POR_TERMO = """
SELECT pa.*, v.nome as nome_veterinario, ca.nome as nome_categoria, ca.cor as cor_categoria
FROM postagem_artigo pa
JOIN veterinario vet ON pa.id_veterinario = vet.id_veterinario
JOIN usuario v ON vet.id_veterinario = v.id_usuario
JOIN categoria_artigo ca ON pa.id_categoria_artigo = ca.id_categoria_artigo
WHERE pa.titulo LIKE ? OR pa.conteudo LIKE ?
ORDER BY pa.data_publicacao DESC
LIMIT 50
"""
```

---

## 10. CHECKLIST FINAL

### ✅ Correções de Bugs (Prioridade ALTA)

- [ ] **BUG #1**: Corrigir redirect em `categoria_artigo_routes.py` linha 62
- [ ] **BUG #2**: Implementar exclusão em `categoria_artigo_routes.py` linha 77-85
- [ ] **BUG #3**: Corrigir objeto request em `categoria_artigo_routes.py` linha 17

### ✅ Templates Faltantes (Prioridade ALTA)

- [ ] `templates/publico/perfil.html`
- [ ] `templates/publico/dados.html`
- [ ] `templates/publico/alterar_senha.html`

### ✅ Área Administrativa (Prioridade ALTA)

**Categorias de Artigos:**
- [ ] Corrigir bugs existentes (ver seção 2)
- [ ] Criar 5 templates: home, listar, cadastrar, alterar, excluir
- [ ] Registrar rota em `main.py`

**Chamados:**
- [ ] Implementar rotas GET e POST em `chamado_routes.py`
- [ ] Criar 2 templates: listar_chamados, responder_chamado
- [ ] Adicionar funções em `resposta_chamado_repo.py`
- [ ] Adicionar queries em SQL
- [ ] Registrar rota em `main.py`

**Comentários:**
- [ ] Implementar rotas em `comentario_admin_routes.py`
- [ ] Criar template `moderar_comentarios.html`
- [ ] Registrar rota em `main.py`

**Denúncias:**
- [ ] Implementar rotas em `denuncia_admin_routes.py`
- [ ] Criar templates (listar, analisar)
- [ ] Adicionar funções de contagem e filtro por status
- [ ] Registrar rota em `main.py`

**Verificação CRMV:**
- [ ] Implementar rotas em `verificacao_crmv_routes.py`
- [ ] Criar templates (listar, responder)
- [ ] Integrar com atualização de veterinário
- [ ] Registrar rota em `main.py`

### ✅ Área do Tutor (Prioridade MÉDIA)

- [ ] Implementar todas as rotas em `postagem_feed_routes.py`
- [ ] Criar 5 templates: home, listar, fazer, editar, excluir
- [ ] Adicionar `obter_por_tutor()` em repositório
- [ ] Integrar upload de imagens
- [ ] Registrar rota em `main.py`

### ✅ Área do Veterinário (Prioridade MÉDIA)

**Artigos:**
- [ ] Implementar rotas em `postagem_artigo_routes.py`
- [ ] Criar 5 templates
- [ ] Adicionar `obter_por_veterinario()` em repositório
- [ ] Integrar upload de imagens
- [ ] Registrar rota em `main.py`

**CRMV:**
- [ ] Implementar rotas em `solicitacao_crmv_routes.py`
- [ ] Criar 2 templates
- [ ] Adicionar `obter_por_veterinario()` em repositório
- [ ] Registrar rota em `main.py`

**Estatísticas:**
- [ ] Implementar rota em `estatisticas_routes.py`
- [ ] Criar template com dashboard
- [ ] Adicionar query de agregação de curtidas
- [ ] Registrar rota em `main.py`

### ✅ Funcionalidades de Usuário (Prioridade MÉDIA)

- [ ] **CRÍTICO**: Adicionar `@requer_autenticacao()` em TODAS as rotas de `usuario_routes.py`
- [ ] Implementar criação de chamados
- [ ] Implementar listagem de chamados do usuário
- [ ] Implementar denúncias
- [ ] Implementar comentários em artigos
- [ ] Implementar listagem e exclusão de próprios comentários
- [ ] Criar 6 templates de usuário
- [ ] Adicionar funções em repositórios
- [ ] Registrar rota em `main.py`

### ✅ Funcionalidades Públicas (Prioridade BAIXA)

**Sistema de Curtidas:**
- [ ] Criar rotas POST em `public_routes.py` (curtir/descurtir)
- [ ] Atualizar templates `detalhes_artigo.html` e `detalhes_post.html`
- [ ] Adicionar verificação de curtida nas rotas GET

**Sistema de Busca:**
- [ ] Criar rota GET `/buscar` em `public_routes.py`
- [ ] Adicionar `buscar_por_termo()` nos repositórios
- [ ] Criar template `buscar.html`
- [ ] Atualizar form no navbar de `base_publica.html`

**Comentários (integração com front):**
- [ ] Atualizar `detalhes_artigo.html` para listar comentários
- [ ] Remover mensagem "em breve"
- [ ] Adicionar `obter_por_artigo()` na rota GET de detalhes

### ✅ Melhorias no Banco de Dados (Prioridade BAIXA)

- [ ] Adicionar 8+ funções de repositório (ver seção 9.1)
- [ ] Adicionar queries SQL correspondentes (ver seção 9.2)
- [ ] Padronizar ordem de parâmetros (limite, offset)

### ✅ Funcionalidade Extra (Opcional)

- [ ] Envio de email na recuperação de senha (`auth_routes.py` linha 333)
- [ ] Sistema de seguir veterinários (tabela já existe)
- [ ] Feed personalizado baseado em seguidas

---

## 📚 RECURSOS E REFERÊNCIAS

### Documentação Oficial

- **FastAPI**: https://fastapi.tiangolo.com/
- **Pydantic**: https://docs.pydantic.dev/
- **Jinja2**: https://jinja.palletsprojects.com/
- **Bootstrap 5.3**: https://getbootstrap.com/docs/5.3/

### Arquivos de Referência no Projeto

**Rotas implementadas (usar como modelo):**
- `routes/publico/public_routes.py` - Exemplo completo de rotas públicas
- `routes/publico/auth_routes.py` - Autenticação e validação
- `routes/publico/perfil_routes.py` - Upload de arquivos e segurança

**DTOs (usar como modelo):**
- `dtos/postagem_artigo_dto.py` - Validação com Pydantic
- `dtos/chamado_dto.py` - Validação simples

**Templates (usar como modelo):**
- `templates/publico/artigos.html` - Listagem com paginação
- `templates/publico/detalhes_artigo.html` - Página de detalhes
- `templates/publico/cadastro.html` - Formulários complexos

**Componentes (reutilizar):**
- `templates/componentes/paginacao.html`
- `templates/componentes/artigo_card.html`
- `templates/componentes/petgram_card.html`

### Utilitários Disponíveis

**Mensagens:**
```python
from util.mensagens import adicionar_mensagem_sucesso, adicionar_mensagem_erro
```

**Autenticação:**
```python
from util.auth_decorator import requer_autenticacao
```

**Validação de arquivos:**
```python
from util.file_validator import FileValidator
from util.file_manager import FileManager
```

**Tratamento de erros:**
```python
from util.error_handlers import tratar_erro_rota
```

---

## 🎯 DICAS IMPORTANTES

### 1. Ordem de Implementação Sugerida

1. **Primeiro**: Corrigir os 3 bugs (seção 2)
2. **Segundo**: Criar templates faltantes de perfil
3. **Terceiro**: Completar área administrativa (começar por categorias)
4. **Quarto**: Implementar sistema de curtidas (alta visibilidade)
5. **Quinto**: Área do tutor e veterinário
6. **Sexto**: Funcionalidades de usuário
7. **Sétimo**: Sistema de busca e comentários

### 2. Padrões a Seguir SEMPRE

- **Rotas**: Sempre usar `@requer_autenticacao()` em áreas privadas
- **Mensagens**: Sempre usar toasts para feedback
- **Validação**: Sempre usar DTOs Pydantic
- **Redirecionamento**: Sempre usar status_code=303 em POST
- **Templates**: Sempre usar componentes existentes
- **Imagens**: Sempre usar formato `{ID:08d}.jpg` e fallback `onerror`
- **Database**: Sempre usar context manager `with get_connection()`

### 3. Testes Recomendados

Para cada funcionalidade implementada, testar:
- ✅ Usuário não autenticado não acessa área restrita
- ✅ Usuário de perfil errado não acessa (tutor não acessa área de vet)
- ✅ Validação de formulários funciona
- ✅ Mensagens de sucesso/erro aparecem
- ✅ Redirecionamentos funcionam
- ✅ Upload de imagens funciona e valida tipo
- ✅ Paginação funciona corretamente
- ✅ Operações de CRUD completas (Create, Read, Update, Delete)

### 4. Comandos Úteis

```bash
# Iniciar servidor
python main.py

# Rodar testes
pytest

# Ver logs
tail -f logs/app.log

# Resetar banco (CUIDADO - desenvolvimento apenas!)
rm dados.db && python main.py
```

### 5. Estrutura de Commit Sugerida

```
git commit -m "feat: Implementar gerenciamento de categorias (admin)"
git commit -m "fix: Corrigir redirect após criar categoria"
git commit -m "feat: Implementar sistema de curtidas"
git commit -m "feat: Criar área do tutor - gerenciar posts"
```

---

## ✨ CONCLUSÃO

Este documento fornece **todas as informações necessárias** para completar o projeto VetConecta. Cada seção contém:

- ✅ Descrição clara da funcionalidade
- ✅ Status atual de implementação
- ✅ Código completo ou estrutura das rotas
- ✅ Templates necessários com exemplos
- ✅ Integrações com repositórios existentes
- ✅ Padrões a seguir do projeto
- ✅ Arquivos a criar e modificar

**Estimativa de esforço:**
- Correções de bugs: 1-2 horas
- Templates faltantes: 2-3 horas
- Área administrativa: 8-12 horas
- Área do tutor: 4-6 horas
- Área do veterinário: 6-8 horas
- Funcionalidades de usuário: 6-8 horas
- Funcionalidades públicas: 4-6 horas
- **Total estimado: 31-45 horas de desenvolvimento**

**Dica final:** Implemente funcionalidade por funcionalidade, teste completamente antes de partir para a próxima. Não tente fazer tudo de uma vez. Use os exemplos de código fornecidos como base e adapte conforme necessário.

Boa sorte! 🚀

---

**Documento gerado por:** Claude Code
**Versão:** 1.0
**Data:** 2025
**Projeto:** VetConecta - IFES
