# Análise de Segurança - VetConecta

**Data da Análise:** 2025-10-15
**Versão do Projeto:** VetConectaNovo
**Analisador:** Claude Code (Sonnet 4.5)

---

## 1. RESUMO EXECUTIVO

Esta análise identificou **vulnerabilidades críticas de segurança** no sistema VetConecta, com destaque para:

- **28 rotas completamente desprotegidas** que deveriam exigir autenticação e autorização
- **0 rotas administrativas protegidas** de um total de 16 rotas admin
- **Configurações de sessão inseguras** que invalidam sessões a cada reinicialização
- **Ausência de proteção CSRF** em formulários
- **Validação de senha fraca** (apenas 6 caracteres mínimos)
- **Exposição de informações sensíveis** em ambiente de desenvolvimento

### Nível de Severidade Geral: **CRÍTICO** 🔴

---

## 2. VULNERABILIDADES CRÍTICAS

### 2.1. Rotas Administrativas Completamente Desprotegidas

**Severidade:** 🔴 CRÍTICA
**Impacto:** Qualquer usuário não autenticado pode acessar funcionalidades administrativas

#### Rotas Afetadas (16 rotas admin):

**categoria_artigo_routes.py** (7 rotas):
```
GET  /admin/listar_categorias
GET  /admin/alterar_categoria/{id_categoria}
POST /admin/alterar_categoria
GET  /admin/cadastrar_categoria
POST /admin/cadastrar_categoria
GET  /admin/excluir_categoria/{id_categoria}
POST /admin/excluir_categoria
```

**chamado_routes.py** (3 rotas):
```
GET  /admin/listar_chamados
GET  /admin/responder_chamado/{id_chamado}
GET  /admin/excluir_chamado/{id_chamado}
```

**comentario_admin_routes.py** (1 rota):
```
GET  /admin/moderar_comentarios/{id_comentario}
```

**denuncia_admin_routes.py** (2 rotas):
```
GET  /admin/listar_denuncias
GET  /admin/excluir_denuncia/{id_denuncia}
```

**verificação_crmv_routes.py** (3 rotas):
```
GET  /admin/listar_verificação_crmv
GET  /admin/responder_verificação_crmv/{id_verificacao_crmv}
```

#### Impacto:
- Qualquer pessoa pode criar, modificar ou excluir categorias de artigos
- Acesso não autorizado a chamados de suporte
- Manipulação de moderação de comentários
- Acesso e exclusão de denúncias
- Manipulação de verificações de CRMV de veterinários

#### Solução:
Adicionar o decorator `@requer_autenticacao(perfis_autorizados=["admin"])` em TODAS as rotas administrativas.

**Exemplo de correção para categoria_artigo_routes.py:15-20:**
```python
from util.auth_decorator import requer_autenticacao

@router.get("/listar_categorias")
@requer_autenticacao(perfis_autorizados=["admin"])
async def get_listar_categorias(request: Request):
    return templates.TemplateResponse("administrador/listar_categorias.html", {"request": request})
```

---

### 2.2. Rotas de Veterinários Desprotegidas

**Severidade:** 🔴 CRÍTICA
**Impacto:** Qualquer usuário pode acessar e manipular conteúdo de veterinários

#### Rotas Afetadas (8 rotas):

**postagem_artigo_routes.py** (5 rotas):
```
GET  /veterinario/listar_postagem_artigo
GET  /veterinario/alterar_postagem_artigo/{id_postagem_artigo}
GET  /veterinario/cadastrar_postagem_artigo
GET  /veterinario/excluir_postagem_artigo/{id_postagem_artigo}
```

**estatisticas_routes.py** (1 rota):
```
GET  /veterinario/listar_estatisticas
```

**solicitacao_crmv_routes.py** (2 rotas):
```
GET  /veterinario/obter_solicitacao_crmv
GET  /veterinario/fazer_solicitacao_crmv
```

#### Solução:
```python
@router.get("/listar_postagem_artigo")
@requer_autenticacao(perfis_autorizados=["veterinario"])
async def get_listar_postagem_artigo(request: Request):
    # código existente...
```

---

### 2.3. Rotas de Tutores Desprotegidas

**Severidade:** 🔴 CRÍTICA
**Impacto:** Acesso não autorizado ao feed e postagens de tutores

#### Rotas Afetadas (4 rotas):

**postagem_feed_routes.py**:
```
GET  /tutor/listar_postagem_feed
GET  /tutor/fazer_postagem_feed
GET  /tutor/excluir_postagem_feed
```

#### Solução:
```python
@router.get("/listar_postagem_feed")
@requer_autenticacao(perfis_autorizados=["tutor"])
async def pagina_listar_postagem_feed(request: Request):
    # código existente...
```

---

## 3. VULNERABILIDADES DE CONFIGURAÇÃO

### 3.1. Chave Secreta Regenerada a Cada Reinicialização

**Severidade:** 🟠 ALTA
**Arquivo:** main.py:23
**Código Problemático:**
```python
SECRET_KEY = secrets.token_urlsafe(32)
```

#### Problema:
A chave secreta é gerada aleatoriamente toda vez que a aplicação reinicia, invalidando todas as sessões ativas dos usuários.

#### Impacto:
- Todos os usuários são forçados a fazer login novamente após cada reinicialização
- Tokens de sessão ficam inválidos
- Má experiência do usuário

#### Solução:
Usar variável de ambiente para a chave secreta:

```python
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY não configurada nas variáveis de ambiente")

app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    max_age=3600,
    same_site="lax",
    https_only=True  # Mudar para True em produção
)
```

Criar arquivo `.env`:
```
SECRET_KEY=gere_uma_chave_segura_aqui_com_secrets_token_urlsafe_32
```

---

### 3.2. Configuração HTTPS Desabilitada

**Severidade:** 🟠 ALTA
**Arquivo:** main.py:31
**Código Problemático:**
```python
https_only=False  # Em produção, mude para True com HTTPS
```

#### Problema:
Cookies de sessão podem ser transmitidos por HTTP não criptografado.

#### Impacto:
- Vulnerabilidade a ataques man-in-the-middle (MITM)
- Sessões podem ser interceptadas
- Roubo de credenciais de sessão

#### Solução:
```python
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    max_age=3600,
    same_site="lax",
    https_only=True if os.getenv("ENVIRONMENT") == "production" else False
)
```

---

## 4. VULNERABILIDADES DE AUTENTICAÇÃO

### 4.1. Ausência de Rate Limiting

**Severidade:** 🟠 ALTA
**Arquivo:** auth_routes.py:31-107

#### Problema:
Não há limitação de tentativas de login, permitindo ataques de força bruta.

#### Impacto:
- Ataques de força bruta ilimitados
- Credential stuffing
- Consumo excessivo de recursos

#### Solução:
Implementar rate limiting com slowapi:

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@router.post("/login")
@limiter.limit("5/minute")  # 5 tentativas por minuto
async def post_login(request: Request, ...):
    # código existente...
```

---

### 4.2. Validação de Senha Fraca

**Severidade:** 🟡 MÉDIA
**Arquivo:** util/security.py:65-79

**Código Atual:**
```python
def validar_forca_senha(senha: str) -> tuple[bool, str]:
    if len(senha) < 6:
        return False, "A senha deve ter pelo menos 6 caracteres"
    # ... outras validações comentadas
```

#### Problema:
Apenas verifica comprimento mínimo de 6 caracteres. Validações de maiúsculas, minúsculas, números e caracteres especiais estão comentadas.

#### Impacto:
- Senhas fracas como "123456" são aceitas
- Vulnerável a ataques de dicionário
- Comprometimento fácil de contas

#### Solução:
Implementar validação robusta:

```python
import re

def validar_forca_senha(senha: str) -> tuple[bool, str]:
    if len(senha) < 8:
        return False, "A senha deve ter pelo menos 8 caracteres"

    if not re.search(r"[a-z]", senha):
        return False, "A senha deve conter pelo menos uma letra minúscula"

    if not re.search(r"[A-Z]", senha):
        return False, "A senha deve conter pelo menos uma letra maiúscula"

    if not re.search(r"\d", senha):
        return False, "A senha deve conter pelo menos um número"

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha):
        return False, "A senha deve conter pelo menos um caractere especial"

    senhas_comuns = ["123456", "password", "123456789", "12345678", "qwerty"]
    if senha.lower() in senhas_comuns:
        return False, "Esta senha é muito comum. Escolha uma senha mais segura."

    return True, ""
```

---

### 4.3. Tratamento de Erros com Bare Except

**Severidade:** 🟡 MÉDIA
**Arquivo:** util/security.py:39

**Código Problemático:**
```python
def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    try:
        return pwd_context.verify(senha_plana, senha_hash)
    except:
        return False
```

#### Problema:
Captura todas as exceções indiscriminadamente, mascarando erros críticos.

#### Impacto:
- Falhas silenciosas
- Dificulta debugging
- Pode ocultar problemas de segurança

#### Solução:
```python
import logging

logger = logging.getLogger(__name__)

def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    try:
        return pwd_context.verify(senha_plana, senha_hash)
    except ValueError as e:
        logger.warning(f"Erro ao verificar senha: hash inválido - {e}")
        return False
    except Exception as e:
        logger.error(f"Erro inesperado ao verificar senha: {e}")
        return False
```

---

### 4.4. Exposição de Debug Link em Produção

**Severidade:** 🟡 MÉDIA
**Arquivo:** auth_routes.py:264-272

**Código Problemático:**
```python
link_redefinicao = f"http://localhost:8000/redefinir-senha/{token}"

return templates.TemplateResponse(
    "esqueci_senha.html",
    {
        "request": request,
        "sucesso": mensagem_sucesso,
        "debug_link": link_redefinicao  # Remover em produção
    }
)
```

#### Problema:
Link de redefinição de senha exposto na resposta HTTP.

#### Impacto:
- Tokens de redefinição visíveis em logs
- Possibilidade de roubo de tokens
- Comprometimento de contas

#### Solução:
```python
response_data = {
    "request": request,
    "sucesso": mensagem_sucesso
}

# Apenas incluir debug_link em ambiente de desenvolvimento
if os.getenv("ENVIRONMENT") == "development":
    link_redefinicao = f"http://localhost:8000/redefinir-senha/{token}"
    response_data["debug_link"] = link_redefinicao

return templates.TemplateResponse("esqueci_senha.html", response_data)
```

---

### 4.5. Ausência de Proteção CSRF

**Severidade:** 🟠 ALTA
**Afetado:** Todos os formulários POST

#### Problema:
Não há implementação de proteção CSRF em nenhum formulário.

#### Impacto:
- Vulnerável a ataques Cross-Site Request Forgery
- Ações não autorizadas em nome do usuário
- Manipulação de dados

#### Solução:
Implementar CSRF com fastapi-csrf-protect:

```python
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from pydantic import BaseModel

class CsrfSettings(BaseModel):
    secret_key: str = os.getenv("CSRF_SECRET_KEY", SECRET_KEY)
    cookie_samesite: str = "lax"

@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()

# Em cada rota POST:
@router.post("/login")
async def post_login(
    request: Request,
    csrf_protect: CsrfProtect = Depends(),
    email: str = Form(),
    senha: str = Form()
):
    await csrf_protect.validate_csrf(request)
    # resto do código...
```

---

### 4.6. Validação de Perfil Ausente

**Severidade:** 🟡 MÉDIA
**Arquivo:** auth_routes.py:133

**Código com TODO:**
```python
perfil: str = Form(), # TODO: adicionar restricao para aceitar apenas 'tutor' ou 'veterinario'
```

#### Problema:
Não há validação do campo perfil no cadastro.

#### Impacto:
- Usuários podem se cadastrar com perfis inválidos
- Possibilidade de escalonamento de privilégios
- Dados inconsistentes

#### Solução:
```python
from enum import Enum

class PerfilUsuario(str, Enum):
    TUTOR = "tutor"
    VETERINARIO = "veterinario"

@router.post("/cadastro")
async def post_cadastro(
    request: Request,
    nome: str = Form(),
    email: str = Form(),
    telefone: str = Form(),
    senha: str = Form(),
    confirmar_senha: str = Form(),
    perfil: PerfilUsuario = Form(),
    crmv: str = Form(None)
):
    # código existente...
```

---

### 4.7. Fixação de Sessão

**Severidade:** 🟠 ALTA
**Arquivo:** auth_routes.py:59-68

#### Problema:
A sessão não é regenerada após o login bem-sucedido, permitindo ataques de fixação de sessão.

#### Impacto:
- Atacante pode fixar um ID de sessão e obter acesso após o usuário fazer login
- Comprometimento de conta

#### Solução:
Modificar `criar_sessao` em auth_decorator.py para regenerar o session ID:

```python
def criar_sessao(request: Request, usuario: dict):
    # Limpar sessão anterior
    request.session.clear()

    # Criar nova sessão com novos dados
    request.session["usuario"] = usuario
    request.session["criado_em"] = datetime.now().isoformat()

    # Forçar regeneração do cookie de sessão
    request.session.modified = True
```

---

### 4.8. Ausência de Bloqueio de Conta

**Severidade:** 🟡 MÉDIA
**Arquivo:** auth_routes.py:31-107

#### Problema:
Não há mecanismo de bloqueio de conta após múltiplas tentativas de login falhadas.

#### Impacto:
- Ataques de força bruta prolongados
- Sem proteção adicional além do rate limiting

#### Solução:
Implementar contador de tentativas falhadas:

```python
# Adicionar na tabela usuario
# tentativas_login: int
# bloqueado_ate: datetime

@router.post("/login")
async def post_login(...):
    usuario = usuario_repo.obter_por_email(login_dto.email)

    if usuario and usuario.bloqueado_ate:
        if datetime.now() < usuario.bloqueado_ate:
            return templates.TemplateResponse(
                "login.html",
                {
                    "request": request,
                    "erros": {"GERAL": "Conta temporariamente bloqueada. Tente novamente mais tarde."},
                    "email": email
                }
            )

    if not usuario or not verificar_senha(login_dto.senha, usuario.senha):
        # Incrementar tentativas
        if usuario:
            tentativas = usuario_repo.incrementar_tentativas_login(usuario.id_usuario)
            if tentativas >= 5:
                # Bloquear por 15 minutos
                usuario_repo.bloquear_conta(usuario.id_usuario, minutos=15)

        return templates.TemplateResponse(...)

    # Login bem-sucedido - resetar tentativas
    usuario_repo.resetar_tentativas_login(usuario.id_usuario)
    # ... resto do código
```

---

## 5. VULNERABILIDADES DE EXCEPTION HANDLING

### 5.1. Bare Exception Handlers em Rotas de Autenticação

**Severidade:** 🟡 MÉDIA
**Arquivo:** auth_routes.py:100-107, 233-238

**Código Problemático:**
```python
except Exception as e:
    # logger.error(f"Erro ao processar cadastro: {e}")
    return templates.TemplateResponse("login.html", {
        "request": request,
        "erros": {"GERAL": "Erro ao processar o login. Tente novamente."},
        "dados": dados_formulario
    })
```

#### Problema:
- Logging comentado
- Captura genérica de todas as exceções
- Falta de rastreabilidade de erros

#### Impacto:
- Dificuldade em diagnosticar problemas
- Falhas silenciosas
- Falta de auditoria

#### Solução:
```python
import logging

logger = logging.getLogger(__name__)

except ValidationError as e:
    # Tratar erro de validação especificamente
    logger.warning(f"Erro de validação no login - Email: {email} - Erros: {e.errors()}")
    # ... código de resposta

except Exception as e:
    logger.error(f"Erro crítico ao processar login - Email: {email} - Erro: {str(e)}", exc_info=True)

    return templates.TemplateResponse("login.html", {
        "request": request,
        "erros": {"GERAL": "Erro ao processar o login. Tente novamente."},
        "dados": dados_formulario
    })
```

---

## 6. RESUMO DE ROTAS PROTEGIDAS vs DESPROTEGIDAS

### Situação Atual:

| Categoria | Total de Rotas | Protegidas | Desprotegidas | % Desprotegido |
|-----------|---------------|------------|---------------|----------------|
| Admin | 16 | 0 | 16 | 100% |
| Veterinário | 8 | 0 | 8 | 100% |
| Tutor | 4 | 0 | 4 | 100% |
| Perfil | 6 | 6 | 0 | 0% |
| Autenticação | 10 | 0 | 10 | N/A |
| **TOTAL** | **44** | **6** | **38** | **86%** |

### Rotas que DEVEM ser protegidas: 28 rotas

---

## 7. PLANO DE AÇÃO PRIORITÁRIO

### Fase 1: CRÍTICO - Implementar Imediatamente (Semana 1)

1. **Proteger TODAS as rotas administrativas** com `@requer_autenticacao(perfis_autorizados=["admin"])`
2. **Proteger rotas de veterinários** com `@requer_autenticacao(perfis_autorizados=["veterinario"])`
3. **Proteger rotas de tutores** com `@requer_autenticacao(perfis_autorizados=["tutor"])`
4. **Configurar SECRET_KEY em variável de ambiente**

### Fase 2: ALTA - Implementar em 2 Semanas

5. **Implementar rate limiting** em rotas de login/cadastro
6. **Adicionar proteção CSRF** em todos os formulários
7. **Configurar https_only=True** para produção
8. **Corrigir regeneração de sessão** após login
9. **Remover debug_link** de produção

### Fase 3: MÉDIA - Implementar em 1 Mês

10. **Fortalecer validação de senha** (8+ chars, complexidade)
11. **Implementar bloqueio de conta** após tentativas falhadas
12. **Adicionar logging robusto** com auditoria
13. **Corrigir exception handlers** (remover bare except)
14. **Validar campo perfil** com Enum

### Fase 4: MONITORAMENTO - Contínuo

15. **Implementar sistema de logs de segurança**
16. **Configurar alertas de segurança**
17. **Realizar testes de penetração**
18. **Auditorias de segurança regulares**

---

## 8. CHECKLIST DE IMPLEMENTAÇÃO

### Para CADA rota protegida:

```python
# ✅ Importar decorator
from util.auth_decorator import requer_autenticacao

# ✅ Adicionar decorator com perfis corretos
@router.get("/rota")
@requer_autenticacao(perfis_autorizados=["perfil_correto"])
async def funcao_rota(request: Request):
    # ✅ Obter usuário logado
    usuario = obter_usuario_logado(request)

    # ✅ Validar autorização adicional se necessário
    if usuario.get('id') != recurso.id_dono:
        raise HTTPException(status_code=403)

    # código da rota...
```

---

## 9. EXEMPLOS DE CÓDIGO CORRIGIDO

### 9.1. Exemplo: Protegendo Rota Admin

**ANTES (categoria_artigo_routes.py:18-20):**
```python
@router.get("/listar_categorias")
async def get_listar_categorias(request: Request):
    return templates.TemplateResponse("administrador/listar_categorias.html", {"request": request})
```

**DEPOIS:**
```python
from util.auth_decorator import requer_autenticacao, obter_usuario_logado

@router.get("/listar_categorias")
@requer_autenticacao(perfis_autorizados=["admin"])
async def get_listar_categorias(request: Request):
    usuario_logado = obter_usuario_logado(request)
    return templates.TemplateResponse(
        "administrador/listar_categorias.html",
        {"request": request, "usuario": usuario_logado}
    )
```

### 9.2. Exemplo: Configuração Segura (main.py)

**ANTES:**
```python
SECRET_KEY = secrets.token_urlsafe(32)

app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    max_age=3600,
    same_site="lax",
    https_only=False
)
```

**DEPOIS:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY não configurada. Defina a variável de ambiente SECRET_KEY.")

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    max_age=3600,
    same_site="strict",
    https_only=(ENVIRONMENT == "production")
)
```

Arquivo `.env`:
```
SECRET_KEY=sua_chave_secreta_gerada_com_secrets_token_urlsafe_32
ENVIRONMENT=development
CSRF_SECRET_KEY=sua_outra_chave_secreta_para_csrf
```

Arquivo `.env.production`:
```
SECRET_KEY=chave_secreta_producao
ENVIRONMENT=production
CSRF_SECRET_KEY=chave_csrf_producao
```

---

## 10. DEPENDÊNCIAS ADICIONAIS NECESSÁRIAS

Adicionar ao `requirements.txt`:

```
python-dotenv==1.0.0
slowapi==0.1.9
fastapi-csrf-protect==0.3.4
```

Instalar:
```bash
pip install python-dotenv slowapi fastapi-csrf-protect
```

---

## 11. TESTES DE SEGURANÇA RECOMENDADOS

### 11.1. Testes Manuais

1. **Teste de Acesso Não Autorizado:**
   - Logout
   - Tentar acessar `/admin/listar_categorias`
   - Deve redirecionar para `/login`

2. **Teste de Escalonamento de Privilégios:**
   - Login como tutor
   - Tentar acessar `/admin/listar_categorias`
   - Deve retornar 403 Forbidden

3. **Teste de Force Brute:**
   - Tentar login com senha incorreta 10 vezes
   - Verificar se rate limiting bloqueia

### 11.2. Testes Automatizados

```python
# test_security.py
import pytest
from fastapi.testclient import TestClient

def test_admin_route_requires_auth():
    client = TestClient(app)
    response = client.get("/admin/listar_categorias")
    assert response.status_code == 303  # Redirect to login
    assert "/login" in response.headers["location"]

def test_admin_route_requires_admin_role():
    # Login como tutor
    client = TestClient(app)
    client.post("/login", data={"email": "tutor@test.com", "senha": "senha123"})

    # Tentar acessar rota admin
    response = client.get("/admin/listar_categorias")
    assert response.status_code == 403

def test_rate_limiting():
    client = TestClient(app)

    # Fazer 6 tentativas de login
    for _ in range(6):
        response = client.post("/login", data={"email": "test@test.com", "senha": "errada"})

    # 6ª tentativa deve ser bloqueada
    assert response.status_code == 429  # Too Many Requests
```

---

## 12. CONCLUSÃO

O sistema VetConecta apresenta **vulnerabilidades críticas de segurança** que colocam em risco:

- **Dados de usuários** (tutores, veterinários, administradores)
- **Conteúdo administrativo** (categorias, denúncias, verificações)
- **Conteúdo de veterinários** (artigos, estatísticas)
- **Conteúdo de tutores** (postagens de feed)

### Riscos Imediatos:
- ⚠️ Qualquer pessoa pode acessar e modificar dados administrativos
- ⚠️ Sessões são invalidadas a cada reinicialização do servidor
- ⚠️ Senhas fracas são aceitas (123456, etc.)
- ⚠️ Sem proteção contra ataques de força bruta
- ⚠️ Sem proteção CSRF

### Recomendação:
**NÃO COLOCAR EM PRODUÇÃO** até que pelo menos as vulnerabilidades CRÍTICAS sejam corrigidas (Fase 1 do Plano de Ação).

---

## 13. RECURSOS ADICIONAIS

### Documentação:
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security_warnings.html)

### Ferramentas de Análise:
- **Bandit** - Scanner de segurança para código Python
- **Safety** - Verifica vulnerabilidades em dependências
- **OWASP ZAP** - Teste de penetração automatizado

Comando para instalar ferramentas:
```bash
pip install bandit safety
bandit -r . -f json -o security_report.json
safety check
```

---

**FIM DA ANÁLISE**

Análise realizada em: 2025-10-15
Próxima análise recomendada: Após implementação das correções da Fase 1
