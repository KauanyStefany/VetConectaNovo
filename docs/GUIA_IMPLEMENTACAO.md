# GUIA DE IMPLEMENTAÇÃO - VetConecta

**Bem-vindo ao projeto VetConecta!** 🐾

Este guia orienta você na conclusão do projeto de forma organizada e eficiente.

---

## 📋 ANTES DE COMEÇAR

### 1. Leia os Documentos Base

- **PENDENCIAS.md** - Relatório detalhado de todas as funcionalidades pendentes com código

### 2. Configure o Ambiente

```bash
# 1. Ativar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Copiar .env.example para .env
cp .env.example .env

# 4. Gerar SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"
# Copiar o resultado para SECRET_KEY no .env

# 5. Inicializar banco de dados
python main.py
# Ctrl+C após ver "Application startup complete"

# 6. Verificar que o banco foi criado
ls -la dados.db  # Deve existir

# 7. Rodar testes para verificar setup
pytest
```

### 3. Explore o Projeto

```bash
# Estrutura de diretórios
tree -L 2 -I 'venv|__pycache__|*.pyc'

# Ver rotas registradas
grep -n "include_router" main.py

# Ver templates criados
ls templates/admin/
ls templates/tutor/
ls templates/veterinario/
ls templates/usuario/
```

---

## 🎯 ROTEIRO DE IMPLEMENTAÇÃO

### FASE 1: CORREÇÕES E SETUP (2-3 horas)

#### 1.1 Corrigir Bugs Existentes ⚠️ PRIORITÁRIO

**Arquivo:** `routes/admin/categoria_artigo_routes.py`

**Bug #1 - Linha 71** (redirect incorreto):
```python
# ANTES:
response = RedirectResponse("/administrador/cadastrar_categoria.html", status_code=303)

# DEPOIS:
from util.mensagens import adicionar_mensagem_sucesso
adicionar_mensagem_sucesso(request, "Categoria cadastrada com sucesso!")
response = RedirectResponse("/administrador/listar_categorias", status_code=303)
```

**Bug #2 - Linha 95** (exclusão não funciona):
```python
# ANTES:
if categoria_artigo_repo.obter_por_id(id_categoria):
    response = RedirectResponse("/administrador/categorias", status_code=303)
    return response

# DEPOIS:
from util.mensagens import adicionar_mensagem_sucesso, adicionar_mensagem_erro

categoria = categoria_artigo_repo.obter_por_id(id_categoria)
if not categoria:
    adicionar_mensagem_erro(request, "Categoria não encontrada.")
elif categoria_artigo_repo.excluir(id_categoria):
    adicionar_mensagem_sucesso(request, "Categoria excluída com sucesso!")
else:
    adicionar_mensagem_erro(request, "Erro ao excluir. Pode haver artigos vinculados.")

return RedirectResponse("/administrador/listar_categorias", status_code=303)
```

**Bug #3 - Linha 16** (request vazio):
```python
# ANTES:
{"request": {}, "categoria_artigo": categoria_artigo}

# DEPOIS:
{"request": request, "categoria_artigo": categoria_artigo}
```

**Testar:**
```bash
python main.py
# Acessar: http://127.0.0.1:8000/administrador/listar_categorias
# Testar: Criar, editar e excluir categoria
```

#### 1.2 Registrar Rotas em main.py

**Arquivo:** `main.py` - Adicionar após linha 62:

```python
# Rotas públicas adicionais
from routes.publico import perfil_routes
app.include_router(perfil_routes.router, prefix="/perfil", tags=["perfil"])

# Rotas admin
from routes.admin import (
    categoria_artigo_routes,
    chamado_routes,
    comentario_admin_routes,
    denuncia_admin_routes,
    verificacao_crmv_routes
)
app.include_router(categoria_artigo_routes.router, prefix="/administrador", tags=["admin-categorias"])
app.include_router(chamado_routes.router, prefix="/administrador", tags=["admin-chamados"])
app.include_router(comentario_admin_routes.router, prefix="/administrador", tags=["admin-comentarios"])
app.include_router(denuncia_admin_routes.router, prefix="/administrador", tags=["admin-denuncias"])
app.include_router(verificacao_crmv_routes.router, prefix="/administrador", tags=["admin-crmv"])

# Rotas tutor
from routes.tutor import postagem_feed_routes
app.include_router(postagem_feed_routes.router, prefix="/tutor", tags=["tutor"])

# Rotas veterinário
from routes.veterinario import (
    postagem_artigo_routes,
    solicitacao_crmv_routes,
    estatisticas_routes
)
app.include_router(postagem_artigo_routes.router, prefix="/veterinario", tags=["veterinario-artigos"])
app.include_router(solicitacao_crmv_routes.router, prefix="/veterinario", tags=["veterinario-crmv"])
app.include_router(estatisticas_routes.router, prefix="/veterinario", tags=["veterinario-stats"])

# Rotas usuário
from routes.usuario import usuario_routes
app.include_router(usuario_routes.router, prefix="/usuario", tags=["usuario"])
```

**Testar:**
```bash
python main.py
# Verificar logs: "INFO:     Application startup complete"
# Acessar http://127.0.0.1:8000/docs para ver todas as rotas
```

#### 1.3 Implementar Templates HTML

Os 33 templates já foram criados com TODOs detalhados. Escolha uma área para começar:

**Exemplo: templates/publico/perfil.html**
1. Abrir o arquivo
2. Ler o TODO no topo (instruções completas)
3. Implementar seguindo a estrutura indicada
4. Testar acessando a rota correspondente

---

### FASE 2: SISTEMA DE CURTIDAS (2-3 horas)

Este é visual e gratificante para começar!

#### 2.1 Adicionar Rotas de Curtida

**Arquivo:** `routes/publico/public_routes.py` - Adicionar ao final:

```python
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

# Fazer o mesmo para /petgram/{id_post}/curtir
```

#### 2.2 Modificar Template de Detalhes

**Arquivo:** `templates/publico/detalhes_artigo.html` - Linha 71:

```html
<!-- ANTES (com alert): -->
<button class="btn btn-outline-laranja" onclick="alert('...')">

<!-- DEPOIS: -->
{% if usuario_logado %}
<form method="post" action="/artigos/{{ artigo.id_postagem_artigo }}/curtir" style="display: inline;">
    <button type="submit" class="btn {{ 'btn-laranja' if usuario_curtiu else 'btn-outline-laranja' }}">
        <i class="bi bi-heart{{ '-fill' if usuario_curtiu else '' }}"></i>
        {{ total_curtidas }}
    </button>
</form>
{% else %}
<a href="/login" class="btn btn-outline-laranja">
    <i class="bi bi-heart"></i> {{ total_curtidas }}
</a>
{% endif %}
```

#### 2.3 Atualizar Rota GET

**Arquivo:** `routes/publico/public_routes.py` - Função `get_detalhes_artigo`:

Adicionar antes do `return`:
```python
# Verificar se usuário curtiu
usuario_curtiu = False
if usuario_logado:
    from repo import curtida_artigo_repo
    curtida = curtida_artigo_repo.obter_por_id(usuario_logado['id'], id_artigo)
    usuario_curtiu = curtida is not None

# Adicionar ao context:
return templates.TemplateResponse("publico/detalhes_artigo.html", {
    "request": request,
    "artigo": artigo,
    "total_curtidas": total_curtidas,
    "usuario_curtiu": usuario_curtiu,  # ADICIONAR ESTA LINHA
    "usuario_logado": usuario_logado
})
```

**Testar:**
1. Fazer login
2. Acessar um artigo
3. Clicar no botão de curtida
4. Verificar que muda de cor e contador atualiza

---

### FASE 3: ÁREA DO TUTOR (4-6 horas)

#### 3.1 Adicionar Função no Repositório

**Arquivo:** `repo/postagem_feed_repo.py` - Adicionar:

```python
def obter_por_tutor(id_tutor: int) -> list[PostagemFeed]:
    """Retorna todos os posts de um tutor"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT pf.*, t.nome as nome_tutor, t.quantidade_pets
            FROM postagem_feed pf
            JOIN tutor tut ON pf.id_tutor = tut.id_tutor
            JOIN usuario t ON tut.id_tutor = t.id_usuario
            WHERE pf.id_tutor = ?
            ORDER BY pf.data_postagem DESC
        """, (id_tutor,))
        rows = cursor.fetchall()
        return [PostagemFeed(**row) for row in rows]
```

#### 3.2 Implementar Rotas

**Arquivo:** `routes/tutor/postagem_feed_routes.py`

Ver **PENDENCIAS.md seção 5.1** para código completo de todas as 8 rotas.

**Estrutura:**
1. GET / - Dashboard (buscar posts)
2. GET /listar - Tabela de posts
3. GET /fazer - Form de criação
4. POST /fazer - Criar com upload
5. GET /editar/{id} - Form de edição
6. POST /editar - Atualizar
7. GET /excluir/{id} - Confirmação
8. POST /excluir - Excluir

**Dica:** Implementar uma rota por vez e testar antes de continuar.

#### 3.3 Implementar Templates

Seguir os TODOs nos arquivos:
- `templates/tutor/home_tutor.html`
- `templates/tutor/listar_postagens_feed.html`
- `templates/tutor/fazer_postagem_feed.html`
- `templates/tutor/editar_postagem_feed.html`
- `templates/tutor/excluir_postagem_feed.html`

**Testar:**
1. Login como tutor
2. Acessar /tutor/
3. Criar um post com foto
4. Editar descrição
5. Excluir post

---

### FASE 4: ÁREA DO VETERINÁRIO (5-7 horas)

Similar à área do tutor, mas com artigos.

#### 4.1 Implementar CRUD de Artigos

**Passos:**
1. Adicionar `obter_por_veterinario()` em `repo/postagem_artigo_repo.py`
2. Implementar 8 rotas em `routes/veterinario/postagem_artigo_routes.py`
3. Implementar 5 templates

Ver **PENDENCIAS.md seção 6.1** para código completo.

#### 4.2 Solicitar Verificação CRMV

**Passos:**
1. Adicionar `obter_por_veterinario()` em `repo/verificacao_crmv_repo.py`
2. Implementar 3 rotas em `routes/veterinario/solicitacao_crmv_routes.py`
3. Implementar 2 templates

Ver **PENDENCIAS.md seção 6.2**.

#### 4.3 Dashboard de Estatísticas

**Passos:**
1. Adicionar `contar_curtidas_veterinario()` em `repo/curtida_artigo_repo.py`
2. Implementar rota GET em `routes/veterinario/estatisticas_routes.py`
3. Implementar template com cards de métricas

Ver **PENDENCIAS.md seção 6.3**.

---

### FASE 5: ÁREA ADMINISTRATIVA (6-8 horas)

#### 5.1 Gerenciar Chamados

**Arquivo:** `routes/admin/chamado_routes.py`

**Passos:**
1. Implementar GET /listar_chamados (buscar do banco)
2. Implementar GET /responder_chamado/{id} (buscar chamado + respostas)
3. Adicionar POST /responder_chamado (criar resposta)
4. Adicionar POST /fechar_chamado (marcar como resolvido)
5. Adicionar funções em repositórios:
   - `contar_total()` em `repo/chamado_repo.py`
   - `obter_por_chamado()` em `repo/resposta_chamado_repo.py`
6. Implementar 2 templates

Ver **PENDENCIAS.md seção 4.2** para código completo.

**Testar:**
1. Criar chamado como usuário normal
2. Login como admin
3. Ver lista de chamados
4. Responder um chamado
5. Marcar como resolvido

#### 5.2 Moderar Comentários

**Arquivo:** `routes/admin/comentario_admin_routes.py`

Implementar listagem e exclusão de comentários.

Ver **PENDENCIAS.md seção 4.3**.

#### 5.3 Gerenciar Denúncias

**Arquivo:** `routes/admin/denuncia_admin_routes.py`

Implementar análise e processamento de denúncias.

Ver **PENDENCIAS.md seção 4.4**.

#### 5.4 Verificar CRMV

**Arquivo:** `routes/admin/verificacao_crmv_routes.py`

Implementar aprovação/rejeição de verificações.

Ver **PENDENCIAS.md seção 4.5**.

---

### FASE 6: FUNCIONALIDADES DE USUÁRIO (5-6 horas)

⚠️ **CRÍTICO:** Adicionar `@requer_autenticacao()` em TODAS as rotas primeiro!

**Arquivo:** `routes/usuario/usuario_routes.py`

#### 6.1 Sistema de Chamados

**Rotas:**
- GET /solicitar_chamado - Form
- POST /solicitar_chamado - Criar
- GET /solicitacoes_chamado - Listar do usuário

**Repositório:**
- Adicionar `obter_por_usuario()` em `repo/chamado_repo.py`

#### 6.2 Sistema de Denúncias

**Rotas:**
- GET /denunciar?tipo=...&id_conteudo=... - Form
- POST /denunciar - Salvar

#### 6.3 Sistema de Comentários

**Rotas:**
- GET /comentar?id_artigo=... - Form
- POST /comentar - Salvar
- GET /comentarios - Listar do usuário
- POST /excluir_comentario/{id} - Excluir próprio

**Repositório:**
- Adicionar `obter_por_usuario()` em `repo/comentario_artigo_repo.py`
- Adicionar `obter_por_artigo()` em `repo/comentario_artigo_repo.py`

Ver **PENDENCIAS.md seção 7** para código completo.

---

### FASE 7: SISTEMA DE BUSCA (2-3 horas)

#### 7.1 Adicionar Funções de Busca

**Arquivos:**
- `repo/postagem_artigo_repo.py` - Adicionar `buscar_por_termo()`
- `repo/postagem_feed_repo.py` - Adicionar `buscar_por_termo()`

#### 7.2 Implementar Rota

**Arquivo:** `routes/publico/public_routes.py`

```python
@router.get("/buscar")
async def buscar(request: Request, q: str = Query(None), tipo: str = Query("artigos")):
    if not q or len(q.strip()) < 3:
        return templates.TemplateResponse("publico/buscar.html", {
            "request": request,
            "erro": "Digite pelo menos 3 caracteres."
        })

    termo = q.strip()
    resultados = []

    if tipo == "artigos":
        from repo import postagem_artigo_repo
        resultados = postagem_artigo_repo.buscar_por_termo(termo)
    elif tipo == "petgram":
        from repo import postagem_feed_repo
        resultados = postagem_feed_repo.buscar_por_termo(termo)

    return templates.TemplateResponse("publico/buscar.html", {
        "request": request,
        "termo": termo,
        "tipo": tipo,
        "resultados": resultados,
        "total": len(resultados)
    })
```

#### 7.3 Modificar Navbar

**Arquivo:** `templates/base_publica.html` - Linha 50:

```html
<form method="get" action="/buscar" class="d-flex">
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

#### 7.4 Implementar Template

**Arquivo:** `templates/publico/buscar.html` - Seguir TODO

Ver **PENDENCIAS.md seção 8.2**.

---

## 🧪 TESTES

### Testar Cada Funcionalidade

```bash
# Rodar testes automatizados
pytest

# Rodar com cobertura
pytest --cov=repo --cov=routes

# Rodar teste específico
pytest tests/test_chamado_repo.py -v
```

### Checklist de Testes Manuais

**Autenticação:**
- [ ] Registro de tutor
- [ ] Registro de veterinário
- [ ] Login/Logout
- [ ] Recuperação de senha

**Áreas Protegidas:**
- [ ] Tutor não acessa área de veterinário
- [ ] Veterinário não acessa área de tutor
- [ ] Usuário não logado não acessa áreas privadas
- [ ] Admin acessa todas as áreas

**CRUD Completo:**
- [ ] Criar, listar, editar, excluir posts (tutor)
- [ ] Criar, listar, editar, excluir artigos (veterinário)
- [ ] Criar, listar, editar, excluir categorias (admin)

**Uploads:**
- [ ] Upload de foto de perfil
- [ ] Upload de imagem de post
- [ ] Upload de imagem de artigo
- [ ] Validação de tipo de arquivo
- [ ] Validação de tamanho

**Interações:**
- [ ] Curtir/descurtir artigo
- [ ] Curtir/descurtir post
- [ ] Comentar em artigo
- [ ] Excluir próprio comentário
- [ ] Criar chamado
- [ ] Fazer denúncia

**Admin:**
- [ ] Responder chamado
- [ ] Moderar comentários
- [ ] Processar denúncias
- [ ] Aprovar/rejeitar CRMV

**Busca:**
- [ ] Buscar artigos por termo
- [ ] Buscar posts por termo
- [ ] Validação de mínimo 3 caracteres

---

## 🐛 DEBUG

### Erros Comuns

**ImportError: cannot import name 'X'**
```python
# Verificar se o arquivo existe
# Verificar se a função/classe está definida
# Verificar circular imports
```

**TemplateNotFound**
```python
# Verificar caminho do template
# Verificar se extends está correto
# Verificar se o diretório está em criar_templates()
```

**405 Method Not Allowed**
```python
# Verificar se a rota POST está definida
# Verificar se o form tem method="post"
# Verificar se action aponta para rota correta
```

**401 Unauthorized**
```python
# Verificar se tem @requer_autenticacao()
# Verificar se usuário está logado
# Verificar perfil autorizado
```

### Ferramentas de Debug

```python
# Adicionar prints
print(f"DEBUG: variavel = {variavel}")

# Usar logging
import logging
logger = logging.getLogger(__name__)
logger.info(f"Info: {info}")
logger.error(f"Erro: {erro}")

# Ver logs do servidor
tail -f logs/app.log

# Usar debugger
import pdb; pdb.set_trace()
```

---

## 📚 RECURSOS

### Documentação

- **FastAPI**: https://fastapi.tiangolo.com/
- **Jinja2**: https://jinja.palletsprojects.com/
- **Bootstrap 5**: https://getbootstrap.com/docs/5.3/
- **Bootstrap Icons**: https://icons.getbootstrap.com/

### Comandos Úteis

```bash
# Ver estrutura do banco
sqlite3 dados.db ".schema"

# Ver dados de uma tabela
sqlite3 dados.db "SELECT * FROM usuario LIMIT 5;"

# Resetar banco (CUIDADO!)
rm dados.db && python main.py

# Ver rotas registradas
python -c "from main import app; print(app.routes)"

# Gerar requirements
pip freeze > requirements.txt
```

### Padrões do Projeto

**Sempre usar:**
- `@requer_autenticacao()` em rotas privadas
- `adicionar_mensagem_sucesso/erro()` para feedback
- DTOs Pydantic para validação
- `status_code=303` em RedirectResponse POST
- `{{ '%08d' % id }}` para IDs em nomes de arquivo
- `onerror="this.src='...'"` para fallback de imagens

**Nunca usar:**
- SQL direto nas rotas (usar repositórios)
- Senhas em texto plano (usar bcrypt)
- Arquivos sem validação de tipo (usar FileValidator)
- Redirect sem mensagem de feedback

---

## 🎓 DICAS FINAIS

1. **Implemente aos poucos**: Uma funcionalidade por vez
2. **Teste constantemente**: Não acumule código sem testar
3. **Leia os TODOs**: Eles têm instruções detalhadas
4. **Use PENDENCIAS.md**: Código completo de referência
5. **Commit frequente**: `git commit` a cada funcionalidade pronta
6. **Peça ajuda**: Se travar mais de 30min, revise a documentação
7. **Seja consistente**: Siga os padrões do código existente

---

## ✅ CHECKLIST FINAL

Antes de entregar:

- [ ] Todos os 3 bugs corrigidos
- [ ] Todas as rotas registradas em main.py
- [ ] Todos os 33 templates implementados
- [ ] Sistema de curtidas funcionando
- [ ] Área do tutor completa (CRUD posts)
- [ ] Área do veterinário completa (CRUD artigos + CRMV + stats)
- [ ] Área admin completa (chamados, denúncias, comentários, CRMV)
- [ ] Funcionalidades de usuário (chamados, denúncias, comentários)
- [ ] Sistema de busca funcionando
- [ ] Todos os testes passando
- [ ] Código commitado no Git
- [ ] README.md atualizado

**Boa sorte! 🚀**

---

*Documentação gerada para o projeto VetConecta - IFES 2025*
