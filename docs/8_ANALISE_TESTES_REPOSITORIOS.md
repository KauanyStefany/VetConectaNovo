# Análise de Testes de Repositórios e Models - VetConecta

**Data:** 2025-10-15
**Responsável:** Análise Técnica Automatizada
**Versão:** 1.0

---

## Sumário Executivo

Esta análise avaliou a implementação dos testes de repositórios e models do projeto VetConecta, identificando problemas críticos de compatibilidade, cobertura e configuração. Foram encontrados **117 testes** distribuídos em 15 arquivos, porém **79,5% dos testes estão falhando** devido a incompatibilidades entre o código legado e a nova estrutura de models.

### Métricas Gerais

| Métrica | Valor |
|---------|-------|
| Total de Testes | 117 |
| Testes Aprovados | 23 (19.7%) |
| Testes Falhando | 56 (47.9%) |
| Testes com Erro | 38 (32.5%) |
| Arquivos de Teste | 15 |
| Linhas de Código de Teste | 2.926 |
| Repositórios Cobertos | 15/15 (100%) |

---

## 1. Estrutura de Testes Atual

### 1.1 Organização de Arquivos

```
VetConectaNovo/
├── pytest.ini                  # Configuração do pytest
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Fixtures compartilhadas
│   └── test_*_repo.py         # 15 arquivos de teste
└── .venv/                     # Ambiente virtual
```

### 1.2 Arquivos de Teste Identificados

| Arquivo | Linhas | Classes de Teste | Status |
|---------|--------|------------------|--------|
| test_administrador_repo.py | 102 | TestAdministradorRepo | Parcialmente falhando |
| test_categoria_artigo_repo.py | 206 | TestCategoriaArtigoRepo | Parcialmente falhando |
| test_chamado_repo.py | 266 | TestChamadoRepo | **Todos com erro** |
| test_comentario_repo.py | 87 | TestComentarioRepo | Parcialmente falhando |
| test_curtida_artigo_repo.py | 86 | TestCurtidaArtigoRepo | Parcialmente falhando |
| test_curtida_feed.py | 183 | TestCurtidaFeedRepo | Parcialmente falhando |
| test_denuncia_repo.py | 292 | TestDenunciaRepo | **Todos com erro** |
| test_postagem_artigo.py | 218 | TestPostagemArtigoRepo | Parcialmente falhando |
| test_postagem_feed.py | 47 | TestPostagemFeedRepo | Parcialmente falhando |
| test_resposta_chamado.py | 285 | TestRespostaChamadoRepo | Parcialmente falhando |
| test_seguida_repo.py | 228 | TestSeguidaRepo | Parcialmente falhando |
| test_tutor_repo.py | 272 | TestTutorRepo | Parcialmente falhando |
| test_usuario_repo.py | 217 | TestUsuarioRepo | Parcialmente falhando |
| test_verificacao_crmv_repo.py | 273 | TestVerificacaoCRMVRepo | **Todos com erro** |
| test_veterinario_repo.py | 164 | TestVeterinarioRepo | Parcialmente falhando |

---

## 2. Problemas Identificados

### 2.1 ⚠️ PROBLEMA CRÍTICO: Incompatibilidade de Models

**Severidade:** CRÍTICA
**Impacto:** 79.5% dos testes falhando

#### Descrição do Problema

Os testes importam models do diretório `model/`, mas esses models foram atualizados com **novos campos obrigatórios** que não existiam quando os testes foram escritos.

#### Exemplo: Model Usuario

**Model atual** (`model/usuario_model.py`):
```python
@dataclass
class Usuario:
    id_usuario: int
    nome: str
    email: str
    senha: str
    telefone: str
    perfil: str                      # NOVO CAMPO
    foto: Optional[str]              # NOVO CAMPO
    token_redefinicao: Optional[str] # NOVO CAMPO
    data_token: Optional[str]        # NOVO CAMPO
    data_cadastro: Optional[str]     # NOVO CAMPO
```

**Uso nos testes** (`tests/test_usuario_repo.py:26-32`):
```python
# ERRO: Faltam 5 argumentos obrigatórios
usuario_teste = Usuario(
    id_usuario=0,
    nome="João Silva",
    email="joao.silva@email.com",
    senha="senha123",
    telefone="11999998888"
)
```

**Erro resultante:**
```
TypeError: Usuario.__init__() missing 5 required positional arguments:
'perfil', 'foto', 'token_redefinicao', 'data_token', and 'data_cadastro'
```

#### Testes Afetados

- **test_chamado_repo.py:** 12 testes (100% com erro)
- **test_denuncia_repo.py:** 13 testes (100% com erro)
- **test_verificacao_crmv_repo.py:** 13 testes (100% com erro)
- **test_usuario_repo.py:** 13 testes (92% falhando)
- **test_tutor_repo.py:** 12 testes (75% falhando)
- **test_veterinario_repo.py:** 6 testes (83% falhando)

### 2.2 Ausência de Testes para Models

**Severidade:** ALTA
**Impacto:** Sem validação de regras de negócio dos models

#### Problema

Não existem testes unitários dedicados para validar os models. Os testes atuais apenas testam os repositórios (camada de persistência), mas não validam:

- Validações de campos dos dataclasses
- Transformações de dados
- Regras de negócio dos enums
- Comportamento de campos opcionais
- Serialização/deserialização

#### Models sem Testes Dedicados

1. `administrador_model.py`
2. `categoria_artigo_model.py`
3. `chamado_model.py`
4. `comentario_model.py`
5. `curtida_artigo_model.py`
6. `curtida_feed_model.py`
7. `denuncia_model.py`
8. `postagem_artigo_model.py`
9. `postagem_feed_model.py`
10. `resposta_chamado_model.py`
11. `seguida_model.py`
12. `tutor_model.py`
13. `usuario_model.py`
14. `verificacao_crmv_model.py`
15. `veterinario_model.py`
16. `enums.py` (ChamadoStatus, DenunciaStatus, VerificacaoStatus)

### 2.3 Problema de Importação: Código Legado vs Nova Estrutura

**Severidade:** ALTA
**Impacto:** Confusão entre duas estruturas de código

#### Estruturas Concorrentes

O projeto possui **duas estruturas de repositórios**:

1. **Estrutura Legada** (usada pelos testes):
   - Localização: `repo/`
   - Importação: `from repo.usuario_repo import *`
   - Conexão: `util/db_util.py`

2. **Nova Estrutura** (não testada):
   - Localização: `app/repositories/`
   - Importação: `from app.repositories.usuario_repo import ...`
   - Conexão: `app/db/connection.py`
   - Possui: `base_repository.py` (classe abstrata)

#### Problema

Os testes importam da estrutura **legada** (`repo/`), mas a aplicação principal pode estar usando a **nova estrutura** (`app/repositories/`). Isso significa:

- ❌ A nova estrutura não está sendo testada
- ❌ Mudanças no código novo não serão detectadas
- ❌ Código legado pode estar obsoleto mas continuará "testado"

### 2.4 Configuração do Conftest Comentada

**Severidade:** MÉDIA
**Impacto:** Código morto no repositório

**Arquivo:** `tests/conftest.py`

O arquivo possui 47 linhas, sendo que as primeiras 24 linhas (51%) estão **comentadas**, incluindo documentação importante sobre o que a fixture faz.

```python
# Linhas 1-24: COMENTADAS
# import pytest
# import os
# ...
# Fixture para criar um banco de dados temporário para testes
# @pytest.fixture
# def test_db():
# ...

# Linhas 27-47: CÓDIGO ATIVO (duplicado)
import os
import tempfile
import pytest

@pytest.fixture
def test_db():
    # Código duplicado do que está comentado acima
```

**Problema:** Código duplicado e falta de clareza sobre qual versão é a "oficial".

### 2.5 Falta de Testes para Métodos Adicionais dos Repositórios

**Severidade:** MÉDIA
**Impacto:** Métodos importantes sem cobertura

#### Métodos Não Testados no Usuario Repository

Analisando `app/repositories/usuario_repo.py` vs `tests/test_usuario_repo.py`:

**Métodos no repositório novo:**
- ✅ `criar_tabela_usuario()`
- ✅ `inserir_usuario()`
- ✅ `atualizar_usuario()`
- ✅ `atualizar_senha_usuario()`
- ✅ `excluir_usuario()`
- ✅ `obter_todos_usuarios_paginado()`
- ✅ `obter_usuario_por_id()`
- ❌ `obter_por_email()` - **NÃO TESTADO**
- ❌ `atualizar_token()` - **NÃO TESTADO**
- ❌ `obter_por_token()` - **NÃO TESTADO**
- ❌ `limpar_token()` - **NÃO TESTADO**
- ❌ `obter_todos_por_perfil()` - **NÃO TESTADO**
- ❌ `atualizar_foto()` - **NÃO TESTADO**

**Impacto:** Funcionalidades críticas como recuperação de senha (tokens) e busca por email não são testadas.

### 2.6 Falta de Testes de Integração

**Severidade:** MÉDIA
**Impacto:** Fluxos complexos não validados

Os testes atuais são majoritariamente **unitários** (testam um método por vez). Faltam testes de **integração** para validar:

- Fluxos completos de negócio (ex: usuário cria chamado → admin responde → usuário visualiza)
- Relacionamentos entre entidades (CASCADE, foreign keys)
- Transações complexas
- Concorrência e locks de banco

**Nota:** O `pytest.ini` define marcadores para `integration`, mas nenhum teste usa esse marcador.

### 2.7 Falta de Testes de Validação de Constraints do Banco

**Severidade:** MÉDIA
**Impacto:** Regras de integridade não validadas

Os testes não validam adequadamente:

- ✅ UNIQUE constraints (parcialmente testado em `test_usuario_repo.py:49`)
- ❌ FOREIGN KEY constraints
- ❌ CHECK constraints
- ❌ NOT NULL constraints (além dos obrigatórios do model)
- ❌ Valores padrão (DEFAULT)

**Exemplo:** Não há testes que verificam:
- O que acontece se inserir um chamado com `id_usuario` inexistente?
- O que acontece se excluir um usuário que tem chamados ativos?

### 2.8 Ausência de Relatório de Cobertura

**Severidade:** BAIXA
**Impacto:** Falta de métricas objetivas

Embora `pytest-cov` esteja instalado (`requirements.txt:24`), não há:

- Configuração de cobertura mínima no `pytest.ini`
- Scripts para gerar relatórios de cobertura
- Histórico de métricas de cobertura

### 2.9 Uso de Import * (Wildcard Imports)

**Severidade:** BAIXA
**Impacto:** Risco de conflitos de namespace

**Exemplo** (`tests/test_usuario_repo.py:2`):
```python
from repo.usuario_repo import *  # Importa TUDO
```

**Problemas:**
- Dificulta rastrear de onde vêm as funções
- Pode causar conflitos se houver nomes duplicados
- Viola PEP 8
- Dificulta análise estática (linters, IDEs)

---

## 3. Análise de Cobertura

### 3.1 Cobertura por Entidade

| Entidade | Repo Testado | Methods Cobertos | Taxa Estimada |
|----------|--------------|------------------|---------------|
| Administrador | ✅ | 5/7 | ~71% |
| Categoria Artigo | ✅ | 5/5 | 100% |
| Chamado | ✅ | 5/5 | 100% |
| Comentário | ✅ | 3/5 | ~60% |
| Curtida Artigo | ✅ | 3/5 | ~60% |
| Curtida Feed | ✅ | 4/6 | ~67% |
| Denúncia | ✅ | 5/5 | 100% |
| Postagem Artigo | ✅ | 5/7 | ~71% |
| Postagem Feed | ✅ | 2/5 | ~40% |
| Resposta Chamado | ✅ | 5/6 | ~83% |
| Seguida | ✅ | 4/5 | ~80% |
| Tutor | ✅ | 5/7 | ~71% |
| Usuário | ✅ | 7/13 | **54%** |
| Verificação CRMV | ✅ | 5/6 | ~83% |
| Veterinário | ✅ | 5/8 | ~63% |

**Cobertura média estimada de repositórios:** ~73%

### 3.2 Gaps de Cobertura por Categoria

#### Métodos Críticos Não Testados

1. **Autenticação e Segurança**
   - `usuario_repo.obter_por_email()` - usado no login
   - `usuario_repo.atualizar_token()` - recuperação de senha
   - `usuario_repo.obter_por_token()` - validação de token
   - `usuario_repo.limpar_token()` - segurança após uso

2. **Upload de Arquivos**
   - `usuario_repo.atualizar_foto()`
   - `veterinario_repo.atualizar_foto_perfil()`
   - `postagem_*_repo.atualizar_imagem()`

3. **Busca e Filtros**
   - `usuario_repo.obter_todos_por_perfil()` - filtragem por tipo
   - `chamado_repo.obter_por_status()`
   - `denuncia_repo.obter_por_status()`

4. **Estatísticas e Contagens**
   - Métodos de contagem (count)
   - Métodos de agregação
   - Relatórios

---

## 4. Análise de Configuração

### 4.1 pytest.ini

**Status:** ✅ Bem configurado

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
markers =
    slow: marca testes que demoram para executar
    integration: marca testes de integração
    unit: marca testes unitários
addopts =
    -v
    --strict-markers
    --disable-warnings
    --color=yes
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
```

**Pontos Positivos:**
- ✅ Padrões de nomenclatura bem definidos
- ✅ Marcadores para categorização
- ✅ Modo verbose habilitado
- ✅ Warnings filtrados

**Pontos de Melhoria:**
- ❌ Falta configuração de cobertura mínima
- ❌ Falta integração com CI/CD
- ❌ Não usa os marcadores definidos (slow, integration, unit)

### 4.2 conftest.py

**Status:** ⚠️ Funcional mas com problemas

**Pontos Positivos:**
- ✅ Fixture `test_db` cria banco temporário
- ✅ Usa `autouse=True` nos testes
- ✅ Cleanup automático

**Pontos Negativos:**
- ❌ 51% do arquivo está comentado
- ❌ Código duplicado
- ❌ Tratamento de exceção genérico (`except: pass`)
- ❌ Apenas uma fixture (poderia ter mais)

### 4.3 requirements.txt

**Status:** ✅ Completo

```txt
pytest
pytest-asyncio
pytest-cov
```

Todas as dependências necessárias para testes estão presentes.

---

## 5. Análise de Qualidade dos Testes

### 5.1 Padrões Seguidos ✅

1. **Padrão AAA (Arrange-Act-Assert)**
   ```python
   def test_inserir_usuario_sucesso(self, test_db):
       # Arrange
       usuario_teste = Usuario(...)

       # Act
       id_inserido = inserir_usuario(usuario_teste)

       # Assert
       assert id_inserido is not None
   ```

2. **Nomenclatura Clara**
   - `test_<acao>_<cenario>`
   - Ex: `test_inserir_usuario_sucesso`, `test_excluir_usuario_inexistente`

3. **Organização em Classes**
   - Uma classe por repositório: `TestUsuarioRepo`

4. **Documentação**
   - Docstrings em cada método de teste

5. **Isolamento**
   - Cada teste cria seus próprios dados
   - Banco temporário por sessão de teste

### 5.2 Problemas de Qualidade

#### 5.2.1 Asserts Insuficientes

**Exemplo** (`test_categoria_artigo_repo.py`):
```python
def test_inserir_categoria_sucesso(self, test_db):
    categoria = CategoriaArtigo(0, "Tecnologia", "Artigos sobre tech")
    id_inserido = inserir_categoria(categoria)

    # Apenas verifica se o ID existe
    assert id_inserido is not None
    assert id_inserido > 0

    # ❌ FALTANDO: Verificar se os dados foram salvos corretamente
    # categoria_db = obter_categoria_por_id(id_inserido)
    # assert categoria_db.nome == "Tecnologia"
    # assert categoria_db.descricao == "Artigos sobre tech"
```

#### 5.2.2 Falta de Testes de Casos Extremos

**Casos não testados:**
- Strings muito longas (SQL injection potencial)
- Caracteres especiais (Unicode, emojis)
- Valores negativos onde não deveria
- Valores nulos em campos opcionais
- Listas vazias vs None
- Timestamps no passado/futuro

#### 5.2.3 Falta de Testes de Desempenho

Não há testes marcados com `@pytest.mark.slow` verificando:
- Performance de paginação com grandes volumes
- Queries com muitos JOINs
- Operações em lote (bulk operations)

#### 5.2.4 Ausência de Testes Parametrizados

Oportunidade perdida de usar `@pytest.mark.parametrize`:

```python
# Atual: 3 testes separados
def test_status_aberto(...): ...
def test_status_em_andamento(...): ...
def test_status_resolvido(...): ...

# Ideal: 1 teste parametrizado
@pytest.mark.parametrize("status", [
    ChamadoStatus.ABERTO,
    ChamadoStatus.EM_ANDAMENTO,
    ChamadoStatus.RESOLVIDO
])
def test_todos_status(status): ...
```

---

## 6. Propostas de Solução

### 6.1 PRIORIDADE 1 - CRÍTICA: Corrigir Incompatibilidade de Models

**Objetivo:** Fazer todos os testes passarem

#### Solução 1A: Atualizar Testes para Usar Novos Campos (RECOMENDADA)

**Ação:**
1. Atualizar todos os testes para incluir os novos campos obrigatórios
2. Usar valores padrão sensatos para testes

**Exemplo de mudança** (`test_usuario_repo.py`):

```python
# ANTES (quebrado)
usuario = Usuario(0, "João Silva", "joao@email.com", "senha123", "11999998888")

# DEPOIS (correto)
usuario = Usuario(
    id_usuario=0,
    nome="João Silva",
    email="joao@email.com",
    senha="senha123",
    telefone="11999998888",
    perfil="tutor",              # NOVO
    foto=None,                   # NOVO
    token_redefinicao=None,      # NOVO
    data_token=None,             # NOVO
    data_cadastro=None           # NOVO
)
```

**Esforço:** Médio (15 arquivos, ~80 ocorrências)
**Benefício:** Todos os testes voltam a funcionar
**Risco:** Baixo

#### Solução 1B: Criar Fixtures de Models (COMPLEMENTAR)

**Ação:**
Adicionar fixtures no `conftest.py` para criar instances padrão de cada model:

```python
# tests/conftest.py

@pytest.fixture
def usuario_padrao():
    """Cria um usuário padrão para testes"""
    return Usuario(
        id_usuario=0,
        nome="João Test",
        email="teste@email.com",
        senha="senha123",
        telefone="11999999999",
        perfil="tutor",
        foto=None,
        token_redefinicao=None,
        data_token=None,
        data_cadastro=None
    )

@pytest.fixture
def admin_padrao():
    """Cria um administrador padrão para testes"""
    return Administrador(...)
```

**Uso nos testes:**
```python
def test_inserir_usuario(self, test_db, usuario_padrao):
    # Arrange - já pronto!

    # Act
    id_inserido = inserir_usuario(usuario_padrao)

    # Assert
    assert id_inserido > 0
```

**Esforço:** Baixo
**Benefício:** Testes mais limpos e DRY
**Risco:** Nenhum

#### Solução 1C: Tornar Campos Opcionais nos Models (NÃO RECOMENDADA)

**Ação:**
Mudar os novos campos para `Optional` com valores default:

```python
@dataclass
class Usuario:
    # ... campos existentes ...
    perfil: str = "tutor"                      # Com default
    foto: Optional[str] = None                 # Já é opcional
    token_redefinicao: Optional[str] = None    # Já é opcional
    data_token: Optional[str] = None           # Já é opcional
    data_cadastro: Optional[str] = None        # Já é opcional
```

**Esforço:** Muito baixo
**Benefício:** Testes funcionam sem mudanças
**Risco:** ⚠️ ALTO - Pode quebrar lógica de negócio se esses campos são realmente obrigatórios

### 6.2 PRIORIDADE 2 - ALTA: Criar Testes para Models

**Objetivo:** Validar regras de negócio dos models

#### Ação: Criar Arquivos de Teste para Models

**Nova estrutura:**
```
tests/
├── test_repositories/     # Mover testes atuais
│   ├── test_usuario_repo.py
│   ├── test_chamado_repo.py
│   └── ...
└── test_models/          # NOVO - testes de models
    ├── test_usuario_model.py
    ├── test_chamado_model.py
    ├── test_enums.py
    └── ...
```

**Exemplo** (`tests/test_models/test_usuario_model.py`):

```python
import pytest
from model.usuario_model import Usuario

class TestUsuarioModel:
    """Testes para o model Usuario"""

    def test_criar_usuario_valido(self):
        """Testa criação de usuário com dados válidos"""
        usuario = Usuario(
            id_usuario=1,
            nome="João Silva",
            email="joao@email.com",
            senha="senha123",
            telefone="11999999999",
            perfil="tutor",
            foto=None,
            token_redefinicao=None,
            data_token=None,
            data_cadastro="2024-01-01"
        )

        assert usuario.id_usuario == 1
        assert usuario.nome == "João Silva"
        assert usuario.perfil == "tutor"

    def test_usuario_campos_opcionais(self):
        """Testa que campos opcionais podem ser None"""
        usuario = Usuario(
            id_usuario=1,
            nome="Maria",
            email="maria@email.com",
            senha="senha",
            telefone="11888888888",
            perfil="veterinario",
            foto=None,          # Opcional
            token_redefinicao=None,  # Opcional
            data_token=None,         # Opcional
            data_cadastro=None       # Opcional
        )

        assert usuario.foto is None
        assert usuario.token_redefinicao is None

    @pytest.mark.parametrize("perfil_valido", [
        "tutor",
        "veterinario",
        "administrador"
    ])
    def test_perfis_validos(self, perfil_valido):
        """Testa que todos os perfis válidos funcionam"""
        usuario = Usuario(
            id_usuario=1,
            nome="Teste",
            email="test@email.com",
            senha="senha",
            telefone="11000000000",
            perfil=perfil_valido,
            foto=None,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None
        )

        assert usuario.perfil == perfil_valido
```

**Exemplo** (`tests/test_models/test_enums.py`):

```python
import pytest
from model.enums import ChamadoStatus, DenunciaStatus, VerificacaoStatus

class TestEnums:
    """Testes para os enums do sistema"""

    def test_chamado_status_valores(self):
        """Testa valores do enum ChamadoStatus"""
        assert ChamadoStatus.ABERTO.value == "aberto"
        assert ChamadoStatus.EM_ANDAMENTO.value == "em_andamento"
        assert ChamadoStatus.RESOLVIDO.value == "resolvido"

    def test_chamado_status_comparacao(self):
        """Testa comparação entre status"""
        status1 = ChamadoStatus.ABERTO
        status2 = ChamadoStatus.ABERTO
        status3 = ChamadoStatus.RESOLVIDO

        assert status1 == status2
        assert status1 != status3

    def test_denuncia_status_completo(self):
        """Testa todos os status de denúncia"""
        assert len(DenunciaStatus) == 4
        assert "PENDENTE" in DenunciaStatus.__members__
        assert "EM_ANALISE" in DenunciaStatus.__members__
        assert "RESOLVIDA" in DenunciaStatus.__members__
        assert "REJEITADA" in DenunciaStatus.__members__
```

**Esforço:** Médio (2-3 dias)
**Benefício:** Validação completa de regras de negócio
**Risco:** Nenhum

### 6.3 PRIORIDADE 3 - ALTA: Consolidar Estrutura de Código

**Objetivo:** Eliminar duplicação entre `repo/` e `app/repositories/`

#### Opção A: Deprecar Estrutura Legada (RECOMENDADA)

**Ação:**
1. Migrar todos os testes para usar `app/repositories/`
2. Marcar `repo/` como deprecated
3. Remover `repo/` em versão futura

**Mudança nos testes:**
```python
# ANTES
from repo.usuario_repo import *

# DEPOIS
from app.repositories.usuario_repo import (
    criar_tabela_usuario,
    inserir_usuario,
    atualizar_usuario,
    # ... importações explícitas
)
```

**Esforço:** Médio (15 arquivos)
**Benefício:** Código unificado, menos confusão
**Risco:** Médio (pode quebrar outros códigos que usam `repo/`)

#### Opção B: Manter Ambas, Testar Ambas (NÃO RECOMENDADA)

**Ação:**
Criar testes duplicados para cada estrutura.

**Esforço:** Alto
**Benefício:** Baixo
**Risco:** Alto (duplicação de esforço)

### 6.4 PRIORIDADE 4 - MÉDIA: Adicionar Testes Faltantes

**Objetivo:** Aumentar cobertura para 90%+

#### 4A: Adicionar Testes para Métodos Não Cobertos

**Lista de prioridades:**

**ALTA PRIORIDADE:**
1. `usuario_repo.obter_por_email()` - usado no login
2. `usuario_repo.atualizar_token()` - recuperação de senha
3. `usuario_repo.obter_por_token()` - validação de token

**MÉDIA PRIORIDADE:**
4. `usuario_repo.limpar_token()`
5. `usuario_repo.obter_todos_por_perfil()`
6. `usuario_repo.atualizar_foto()`
7. Métodos similares em outros repositórios

**Exemplo de teste a adicionar:**

```python
# tests/test_repositories/test_usuario_repo.py

def test_obter_usuario_por_email_existente(self, test_db, usuario_padrao):
    """Testa busca de usuário por email existente"""
    # Arrange
    id_usuario = inserir_usuario(usuario_padrao)

    # Act
    usuario_db = obter_por_email(usuario_padrao.email)

    # Assert
    assert usuario_db is not None, "Usuário deveria ser encontrado"
    assert usuario_db.id_usuario == id_usuario
    assert usuario_db.email == usuario_padrao.email
    assert usuario_db.nome == usuario_padrao.nome

def test_obter_usuario_por_email_inexistente(self, test_db):
    """Testa busca de usuário por email inexistente"""
    # Act
    usuario = obter_por_email("naoexiste@email.com")

    # Assert
    assert usuario is None, "Não deveria encontrar usuário"

def test_obter_usuario_por_email_vazio(self, test_db):
    """Testa busca com email vazio"""
    # Act
    usuario = obter_por_email("")

    # Assert
    assert usuario is None

def test_obter_usuario_por_email_case_insensitive(self, test_db, usuario_padrao):
    """Testa se busca por email é case-insensitive"""
    # Arrange
    inserir_usuario(usuario_padrao)

    # Act
    usuario1 = obter_por_email(usuario_padrao.email.upper())
    usuario2 = obter_por_email(usuario_padrao.email.lower())

    # Assert
    # Depende da implementação - documentar comportamento esperado
    # Se for case-sensitive, ambos devem ser None (exceto o exato)
    # Se for case-insensitive, ambos devem encontrar o usuário
```

#### 4B: Adicionar Testes de Constraints

```python
def test_inserir_usuario_com_fk_invalida(self, test_db):
    """Testa inserção com foreign key inválida"""
    # Arrange - depende de como as FKs estão modeladas
    # Por exemplo, se Tutor tem FK para Usuario

    tutor = Tutor(
        id_tutor=0,
        id_usuario=9999,  # Usuário inexistente
        pets="Rex, Miau"
    )

    # Act & Assert
    with pytest.raises(Exception):  # IntegrityError ou similar
        inserir_tutor(tutor)

def test_excluir_usuario_com_dependencias(self, test_db):
    """Testa exclusão de usuário que tem dependências"""
    # Arrange
    id_usuario = inserir_usuario(usuario_padrao)

    # Criar um chamado para esse usuário
    chamado = Chamado(
        id_chamado=0,
        id_usuario=id_usuario,
        titulo="Teste",
        descricao="Descrição",
        status=ChamadoStatus.ABERTO,
        data=datetime.now()
    )
    inserir_chamado(chamado)

    # Act & Assert
    # Depende da configuração: CASCADE delete ou RESTRICT?
    resultado = excluir_usuario(id_usuario)

    # Se for CASCADE: usuário e chamado são excluídos
    # Se for RESTRICT: deve falhar
    # Documentar comportamento esperado
```

#### 4C: Adicionar Testes Parametrizados

```python
@pytest.mark.parametrize("status_inicial,status_final,esperado", [
    (ChamadoStatus.ABERTO, ChamadoStatus.EM_ANDAMENTO, True),
    (ChamadoStatus.EM_ANDAMENTO, ChamadoStatus.RESOLVIDO, True),
    (ChamadoStatus.RESOLVIDO, ChamadoStatus.ABERTO, True),  # Reabrir
    # Adicionar mais transições conforme regras de negócio
])
def test_transicoes_status_chamado(self, test_db, status_inicial, status_final, esperado):
    """Testa transições válidas de status"""
    # Arrange
    chamado = criar_chamado_com_status(status_inicial)

    # Act
    resultado = atualizar_status_chamado(chamado.id, status_final)

    # Assert
    assert resultado == esperado
```

**Esforço:** Alto (1 semana)
**Benefício:** Cobertura 90%+
**Risco:** Baixo

### 6.5 PRIORIDADE 5 - MÉDIA: Limpar Conftest

**Objetivo:** Remover código morto e melhorar fixtures

#### Ação:

```python
# tests/conftest.py - VERSÃO LIMPA

"""
Fixtures compartilhadas para os testes do VetConecta.

Este arquivo contém fixtures que são automaticamente disponibilizadas
para todos os testes do projeto.
"""

import os
import tempfile
import pytest
from datetime import datetime

from model.usuario_model import Usuario
from model.administrador_model import Administrador
from model.enums import ChamadoStatus, DenunciaStatus, VerificacaoStatus


@pytest.fixture
def test_db():
    """
    Cria um banco de dados SQLite temporário para testes.

    O banco é criado antes de cada teste e destruído após,
    garantindo isolamento completo entre testes.

    Yields:
        str: Caminho para o arquivo de banco de dados temporário
    """
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.environ['TEST_DATABASE_PATH'] = db_path

    try:
        yield db_path
    finally:
        try:
            os.close(db_fd)
        except OSError:
            pass  # Já foi fechado

        try:
            os.remove(db_path)
        except (PermissionError, FileNotFoundError):
            # Em Windows, o arquivo pode estar bloqueado
            pass


@pytest.fixture
def usuario_padrao():
    """
    Cria uma instância padrão de Usuario para testes.

    Returns:
        Usuario: Objeto Usuario com dados de teste
    """
    return Usuario(
        id_usuario=0,
        nome="João Test",
        email="joao.test@vetconecta.com",
        senha="senha_segura_123",
        telefone="11999999999",
        perfil="tutor",
        foto=None,
        token_redefinicao=None,
        data_token=None,
        data_cadastro=None
    )


@pytest.fixture
def veterinario_padrao():
    """
    Cria uma instância padrão de Veterinário para testes.

    Returns:
        Usuario: Objeto Usuario com perfil veterinário
    """
    return Usuario(
        id_usuario=0,
        nome="Dra. Maria Veterinária",
        email="maria.vet@vetconecta.com",
        senha="senha_segura_456",
        telefone="11888888888",
        perfil="veterinario",
        foto=None,
        token_redefinicao=None,
        data_token=None,
        data_cadastro=None
    )


@pytest.fixture
def admin_padrao():
    """
    Cria uma instância padrão de Administrador para testes.

    Returns:
        Administrador: Objeto Administrador com dados de teste
    """
    return Administrador(
        id_administrador=0,
        nome="Admin Test",
        email="admin@vetconecta.com",
        senha="admin_senha_789"
    )


@pytest.fixture
def data_atual():
    """
    Retorna a data/hora atual para testes.

    Returns:
        datetime: Data/hora atual
    """
    return datetime.now()
```

**Esforço:** Baixo (1-2 horas)
**Benefício:** Código mais limpo, fixtures reutilizáveis
**Risco:** Nenhum

### 6.6 PRIORIDADE 6 - MÉDIA: Configurar Cobertura de Código

**Objetivo:** Monitorar cobertura automaticamente

#### Ação: Atualizar pytest.ini

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*

markers =
    slow: marca testes que demoram para executar
    integration: marca testes de integração
    unit: marca testes unitários
    smoke: testes básicos de sanidade

addopts =
    -v
    --strict-markers
    --disable-warnings
    --color=yes
    --cov=repo
    --cov=app/repositories
    --cov=model
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80

filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
```

#### Criar Script de Teste com Cobertura

```bash
#!/bin/bash
# scripts/run_tests_with_coverage.sh

echo "Executando testes com cobertura..."

# Limpar cobertura anterior
rm -rf htmlcov/
rm -f .coverage

# Executar testes
pytest

# Abrir relatório
if [ $? -eq 0 ]; then
    echo "✅ Todos os testes passaram!"
    echo "📊 Relatório de cobertura: htmlcov/index.html"
    open htmlcov/index.html  # macOS
    # xdg-open htmlcov/index.html  # Linux
else
    echo "❌ Alguns testes falharam"
    exit 1
fi
```

**Esforço:** Baixo (1 hora)
**Benefício:** Visibilidade contínua da cobertura
**Risco:** Nenhum

### 6.7 PRIORIDADE 7 - BAIXA: Substituir Import *

**Objetivo:** Melhorar qualidade do código

#### Ação: Usar Importações Explícitas

```python
# ANTES
from repo.usuario_repo import *

# DEPOIS
from repo.usuario_repo import (
    criar_tabela_usuario,
    inserir_usuario,
    atualizar_usuario,
    atualizar_senha_usuario,
    excluir_usuario,
    obter_todos_usuarios_paginado,
    obter_usuario_por_id,
)
```

**Benefício:**
- ✅ Código mais limpo
- ✅ Melhor suporte de IDEs
- ✅ Evita conflitos de namespace
- ✅ Mais fácil de refatorar

**Esforço:** Baixo (pode ser automatizado)
**Risco:** Nenhum

### 6.8 PRIORIDADE 8 - BAIXA: Adicionar Testes de Integração

**Objetivo:** Validar fluxos completos

#### Exemplo de Teste de Integração

```python
# tests/test_integration/test_fluxo_chamado_completo.py

@pytest.mark.integration
class TestFluxoChamadoCompleto:
    """
    Testes de integração para o fluxo completo de chamados.

    Valida o ciclo de vida completo:
    1. Usuário cria chamado
    2. Admin visualiza e aceita
    3. Admin responde
    4. Usuário visualiza resposta
    5. Chamado é resolvido
    """

    @pytest.fixture(autouse=True)
    def setup(self, test_db):
        """Setup para testes de integração"""
        # Criar todas as tabelas necessárias
        criar_tabela_usuario()
        criar_tabela_administrador()
        criar_tabela_chamado()
        criar_tabela_resposta_chamado()

        # Criar dados base
        self.usuario = Usuario(...)
        self.id_usuario = inserir_usuario(self.usuario)

        self.admin = Administrador(...)
        self.id_admin = inserir_administrador(self.admin)

    def test_fluxo_completo_sucesso(self, test_db):
        """Testa fluxo completo de chamado com sucesso"""
        # 1. Usuário cria chamado
        chamado = Chamado(
            id_chamado=0,
            id_usuario=self.id_usuario,
            id_admin=None,  # Ainda não atribuído
            titulo="Problema com login",
            descricao="Não consigo fazer login no sistema",
            status=ChamadoStatus.ABERTO,
            data=datetime.now()
        )
        id_chamado = inserir_chamado(chamado)
        assert id_chamado is not None

        # 2. Admin visualiza e aceita
        chamados_abertos = obter_chamados_por_status(ChamadoStatus.ABERTO)
        assert len(chamados_abertos) == 1
        assert chamados_abertos[0].id_chamado == id_chamado

        # 3. Admin atualiza status para "em andamento"
        atualizar_status_chamado(id_chamado, ChamadoStatus.EM_ANDAMENTO)
        chamado_db = obter_chamado_por_id(id_chamado)
        assert chamado_db.status == ChamadoStatus.EM_ANDAMENTO

        # 4. Admin cria resposta
        resposta = RespostaChamado(
            id_resposta=0,
            id_chamado=id_chamado,
            id_admin=self.id_admin,
            mensagem="Tente resetar sua senha usando o link 'Esqueci minha senha'",
            data=datetime.now()
        )
        id_resposta = inserir_resposta_chamado(resposta)
        assert id_resposta is not None

        # 5. Usuário visualiza resposta
        respostas = obter_respostas_por_chamado(id_chamado)
        assert len(respostas) == 1
        assert respostas[0].mensagem == resposta.mensagem

        # 6. Admin marca como resolvido
        atualizar_status_chamado(id_chamado, ChamadoStatus.RESOLVIDO)
        chamado_final = obter_chamado_por_id(id_chamado)
        assert chamado_final.status == ChamadoStatus.RESOLVIDO

        # Validações finais
        assert chamado_final.id_usuario == self.id_usuario
        assert chamado_final.titulo == "Problema com login"
```

**Esforço:** Médio
**Benefício:** Validação de fluxos críticos
**Risco:** Baixo

---

## 7. Plano de Ação Recomendado

### Fase 1: Estabilização (Semana 1)

**Objetivo:** Fazer todos os testes passarem

| Tarefa | Prioridade | Esforço | Responsável |
|--------|-----------|---------|-------------|
| Atualizar testes para novos campos do Model | P1 | 2 dias | Dev Backend |
| Criar fixtures no conftest | P1 | 4 horas | Dev Backend |
| Executar testes e validar sucesso | P1 | 2 horas | QA |

**Meta:** 100% dos testes passando

### Fase 2: Expansão (Semanas 2-3)

**Objetivo:** Aumentar cobertura e qualidade

| Tarefa | Prioridade | Esforço | Responsável |
|--------|-----------|---------|-------------|
| Criar testes para models | P2 | 2 dias | Dev Backend |
| Adicionar testes para métodos não cobertos | P4 | 3 dias | Dev Backend |
| Configurar relatório de cobertura | P6 | 4 horas | DevOps |
| Limpar conftest e remover código morto | P5 | 2 horas | Dev Backend |

**Meta:** 85% de cobertura

### Fase 3: Consolidação (Semana 4)

**Objetivo:** Unificar estrutura e melhorar organização

| Tarefa | Prioridade | Esforço | Responsável |
|--------|-----------|---------|-------------|
| Migrar testes para app/repositories/ | P3 | 1 dia | Dev Backend |
| Deprecar estrutura legada repo/ | P3 | 2 horas | Tech Lead |
| Substituir import * por explícitos | P7 | 4 horas | Dev Backend |
| Adicionar testes de integração | P8 | 2 dias | Dev Backend |

**Meta:** Código consolidado e organizado

### Fase 4: Melhoria Contínua (Ongoing)

**Objetivo:** Manter qualidade

| Tarefa | Prioridade | Esforço | Responsável |
|--------|-----------|---------|-------------|
| Code review obrigatório com testes | - | Contínuo | Toda equipe |
| Monitorar cobertura (não cair abaixo de 80%) | - | Contínuo | CI/CD |
| Adicionar testes para novos features | - | Contínuo | Dev Backend |

---

## 8. Métricas de Sucesso

### 8.1 Métricas Quantitativas

| Métrica | Atual | Meta Fase 1 | Meta Fase 2 | Meta Fase 3 |
|---------|-------|-------------|-------------|-------------|
| Testes Passando | 19.7% | 100% | 100% | 100% |
| Cobertura de Código | ~73% | ~73% | 85% | 90% |
| Testes Totais | 117 | 117 | 180 | 220 |
| Testes de Models | 0 | 0 | 50 | 50 |
| Testes de Integração | 0 | 0 | 5 | 15 |
| Tempo de Execução | 0.18s | < 1s | < 3s | < 5s |

### 8.2 Métricas Qualitativas

- ✅ Todos os testes passam consistentemente
- ✅ Testes são fáceis de entender e manter
- ✅ Nova funcionalidade sempre vem com testes
- ✅ Bugs encontrados ganham testes de regressão
- ✅ Documentação dos testes está atualizada
- ✅ CI/CD falha se cobertura cair

---

## 9. Riscos e Mitigações

### 9.1 Riscos Técnicos

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Mudanças nos models quebram testes | Média | Alto | Fixtures centralizadas, testes bem isolados |
| Performance degradada com mais testes | Baixa | Médio | Usar marcadores (@pytest.mark.slow) |
| Conflitos entre estruturas legada e nova | Alta | Alto | Consolidar em uma estrutura única (Fase 3) |
| Testes flaky (instáveis) | Média | Alto | Isolamento adequado, evitar dependências temporais |

### 9.2 Riscos de Processo

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Desenvolvedores não escreverem testes | Média | Alto | Code review obrigatório, CI/CD |
| Falta de tempo para implementar melhorias | Alta | Médio | Priorizar Fase 1, demais fases incrementais |
| Resistência a mudanças | Baixa | Médio | Mostrar benefícios com métricas |

---

## 10. Conclusão

### 10.1 Resumo dos Achados

O projeto VetConecta possui uma **base sólida de testes**, com 15 arquivos e 117 casos de teste cobrindo todos os 15 repositórios. A estrutura está bem organizada com pytest e segue boas práticas como o padrão AAA e isolamento de testes.

Porém, **79.5% dos testes estão falhando** devido a um problema crítico: incompatibilidade entre os testes (escritos para models antigos) e os models atuais (que ganharam novos campos obrigatórios). Este é um problema de **dívida técnica** que precisa ser endereçado com urgência.

Além disso, há **gaps importantes de cobertura**:
- ❌ Nenhum teste dedicado para models
- ❌ Métodos críticos sem cobertura (autenticação, tokens, uploads)
- ❌ Sem testes de integração
- ❌ Duplicação de código (repo/ vs app/repositories/)

### 10.2 Próximos Passos Imediatos

**SEMANA 1 - CRÍTICO:**

1. ✅ **Aprovar este documento** com stakeholders
2. 🔧 **Corrigir incompatibilidade** de models (Solução 6.1)
3. ✅ **Validar** que todos os 117 testes passam
4. 📊 **Gerar relatório** de cobertura baseline

**SEMANA 2-4 - IMPORTANTE:**

5. 📝 **Adicionar testes** para models (Solução 6.2)
6. 🔍 **Aumentar cobertura** para métodos faltantes (Solução 6.4)
7. 🏗️ **Consolidar estrutura** de código (Solução 6.3)

### 10.3 Benefícios Esperados

Ao implementar as soluções propostas, o projeto terá:

- ✅ **Confiabilidade:** 100% dos testes passando
- ✅ **Cobertura:** 90%+ de cobertura de código
- ✅ **Qualidade:** Testes para models, repositórios e integrações
- ✅ **Manutenibilidade:** Código consolidado e bem organizado
- ✅ **Produtividade:** Menos bugs em produção, mais confiança para refatorar
- ✅ **Documentação:** Testes servem como documentação viva do código

---

## 11. Anexos

### 11.1 Comandos Úteis

```bash
# Executar todos os testes
.venv/bin/python -m pytest tests/ -v

# Executar com cobertura
.venv/bin/python -m pytest tests/ --cov=repo --cov=model --cov-report=html

# Executar apenas testes unitários
.venv/bin/python -m pytest tests/ -m unit

# Executar apenas testes de integração
.venv/bin/python -m pytest tests/ -m integration

# Executar testes de um arquivo específico
.venv/bin/python -m pytest tests/test_usuario_repo.py -v

# Executar um teste específico
.venv/bin/python -m pytest tests/test_usuario_repo.py::TestUsuarioRepo::test_inserir_usuario_sucesso -v

# Ver testes que falharam
.venv/bin/python -m pytest tests/ --lf  # last failed

# Modo watch (reexecutar ao salvar)
.venv/bin/python -m pytest tests/ --watch
```

### 11.2 Recursos e Referências

**Pytest:**
- [Documentação Oficial](https://docs.pytest.org/)
- [Fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [Parametrize](https://docs.pytest.org/en/stable/parametrize.html)

**Cobertura:**
- [pytest-cov](https://pytest-cov.readthedocs.io/)
- [Coverage.py](https://coverage.readthedocs.io/)

**Boas Práticas:**
- [Testing Best Practices - Python](https://realpython.com/python-testing/)
- [AAA Pattern](https://wiki.c2.com/?ArrangeActAssert)

### 11.3 Glossário

- **AAA:** Arrange-Act-Assert (padrão de organização de testes)
- **Fixture:** Função que fornece dados ou configuração para testes
- **Mock:** Objeto falso usado para simular dependências
- **Stub:** Versão simplificada de um componente para testes
- **Coverage:** Percentual do código executado pelos testes
- **Flaky Test:** Teste que às vezes passa e às vezes falha
- **Integration Test:** Teste que valida múltiplos componentes juntos
- **Unit Test:** Teste que valida uma unidade isolada
- **Smoke Test:** Teste básico de sanidade

---

**Documento gerado em:** 2025-10-15
**Última atualização:** 2025-10-15
**Versão:** 1.0
**Status:** Aguardando aprovação
