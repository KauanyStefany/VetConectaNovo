# .gitignore

```
# Ambiente virtual
.venv/
env/
venv/
ENV/

# Bytecode compilado
__pycache__/
*.py[cod]
*$py.class

# Logs
*.log

# Arquivos temporários do sistema
*.swp
*.swo
*.bak
*.tmp
*.DS_Store
Thumbs.db

# Arquivos de packaging e distribuição
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
# Veja https://pyinstaller.org/en/stable/usage.html
*.manifest
*.spec

# Rodas
*.whl

# Pytest cache
.pytest_cache/

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover

# Cython build
cython_debug/

# Jupyter Notebook checkpoints
.ipynb_checkpoints

# VS Code
.vscode/

# Arquivos de configuração do PyCharm
.idea/

# Arquivos de configuração do Visual Studio
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?

```

# .vscode\settings.json

```json
{
    "python.testing.pytestArgs": [
        "tests"
    ],
    "python.testing.unittestEnabled": false,
    "python.testing.pytestEnabled": true
}
```

# dados.db

This is a binary file of the type: Binary

# data\administrador_model.py

```py
from dataclasses import dataclass

@dataclass
class Administrador:
    id_admin: int
    nome: str
    email: str
    senha: str
    
```

# data\administrador_repo.py

```py
from typing import Any, Optional, List
from data.administrador_model import Administrador
from data.administrador_sql import *
from util import get_connection


def criar_tabela_administrador() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de administrador: {e}")
        return False

def inserir_administrador(admin: Administrador) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (admin.nome, admin.email, admin.senha))
        return cursor.lastrowid


def atualizar_administrador(admin: Administrador) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (admin.nome, admin.email, admin.senha, admin.id_admin))
        return cursor.rowcount > 0
    
def atualizar_senha(id_admin: int, nova_senha: str) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_SENHA, (nova_senha, id_admin))
        return cursor.rowcount > 0

def excluir_administrador(id_admin: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_admin,))
        return cursor.rowcount > 0


def obter_administradores_paginado(offset: int, limite: int) -> List[Administrador]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_ADMINISTRADORES_PAGINADO, (limite, offset))
        rows = cursor.fetchall()
        return [Administrador(**row) for row in rows]


def obter_administrador_por_id(id_admin: int) -> Optional[Administrador]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_admin,))
        row = cursor.fetchone()
        return Administrador(**row) if row else None
```

# data\administrador_sql.py

```py
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS administrador (
    id_admin INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha CHAR(8) NOT NULL
);
"""

INSERIR = """
INSERT INTO administrador (nome, email, senha )
VALUES (?, ?, ?);
"""

ATUALIZAR = """
UPDATE administrador 
SET nome = ?, email = ?, senha = ?
WHERE id_admin = ?;
"""

ATUALIZAR_SENHA = """
UPDATE administrador
SET senha = ?
WHERE id_admin = ?;
"""

EXCLUIR = """
DELETE FROM administrador 
WHERE id_admin = ?;
"""

OBTER_ADMINISTRADORES_PAGINADO = """
SELECT * 
FROM administrador 
ORDER BY id_admin
LIMIT ? OFFSET ?;
"""

OBTER_POR_ID = """
SELECT * 
FROM administrador 
WHERE id_admin = ?;
"""

```

# data\categoria_artigo_model.py

```py
from dataclasses import dataclass

@dataclass
class CategoriaArtigo:
    id: int
    nome: str
    descricao: str | None  # campo opcional

```

# data\categoria_artigo_repo.py

```py
from typing import Optional, List
from data.categoria_artigo_model import CategoriaArtigo
from data.categoria_artigo_sql import *
from util import get_connection


def criar_tabela_categoria_artigo() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de categorias: {e}")
        return False


def inserir_categoria(categoria: CategoriaArtigo) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (categoria.nome, categoria.descricao))
        return cursor.lastrowid


def atualizar_categoria(categoria: CategoriaArtigo) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (categoria.nome, categoria.descricao, categoria.id))
        return cursor.rowcount > 0


def excluir_categoria(id_categoria: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_categoria,))
        return cursor.rowcount > 0


def obter_categorias_paginado(offset: int, limite: int) -> List[CategoriaArtigo]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS_PAGINADO, (limite, offset))
        rows = cursor.fetchall()
        return [CategoriaArtigo(**row) for row in rows]
    

def obter_categoria_por_id(id_categoria: int) -> Optional[CategoriaArtigo]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_categoria,))
        row = cursor.fetchone()
        return CategoriaArtigo(**row) if row else None

```

# data\categoria_artigo_sql.py

```py
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS categoria_artigo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT
);
"""
INSERIR = """
INSERT INTO categoria_artigo (nome, descricao)
VALUES (?, ?);
"""
ATUALIZAR = """
UPDATE categoria_artigo SET nome = ?, descricao = ?
WHERE id = ?;
"""
EXCLUIR = """
DELETE FROM categoria_artigo 
WHERE id = ?;
"""
OBTER_TODOS_PAGINADO = """
SELECT * 
FROM categoria_artigo 
ORDER BY nome
LIMIT ? OFFSET ?;
"""

OBTER_POR_ID = """
SELECT * 
FROM categoria_artigo 
WHERE id = ?;
"""


```

# data\chamado_model.py

```py
from dataclasses import dataclass

@dataclass
class Chamado:
    id: int
    id_usuario: int
    id_admin: int
    titulo: str
    descricao: str
    status: str  # valores possíveis: 'aberto', 'em andamento', 'resolvido'
    data: str  # formato DATE

```

# data\chamado_repo.py

```py
from typing import Optional, List
from data.chamado_model import Chamado
from data.chamado_sql import *
from util import get_connection


def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de categorias: {e}")
        return False


def inserir_chamado(chamado: Chamado) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            chamado.id_usuario,
            chamado.id_admin,
            chamado.titulo,
            chamado.descricao,
            chamado.status,
            chamado.data
        ))
        return cursor.lastrowid


def atualizar_status_chamado(id_chamado: int, novo_status: str) -> bool:
    if novo_status not in ['aberto', 'em andamento', 'resolvido']:
        raise ValueError("Status inválido. Use: 'aberto', 'em andamento' ou 'resolvido'.")

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (novo_status, id_chamado))
        return cursor.rowcount > 0

from data.chamado_sql import ATUALIZAR_STATUS

def atualizar_status_chamado(id_chamado: int, novo_status: str) -> bool:
    if novo_status not in ['aberto', 'em andamento', 'resolvido']:
        raise ValueError("Status inválido. Use: 'aberto', 'em andamento' ou 'resolvido'.")
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_STATUS, (novo_status, id_chamado))
        return cursor.rowcount > 0

def excluir_chamado(id_chamado: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_chamado,))
        return cursor.rowcount > 0


def obter_todos_chamados_paginado(offset: int, limite: int) -> List[Chamado]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS_PAGINADO, (limite, offset))
        rows = cursor.fetchall()
        return [
            Chamado(
                id=row["id"],
                id_usuario=row["id_usuario"],
                id_admin=row["id_admin"],
                titulo=row["titulo"],
                descricao=row["descricao"],
                status=row["status"],
                data=row["data"]
            )
            for row in rows
        ]



def obter_chamado_por_id(id_chamado: int) -> Optional[Chamado]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_chamado,))
        row = cursor.fetchone()
        if row:
            return Chamado(
                id=row["id"],
                id_usuario=row["id_usuario"],
                id_admin=row["id_admin"],
                titulo=row["titulo"],
                descricao=row["descricao"],
                status=row["status"],
                data=row["data"]
            )
        return None




```

# data\chamado_sql.py

```py
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS chamado (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    id_admin INTEGER,
    titulo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    status TEXT CHECK(status IN ('aberto', 'em andamento', 'resolvido')) DEFAULT 'aberto',
    data DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_admin) REFERENCES administrador(id_admin)
);
"""

INSERIR = """
INSERT INTO chamado (id_usuario, id_admin, titulo, descricao, status, data) 
VALUES (?, ?, ?, ?, ?, ?);
"""

ATUALIZAR = """
UPDATE chamado 
SET id_usuario = ?, id_admin = ?, titulo = ?, descricao = ?, status = ?, data = ?
WHERE id = ?
"""
ATUALIZAR_STATUS = """
UPDATE chamado
SET status = ?
WHERE id = ?;
"""

EXCLUIR = """
DELETE FROM chamado
WHERE id = ?;
"""

OBTER_TODOS_PAGINADO = """
SELECT id, id_usuario, id_admin, titulo, descricao, status, data
FROM chamado
ORDER BY id
LIMIT ? OFFSET ?;
"""


OBTER_POR_ID = """
SELECT * 
FROM chamado
WHERE id = ?;

"""
```

# data\comentario_model.py

```py
from dataclasses import dataclass, field
import datetime
from typing import Optional

from data.postagem_artigo_model import PostagemArtigo
from data.usuario_model import Usuario

@dataclass
class Comentario:
    id: int
    id_usuario: int
    id_artigo: int
    texto: str
    data_comentario: str = field(default_factory=lambda: datetime.datetime.now().strftime("%Y-%m-%d"))
    data_moderacao: Optional[str] = None

```

# data\comentario_repo.py

```py
from typing import Optional, List
from data.comentario_model import Comentario
from data.comentario_sql import *
from data.postagem_artigo_model import PostagemArtigo
from data.usuario_model import Usuario
from util import get_connection


def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de categorias: {e}")
        return False


def inserir(comentario: Comentario) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
        comentario.id_usuario,
        comentario.id_artigo,
        comentario.texto,
        ))
        return cursor.lastrowid


def atualizar(comentario: Comentario) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (
            comentario.texto,
            comentario.data_moderacao,
            comentario.id
        ))
        return cursor.rowcount > 0


def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return cursor.rowcount > 0


def obter_todos_paginado(limite: int, offset: int) -> List[Comentario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS_PAGINADO, (limite, offset))
        rows = cursor.fetchall()
        return [
            Comentario(
                id=row["id"],
                id_usuario=Usuario(id_usuario=row["id_usuario"], nome=row["nome_usuario"]),
                id_artigo=PostagemArtigo(id=row["id_artigo"], titulo=row["titulo_artigo"]),
                texto=row["texto"],
                data_comentario=row["data_comentario"],
                data_moderacao=row["data_moderacao"]
            )
            for row in rows]



def obter_por_id(id: int) -> Optional[Comentario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            return Comentario(
                id=row["id"],
                id_usuario=Usuario(id_usuario=row["id_usuario"], nome=row["nome_usuario"]),
                id_artigo=PostagemArtigo(id=row["id_artigo"], titulo=row["titulo_artigo"]),
                texto=row["texto"],
                data_comentario=row["data_comentario"],
                data_moderacao=row["data_moderacao"])
        return None
```

# data\comentario_sql.py

```py
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS comentario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    id_artigo INTEGER NOT NULL,
    texto TEXT NOT NULL,
    data_comentario DATE DEFAULT CURRENT_DATE,
    data_moderacao DATE,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id),
    FOREIGN KEY (id_artigo) REFERENCES postagem_artigo(id)
);
"""
INSERIR = """
INSERT INTO comentario (id_usuario, id_artigo, texto, data_comentario, data_moderacao)
VALUES (?, ?, ?);
"""
ATUALIZAR = """
UPDATE comentario SET texto = ?, data_moderacao = ?
WHERE id = ?;
"""
EXCLUIR = """
DELETE FROM comentario 
WHERE id = ?;
"""
OBTER_TODOS_PAGINADO = """
SELECT 
    c.id,
    c.texto,
    c.data_comentario,
    c.data_moderacao,
    u.id_usuario,
    u.nome AS nome_usuario,
    a.id AS id_artigo,
    a.titulo AS titulo_artigo
FROM comentario c
JOIN usuario u ON c.id_usuario = u.id_usuario
JOIN postagem_artigo a ON c.id_artigo = a.id
ORDER BY c.data_comentario DESC
LIMIT ? OFFSET ?;
"""


OBTER_POR_ID = """
SELECT 
    c.id,
    c.texto,
    c.data_comentario,
    c.data_moderacao,
    u.id_usuario,
    u.nome AS nome_usuario,
    a.id AS id_artigo,
    a.titulo AS titulo_artigo
FROM comentario c
JOIN usuario u ON c.id_usuario = u.id_usuario
JOIN postagem_artigo a ON c.id_artigo = a.id
WHERE c.id = ?;
"""
```

# data\curtida_artigo_model.py

```py
from dataclasses import dataclass
from data.postagem_artigo_model import PostagemArtigo
from data.usuario_model import Usuario

@dataclass
class CurtidaArtigo:
    usuario: Usuario
    artigo: PostagemArtigo
    data_curtida: str
```

# data\curtida_artigo_repo.py

```py
from typing import Optional, List
from data.curtida_artigo_model import CurtidaArtigo
from data.curtida_artigo_sql import *
from data.postagem_artigo_model import PostagemArtigo
from data.usuario_model import Usuario
from util import get_connection


def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de categorias: {e}")
        return False


def inserir(curtida: CurtidaArtigo) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (curtida.id_usuario, curtida.id_artigo))
        return cursor.rowcount > 0

def excluir_curtida(id_usuario: int, id_postagem_artigo: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_usuario, id_postagem_artigo))
        return cursor.rowcount > 0


def obter_todos_paginado(limite: int, offset: int) -> List[CurtidaArtigo]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS_PAGINADO, (limite, offset))
        rows = cursor.fetchall()
        return [
            CurtidaArtigo(
                usuario=Usuario(id=row["id_usuario"], nome=row["nome_usuario"]),
                artigo=PostagemArtigo(id=row["id_postagem_artigo"], titulo=row["titulo_artigo"]),
                data_curtida=row["data_curtida"]
            )
            for row in rows]


def obter_por_id(id_usuario: int, id_postagem_artigo: int) -> Optional[CurtidaArtigo]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_usuario, id_postagem_artigo))
        row = cursor.fetchone()
        if row:
            return CurtidaArtigo(
                usuario=Usuario(id=row["id_usuario"],nome=row["nome_usuario"]),
                artigo=PostagemArtigo(id=row["id_artigo"], nome=row["titulo_artigo"]), #verificar o nome do campo titulo na tabela postagem art.
                data_curtida=row["data_curtida"]
            )
        return None
```

# data\curtida_artigo_sql.py

```py
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS curtida_artigo (
    id_usuario INTEGER NOT NULL,
    id_postagem_artigo INTEGER NOT NULL,
    data_curtida DATE DEFAULT CURRENT_DATE
    PRIMARY KEY (id_usuario, id_postagem_artigo),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_postagem_artigo) REFERENCES postagem_artigo(id_artigo)
);  
"""

INSERIR = """
INSERT INTO curtida_artigo (id_usuario, id_postagem_artigo)
VALUES (?, ?);
"""

ATUALIZAR = """
UPDATE curtida_artigo
SET data_curtida = ?
WHERE id_usuario = ? AND id_postagem_artigo = ?;
"""

EXCLUIR = """
DELETE FROM curtida_artigo
WHERE id_usuario = ? 
AND id_postagem_artigo = ?;
"""

OBTER_TODOS_PAGINADO = """
SELECT
    ca.id_usuario,
    u.nome AS nome_usuario,
    ca.id_postagem_artigo,
    pa.titulo AS titulo_artigo,
    ca.data_curtida
FROM curtida_artigo ca
INNER JOIN usuario u ON ca.id_usuario = u.id_usuario
INNER JOIN postagem_artigo pa ON ca.id_postagem_artigo = pa.id
ORDER BY ca.data_curtida DESC
LIMIT ? OFFSET ?;
"""

OBTER_POR_ID = """
SELECT
    ca.id_usuario,
    u.nome AS nome_usuario,
    ca.id_postagem_artigo,
    pa.titulo AS titulo_artigo,
    ca.data_curtida
FROM curtida_artigo ca
INNER JOIN usuario u ON ca.id_usuario = u.id_usuario
INNER JOIN postagem_artigo pa ON ca.id_postagem_artigo = pa.id
WHERE ca.id_usuario = ? AND ca.id_postagem_artigo = ?;
"""
```

# data\curtida_feed_model.py

```py
from dataclasses import dataclass
from typing import Optional

@dataclass
class CurtidaFeed:
    id_usuario: int
    id_postagem_feed: int
    data_curtida: Optional[str] = None

```

# data\curtida_feed_repo.py

```py
from typing import Optional, List
from data.curtida_feed_model import CurtidaFeed
from data.curtida_feed_sql import *
from util import get_connection


def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de categorias: {e}")
        return False


def inserir(curtida: CurtidaFeed) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            curtida.id_usuario,
            curtida.id_postagem_feed
        ))
        return cursor.rowcount > 0


def excluir(id_usuario: int, id_postagem_feed: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_usuario, id_postagem_feed))
        return cursor.rowcount > 0


def obter_todos_paginado(limite: int, offset: int) -> List[CurtidaFeed]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS_PAGINADO, (limite, offset))
        rows = cursor.fetchall()
        return [
            CurtidaFeed(
                id_usuario=row["id_usuario"],
                id_postagem_feed=row["id_postagem_feed"],
                data_curtida=row["data_curtida"]
            )
            for row in rows]


def obter_por_id(id_usuario: int, id_postagem_feed: int) -> Optional[CurtidaFeed]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_usuario, id_postagem_feed))
        row = cursor.fetchone()
        if row:
            return CurtidaFeed(
                id_usuario=id_usuario,
                id_postagem_feed=id_postagem_feed,
                data_curtida=row["data_curtida"]
            )
        return None

```

# data\curtida_feed_sql.py

```py
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS curtida_feed (
    id_usuario INTEGER NOT NULL,
    id_postagem_feed INTEGER NOT NULL,
    data_curtida DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (id_usuario, id_postagem_feed),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_postagem_feed) REFERENCES postagem_feed(id_postagem_feed)
);
"""

INSERIR = """
INSERT INTO curtida_feed (id_usuario, id_postagem_feed)
VALUES (?, ?);
"""

EXCLUIR = """
DELETE FROM curtida_feed 
WHERE id_usuario = ? AND id_postagem_feed = ?;
"""


OBTER_TODOS_PAGINADO = """
SELECT 
    cf.id_usuario,
    u.nome AS nome_usuario,
    cf.id_postagem_feed,
    pf.descricao AS descricao_postagem,
    pf.imagem,
    cf.data_curtida
FROM curtida_feed cf
JOIN usuario u ON cf.id_usuario = u.id_usuario
JOIN postagem_feed pf ON cf.id_postagem_feed = pf.id_postagem_feed
ORDER BY cf.data_curtida DESC
LIMIT ? OFFSET ?;
"""

OBTER_POR_ID = """
SELECT 
    u.nome AS nome_usuario,
    pf.descricao AS descricao_postagem,
    pf.imagem,
    cf.data_curtida
FROM curtida_feed cf
JOIN usuario u ON cf.id_usuario = u.id_usuario
JOIN postagem_feed pf ON cf.id_postagem_feed = pf.id_postagem_feed
WHERE cf.id_usuario = ? AND cf.id_postagem_feed = ?;
"""

```

# data\denuncia_model.py

```py
from dataclasses import dataclass
from typing import Optional
from data.administrador_model import Administrador
from data.usuario_model import Usuario

@dataclass
class Denuncia:
    id_denuncia: Optional[int] 
    id_usuario: int
    id_admin: int
    motivo: str
    data_denuncia: str
    status: str

```

# data\denuncia_repo.py

```py
from typing import Optional, List
from data.denuncia_model import Denuncia
from data.denuncia_sql import *
from util import get_connection


def criar_tabela_denuncia() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de categorias: {e}")
        return False


def inserir_denuncia(denuncia: Denuncia) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            denuncia.id_usuario,
            denuncia.id_admin,
            denuncia.motivo,
            denuncia.data_denuncia,  # <- adicionar aqui
            denuncia.status
        ))
        return cursor.lastrowid
    

def atualizar_denuncia(denuncia: Denuncia) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (
            denuncia.id_usuario,
            denuncia.id_admin,
            denuncia.motivo,
            denuncia.data_denuncia,
            denuncia.status,
            denuncia.id_denuncia
        ))
        return cursor.rowcount > 0


def excluir_denuncia(id_denuncia: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_denuncia,))
        return cursor.rowcount > 0

# def obter_todas_denuncias_paginadas(limite: int, offset: int) -> List[Denuncia]:
#     with get_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute(OBTER_TODAS_DENUNCIAS_PAGINADAS, (limite, offset))
#         rows = cursor.fetchall()
#         return [Denuncia(**row) for row in rows]

def obter_todas_denuncias_paginadas(limite: int, offset: int) -> List[Denuncia]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODAS_DENUNCIAS_PAGINADAS, (limite, offset))
        rows = cursor.fetchall()

        denuncias = []
        for row in rows:
            dados = {
                "id_denuncia": row["id_denuncia"],
                "id_usuario": row["id_usuario"],
                "id_admin": row["id_admin"],
                "motivo": row["motivo"],
                "data_denuncia": row["data_denuncia"],
                "status": row["status"]
            }
            denuncias.append(Denuncia(**dados))
        return denuncias


# def obter_denuncia_por_id(id_denuncia: int) -> Optional[Denuncia]:
#     with get_connection() as conn:
#         cursor = conn.cursor()
#         cursor.execute(OBTER_POR_ID, (id_denuncia,))
#         row = cursor.fetchone()
#         denuncia = Denuncia(
#             id_denuncia=row["id_denuncia"],
#             id_usuario=row["id_usuario"],
#             id_admin=row["id_admin"],
#             motivo = row["motivo"],
#             data_denuncia = row["data_denuncia"],
#             status = row["status"]
#         )
#         return denuncia

def obter_denuncia_por_id(id_denuncia: int) -> Optional[Denuncia]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_denuncia,))
        row = cursor.fetchone()
        if row is None:
            return None  # <- evita erro
        denuncia = Denuncia(
            id_denuncia=row["id_denuncia"],
            id_usuario=row["id_usuario"],
            id_admin=row["id_admin"],
            motivo=row["motivo"],
            data_denuncia=row["data_denuncia"],
            status=row["status"]
        )
        return denuncia
    
```

# data\denuncia_sql.py

```py
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS denuncia (
    id_denuncia INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    id_admin INTEGER,
    motivo TEXT NOT NULL,
    data_denuncia DATETIME DEFAULT CURRENT_DATE,
    status TEXT NOT NULL CHECK (status IN ('pendente', 'aprovada', 'rejeitada')),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_admin) REFERENCES administrador(id_admin)
);
"""

INSERIR = """
INSERT INTO denuncia (id_usuario, id_admin, motivo, data_denuncia, status)
VALUES (?, ?, ?, ?, ?)
"""

ATUALIZAR = """
UPDATE denuncia 
SET id_usuario = ?, id_admin = ?, motivo = ?, data_denuncia = ?,  status = ?
WHERE id_denuncia = ?;
"""

EXCLUIR = """
DELETE FROM denuncia 
WHERE id_denuncia = ?;
"""

# OBTER_TODAS_DENUNCIAS_PAGINADAS = """
# SELECT
#     d.id_denuncia,
#     d.id_usuario,
#     u.nome AS nome_usuario,
#     d.id_admin,
#     a.nome AS nome_admin,
#     d.motivo,
#     d.data_denuncia,
#     d.status
# FROM denuncia d
# INNER JOIN usuario u ON d.id_usuario = u.id_usuario
# INNER JOIN administrador a ON d.id_admin = a.id_admin
# ORDER BY d.data_denuncia DESC
# LIMIT ? OFFSET ?;
# """

OBTER_TODAS_DENUNCIAS_PAGINADAS = """
SELECT 
    d.id_denuncia,
    d.id_usuario,
    u.nome AS nome_usuario,
    d.id_admin,
    a.nome AS nome_admin,
    d.motivo,
    d.data_denuncia,
    d.status
FROM denuncia d
JOIN usuario u ON d.id_usuario = u.id_usuario
JOIN administrador a ON d.id_admin = a.id_admin
ORDER BY d.id_denuncia ASC
LIMIT ? OFFSET ?
"""

OBTER_POR_ID = """
SELECT
    d.id_denuncia,
    d.id_usuario,
    u.nome AS nome_usuario,
    d.id_admin,
    a.nome AS nome_admin,
    d.motivo,
    d.data_denuncia,
    d.status
FROM denuncia d
INNER JOIN usuario u ON d.id_usuario = u.id_usuario
INNER JOIN administrador a ON d.id_admin = a.id_admin
WHERE d.id_denuncia = ?;
"""
```

# data\postagem_artigo_model.py

```py
from dataclasses import dataclass
from data.categoria_artigo_model import CategoriaArtigo
from data.veterinario_model import Veterinario

@dataclass
class PostagemArtigo:
    id: int
    veterinario: Veterinario
    titulo: str
    conteudo: str
    categoria_artigo: CategoriaArtigo
    data_publicacao: str
    visualizacoes: int
```

# data\postagem_artigo_repo.py

```py
from typing import Optional, List
from data.categoria_artigo_model import CategoriaArtigo
from data.postagem_artigo_model import PostagemArtigo
from data.postagem_artigo_sql import *
from util import get_connection
from data.veterinario_model import Veterinario


def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de categorias: {e}")
        return False


def inserir(postagem: PostagemArtigo) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            postagem.id_veterinario,
            postagem.titulo,
            postagem.conteudo,
            postagem.categoria_artigo .id
        ))
        return cursor.lastrowid


def atualizar(postagem: PostagemArtigo) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (
            postagem.titulo,
            postagem.conteudo,
            postagem.categoria_artigo .id,
            postagem.visualizacoes,
            postagem.id
        ))
        return cursor.rowcount > 0


def excluir(id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id,))
        return cursor.rowcount > 0


def obter_todos_paginado(limite: int, offset: int) -> List[PostagemArtigo]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS_PAGINADO, (limite, offset))
        rows = cursor.fetchall()
        return [
            PostagemArtigo(
                id=row["id"],
                veterinario=Veterinario(id=row["id_veterinario"], nome=row["nome_veterinario"]),
                titulo=row["titulo"],
                conteudo=row["conteudo"],
                categoria=CategoriaArtigo(id=row["id_categoria_artigo"], nome_categoria=row["nome_categoria"]),
                data_publicacao=row["data_publicacao"],
                visualizacoes=row["visualizacoes"]
            )
            for row in rows]



def obter_por_id(id: int) -> Optional[PostagemArtigo]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            return PostagemArtigo(
                id=row["id"],
                veterinario=Veterinario(id=row["id_veterinario"], nome=row["nome_veterinario"]),
                titulo=row["titulo"],
                conteudo=row["conteudo"],
                categoria=CategoriaArtigo(id=row["categoria_id"], nome_categoria=row["nome_categoria"]),
                data_publicacao=row["data_publicacao"],
                visualizacoes=row["visualizacoes"]
            )
        return None
```

# data\postagem_artigo_sql.py

```py
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS postagem_artigo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_veterinario INTEGER NOT NULL,
    titulo TEXT NOT NULL,
    conteudo TEXT NOT NULL,
    id_categoria_artigo INTEGER NOT NULL,
    data_publicacao DATE DEFAULT CURRENT_DATE,
    visualizacoes INTEGER DEFAULT 0,
    FOREIGN KEY (id_veterinario) REFERENCES veterinario(id_usuario),
    FOREIGN KEY (id_categoria_artigo) REFERENCES categoria_artigo(id)
);
"""

INSERIR = """
INSERT INTO postagem_artigo (id_veterinario, titulo, conteudo, id_categoria_artigo)
VALUES (?, ?, ?, ?);
"""

ATUALIZAR = """
UPDATE postagem_artigo 
SET titulo = ?, conteudo = ?, id_categoria_artigo = ?
WHERE id = ?;
"""

EXCLUIR = """
DELETE FROM postagem_artigo 
WHERE id = ?;
"""

OBTER_TODOS_PAGINADO = """
SELECT 
    p.id,
    p.id_veterinario,
    v.nome AS nome_veterinario,
    p.titulo,
    p.conteudo,
    p.id_categoria_artigo,
    c.nome AS nome_categoria,
    p.data_publicacao,
    p.visualizacoes
FROM postagem_artigo p
JOIN categoria_artigo c ON p.id_categoria_artigo = c.id
JOIN veterinario v ON p.id_veterinario = v.id
ORDER BY p.data_publicacao DESC
LIMIT ? OFFSET ?;
"""


OBTER_POR_ID = """
SELECT 
    p.id,
    p.id_veterinario,
    v.nome AS nome_veterinario,
    p.titulo,
    p.conteudo,
    p.id_categoria_artigo,
    c.nome AS nome_categoria,
    p.data_publicacao,
    p.visualizacoes
FROM postagem_artigo p
JOIN categoria_artigo c ON p.id_categoria_artigo = c.id
JOIN veterinario v ON p.id_veterinario = v.id
WHERE p.id = ?;
"""
```

# data\postagem_feed_model.py

```py
from dataclasses import dataclass
from typing import Optional
from data.tutor_model import Tutor

@dataclass
class PostagemFeed:
    id_postagem_feed: int
    tutor: Tutor
    imagem: Optional[str]
    descricao: str
    data_postagem: str

```

# data\postagem_feed_repo.py

```py
from typing import Optional, List
from data.postagem_feed_model import PostagemFeed
from data.postagem_feed_sql import *
from data.tutor_model import Tutor
from util import get_connection


def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de categorias: {e}")
        return False


def inserir(postagem: PostagemFeed) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            postagem.id_tutor,
            postagem.imagem,
            postagem.descricao
        ))
        return cursor.lastrowid


    
def atualizar(postagem: PostagemFeed) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (
            postagem.descricao,
            postagem.id_postagem_feed
        ))
        return cursor.rowcount > 0


def excluir(id_postagem_feed: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_postagem_feed,))
        return cursor.rowcount > 0

def obter_todos_paginado(limite: int, offset: int) -> List[PostagemFeed]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS_PAGINADO, (limite, offset))
        rows = cursor.fetchall()
        return [
            PostagemFeed(
                id_postagem_feed=row["id_postagem_feed"],
                tutor=Tutor(id=row["id_tutor"], nome=row["nome_tutor"]),
                imagem=row["imagem"],
                descricao=row["descricao"],
                data_postagem=row["data_postagem"]
            )
            for row in rows
        ]



def obter_por_id(id_postagem_feed: int) -> Optional[PostagemFeed]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_postagem_feed,))
        row = cursor.fetchone()
        if row:
            return PostagemFeed(
                id_postagem_feed=row["id_postagem_feed"],
                tutor=Tutor(id=row["id_tutor"], nome=row["nome_tutor"]),
                imagem=row["imagem"],
                descricao=row["descricao"],
                data_postagem=row["data_postagem"]
            )
        return None
```

# data\postagem_feed_sql.py

```py
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS postagem_feed (
    id_postagem_feed INTEGER PRIMARY KEY AUTOINCREMENT,
    id_tutor INTEGER NOT NULL,
    imagem TEXT,
    descricao TEXT,
    data_postagem DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (id_tutor) REFERENCES tutor(id_usuario)
);
"""

INSERIR = """
INSERT INTO postagem_feed (id_tutor, imagem, descricao)
VALUES (?, ?, ?);
"""

ATUALIZAR = """
UPDATE postagem_feed
SET descricao = ?
WHERE id_postagem_feed = ?;
"""

EXCLUIR = """
DELETE FROM postagem_feed
WHERE id_postagem_feed = ?;
"""

OBTER_TODOS_PAGINADO = """
SELECT 
    pf.id_postagem_feed,
    pf.id_tutor,
    u.nome AS nome_tutor,
    pf.imagem,
    pf.descricao,
    pf.data_postagem
FROM postagem_feed pf
JOIN tutor t ON pf.id_tutor = t.id_usuario
JOIN usuario u ON t.id_usuario = u.id_usuario
ORDER BY pf.data_postagem DESC
LIMIT ? OFFSET ?;
"""


OBTER_POR_ID = """
SELECT 
    pf.id_postagem_feed,
    pf.id_tutor,
    u.nome AS nome_tutor,
    pf.imagem,
    pf.descricao,
    pf.data_postagem
FROM postagem_feed pf
JOIN tutor t ON pf.id_tutor = t.id_usuario
JOIN usuario u ON t.id_usuario = u.id_usuario
WHERE pf.id_postagem_feed = ?;
"""

```

# data\resposta_chamado_model.py

```py
from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass
class RespostaChamado:
    id: Optional[int] = None     
    id_chamado: int = 0
    titulo: str = ""
    descricao: str = ""
    data: Optional[date] = None  
```

# data\resposta_chamado_repo.py

```py
from typing import Optional, List
from data.resposta_chamado_model import RespostaChamado
from data.resposta_chamado_sql import *
from util import get_connection

def criar_tabelas() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de categorias: {e}")
        return False
    
def inserir_resposta(resposta: RespostaChamado) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            resposta.id_chamado,
            resposta.titulo,
            resposta.descricao,
            resposta.data
        ))
        return cursor.lastrowid
    
def obter_todas_respostas_paginado(limite: int, offset: int) -> List[RespostaChamado]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS_PAGINADO, (limite, offset))
        rows = cursor.fetchall()
        return [
            RespostaChamado(
                id=row["id"],
                id_chamado=row["id_chamado"],
                titulo=row["titulo"],
                descricao=row["descricao"],
                data=row["data"]
            )
            for row in rows
        ]


def obter_resposta_por_id(id_resposta: int) -> Optional[RespostaChamado]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_resposta,))
        row = cursor.fetchone()
        if row:
            return RespostaChamado(
                id=row["id"],
                id_chamado=row["id_chamado"],
                titulo=row["titulo"],
                descricao=row["descricao"],
                data=row["data"]
            )
        return None
```

# data\resposta_chamado_sql.py

```py
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS resposta_chamado (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_chamado INTEGER NOT NULL,
    titulo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    data DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (id_chamado) REFERENCES chamado(id)
);
"""

INSERIR = """
INSERT INTO resposta_chamado (id_chamado, titulo, descricao, data) 
VALUES (?, ?, ?, ?);
"""

ATUALIZAR = """
UPDATE resposta_chamado 
SET id_chamado, titulo = ?, descricao = ?, data = ?
WHERE id = ?
"""

EXCLUIR = """
DELETE FROM resposta_chamado
WHERE id = ?;
"""

OBTER_TODOS_PAGINADO = """
SELECT * 
FROM resposta_chamado 
ORDER BY data DESC
LIMIT ? OFFSET ?;
"""


OBTER_POR_ID = """
SELECT * 
FROM resposta_chamado
WHERE id = ?;

"""
```

# data\seguida_model.py

```py
from dataclasses import dataclass
from datetime import date

from data.tutor_model import Tutor
from data.veterinario_model import Veterinario

@dataclass
class Seguida:
    id_veterinario: Veterinario
    id_tutor: Tutor
    data_inicio: date
# verificar se data_inicio est´CORRETO, verificar se os ints estao corretos
```

# data\seguida_repo.py

```py
from typing import Optional, List
from data.seguida_model import Seguida
from data.seguida_sql import *
from data.tutor_model import Tutor
from util import get_connection
from data.veterinario_model import Veterinario


def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de categorias: {e}")
        return False


def inserir(seguida: Seguida) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            seguida.id_veterinario,
            seguida.id_tutor))
        return cursor.rowcount > 0


def excluir(id_veterinario: int, id_tutor: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_veterinario, id_tutor))
        return cursor.rowcount > 0


def obter_todos_paginado(limite: int, offset: int) -> List[Seguida]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS_PAGINADO, (limite, offset))
        rows = cursor.fetchall()
        return [
            Seguida(
                id_veterinario=Veterinario(id_usuario=row["id_veterinario"], nome=row["nome_veterinario"]),
                id_tutor=Tutor(id_usuario=row["id_tutor"], nome=row["nome_tutor"]),
                data_inicio=row["data_inicio"]
            )
            for row in rows]



def obter_por_id(id_veterinario: int, id_tutor: int) -> Optional[Seguida]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_veterinario, id_tutor))
        row = cursor.fetchone()
        if row:
            return Seguida(
                id_veterinario=Veterinario(id_usuario=row["id_veterinario"], nome=row["nome_veterinario"]),
                id_tutor=Tutor(id_usuario=row["id_tutor"], nome=row["nome_tutor"]),
                data_inicio=row["data_inicio"]
            )
        return None

```

# data\seguida_sql.py

```py
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS seguida (
  id_veterinario INTEGER NOT NULL,
  id_tutor INTEGER NOT NULL,
  data_inicio DATE DEFAULT CURRENT_DATE,
  PRIMARY KEY (id_veterinario, id_tutor),
  FOREIGN KEY (id_veterinario) REFERENCES veterinario(id_usuario),
  FOREIGN KEY (id_tutor) REFERENCES tutor(id_usuario)
);
"""

INSERIR = """
INSERT INTO seguida (id_veterinario, id_tutor)
VALUES (?, ?);
"""

EXCLUIR = """
DELETE FROM seguida 
WHERE id_veterinario = ? AND id_tutor = ?;
"""

OBTER_TODOS_PAGINADO = """
SELECT 
  s.id_veterinario,
  v.nome AS nome_veterinario,
  s.id_tutor,
  t.nome AS nome_tutor,
  s.data_inicio
FROM seguida s
JOIN veterinario v ON s.id_veterinario = v.id_usuario
JOIN tutor t ON s.id_tutor = t.id_usuario
ORDER BY s.data_inicio DESC
LIMIT ? OFFSET ?;
"""


OBTER_POR_ID = """
SELECT 
  s.id_veterinario,
  v.nome AS nome_veterinario,
  s.id_tutor,
  t.nome AS nome_tutor,
  s.data_inicio
FROM seguida s
JOIN veterinario v ON s.id_veterinario = v.id_usuario
JOIN tutor t ON s.id_tutor = t.id_usuario
WHERE s.id_veterinario = ? AND s.id_tutor = ?;
"""

```

# data\tutor_model.py

```py
from dataclasses import dataclass

from data.usuario_model import Usuario

@dataclass
class Tutor(Usuario):
    pass
```

# data\tutor_repo.py

```py
from typing import Any, Optional
from data import usuario_repo
from data.tutor_model import Tutor
import data.tutor_sql as tutor_sql
from data.usuario_model import Usuario
import data.usuario_sql as usuario_sql
from util import get_connection

  
def criar_tabela_tutor() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(tutor_sql.CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de categorias: {e}")
        return False

    
def inserir_tutor(tutor: Tutor) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(tutor_sql.INSERIR, (tutor.id_usuario, tutor.nome, tutor.email, tutor.senha))
        return cursor.lastrowid
    



def atualizar_tutor(tutor: Tutor) -> bool:
    return usuario_repo.atualizar_usuario(tutor)
    
def excluir_tutor(id_tutor: int) -> bool:
     with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(tutor_sql.EXCLUIR, (id_tutor,))
        return (cursor.rowcount > 0)

def obter_todos_tutores_paginado(limite: int, offset: int) -> list[Tutor]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(tutor_sql.OBTER_TODOS_PAGINADO, (limite, offset))
        rows = cursor.fetchall()
        tutores = [
            Tutor(
                id_tutor=row["id_tutor"],
                nome=row["nome"],
                email=row["email"],
                telefone=row["telefone"]
            )
            for row in rows]
        return tutores

    
def obter_tutor_por_id(id_tutor: int) -> Optional[Tutor]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(tutor_sql.OBTER_POR_ID, (id_tutor,))
        row = cursor.fetchone()
        tutor = Tutor(
                id_tutor=row["id_tutor"], 
                telefone=row["telefone"])
        return tutor
```

# data\tutor_sql.py

```py
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS tutor (
    id_tutor INTEGER PRIMARY KEY,
    FOREIGN KEY (id_tutor) REFERENCES usuario(id_usuario)
);
"""

INSERIR = """
INSERT INTO tutor (id_tutor)
VALUES (?);
"""

EXCLUIR = """
DELETE FROM tutor 
WHERE id_tutor = ?;
"""

OBTER_TODOS_PAGINADO = """
SELECT 
    t.id_tutor,
    u.nome, 
    u.email, 
    u.telefone
FROM tutor t
INNER JOIN usuario u ON t.id_tutor = u.id_usuario
ORDER BY u.nome
LIMIT ? OFFSET ?;
"""


OBTER_POR_ID = """
SELECT 
t.id_tutor,
u.nome,
u.email,
u.telefone
FROM tutor t
INNER JOIN usuario u ON t.id_usuario = u.id_usuario
WHERE t.id_tutor = ?;
"""
```

# data\usuario_model.py

```py
from dataclasses import dataclass

@dataclass
class Usuario:
    id_usuario: int
    nome: str
    email: str
    senha: str
    telefone: str
```

# data\usuario_repo.py

```py
from typing import Any, Optional
from data.usuario_model import Usuario
from data.usuario_sql import *
from util import get_connection


def criar_tabela_usuario() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de categorias: {e}")
        return False

def inserir_usuario(usuario: Usuario) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            usuario.nome,
            usuario.email,
            usuario.senha,
            usuario.telefone))
        return cursor.lastrowid


def atualizar_usuario(usuario: Usuario) -> bool:
     with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (
            usuario.nome,
            usuario.email,
            usuario.telefone,
            usuario.id_usuario))
        return cursor.rowcount > 0
    
def atualizar_senha_usuario(id_usuario: int, senha: str) -> bool:
     with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_SENHA, (senha, id_usuario))
        return (cursor.rowcount > 0)
    
def excluir_usuario(id_usuario: int) -> bool:
     with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_usuario,))
        return (cursor.rowcount > 0)

def obter_todos_usuarios_paginado(limite: int, offset: int) -> list[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS_PAGINADO, (limite, offset))
        rows = cursor.fetchall()
        usuarios = [
            Usuario(
                id_usuario=row["id_usuario"], 
                nome=row["nome"], 
                email=row["email"], 
                senha=row["senha"], 
                telefone=row["telefone"]
            ) 
            for row in rows]
        return usuarios

def obter_usuario_por_id(id_usuario: int) -> Optional[Usuario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_usuario,))
        row = cursor.fetchone()
        if row is None:
            return None
        return Usuario(
            id_usuario=row["id_usuario"],
            nome=row["nome"],
            email=row["email"],
            senha=row["senha"],
            telefone=row["telefone"]
        )


```

# data\usuario_sql.py

```py
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha CHAR(8) NOT NULL,
    telefone CHAR(11) NOT NULL
);
"""

INSERIR = """
INSERT INTO usuario (nome, email, senha, telefone)
VALUES (?, ?, ?, ?);
"""
ATUALIZAR = """
UPDATE usuario 
SET nome = ?, email = ?, telefone = ?
WHERE id_usuario = ?;
"""

ATUALIZAR_SENHA = """
UPDATE usuario 
SET senha = ?
WHERE id_usuario = ?;
"""

EXCLUIR = """
DELETE FROM usuario 
WHERE id_usuario = ?;
"""
OBTER_TODOS_PAGINADO = """
SELECT 
    id_usuario, 
    nome, 
    email, 
    senha, 
    telefone
FROM usuario 
ORDER BY nome
LIMIT ? OFFSET ?;
"""


OBTER_POR_ID = """
SELECT 
id_usuario, 
nome, 
email,
senha,
telefone
FROM usuario 
WHERE id_usuario = ?;
"""
```

# data\verificacao_crmv_model.py

```py
from dataclasses import dataclass
from data.veterinario_model import Veterinario
from data.administrador_model import Administrador

@dataclass
class VerificacaoCRMV:
    id: int
    veterinario: Veterinario
    administrador: Administrador
    data_verificacao: str
    status_verificacao: str

```

# data\verificacao_crmv_repo.py

```py
from typing import Optional, List
from data.verificacao_crmv_model import VerificacaoCRMV
from data.verificacao_crmv_sql import *
from util import get_connection
from data.veterinario_model import Veterinario
from data.administrador_model import Administrador


def criar_tabela() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de categorias: {e}")
        return False

def inserir(verificacao: VerificacaoCRMV) -> Optional[int]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR, (
            verificacao.veterinario.id_veterinario,
            verificacao.administrador.id_admin,
            verificacao.status_verificacao
        ))
        return cursor.lastrowid


def atualizar(id_veterinario: int, novo_status: str) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (novo_status, id_veterinario))
        return cursor.rowcount > 0


def excluir(id_veterinario: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_veterinario,))
        return cursor.rowcount > 0


def obter_todos_paginado(limite: int, offset: int) -> List[VerificacaoCRMV]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS_PAGINADO, (limite, offset))
        rows = cursor.fetchall()
        return [
            VerificacaoCRMV(
                id=row["id"],
                veterinario=Veterinario(id_veterinario=row["id_veterinario"], nome=row["nome_veterinario"]),
                administrador=Administrador(
                    id_admin=row["id_admin"],
                    nome=row["nome_admin"],
                    email=row["email_admin"]
                ),
                data_verificacao=row["data_verificacao"],
                status_verificacao=row["status_verificacao"]
            )
            for row in rows]



def obter_por_id(id: int) -> Optional[VerificacaoCRMV]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            return VerificacaoCRMV(
                id=row["id"],
                veterinario=Veterinario(id_veterinario=row["id_veterinario"]),
                administrador=Administrador(id_admin=row["id_admin"],nome=row["nome_admin"],email=row["email_admin"]),
                data_verificacao=row["data_verificacao"],
                status_verificacao=row["status_verificacao"])
        return None

```

# data\verificacao_crmv_sql.py

```py
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS verificacao_crmv (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_veterinario INTEGER NOT NULL,
    id_admin INTEGER NOT NULL,
    data_verificacao DATE DEFAULT CURRENT_DATE,
    status_verificacao TEXT CHECK(status_verificacao IN ('pendente', 'verificado', 'rejeitado')),
    FOREIGN KEY (id_veterinario) REFERENCES veterinario(id_usuario),
    FOREIGN KEY (id_admin) REFERENCES administrador(id_admin)
);
"""

INSERIR = """
INSERT INTO verificacao_crmv (id_veterinario, id_admin, status_verificacao)
VALUES (?, ?, ?);
"""

ATUALIZAR = """
UPDATE verificacao_crmv 
SET status_verificacao = ?, id_admin = ?
WHERE id_veterinario = ?;
"""

EXCLUIR = """
DELETE FROM verificacao_crmv 
WHERE id_veterinario = ?;
"""

OBTER_TODOS_PAGINADO = """
SELECT 
    v.id,
    v.data_verificacao,
    v.status_verificacao,
    u.id_usuario AS id_veterinario,
    u.nome AS nome_veterinario,
    a.id_admin,
    a.nome AS nome_admin,
    a.email AS email_admin
FROM verificacao_crmv v
JOIN usuario u ON v.id_veterinario = u.id_usuario
JOIN administrador a ON v.id_admin = a.id_admin
ORDER BY v.data_verificacao DESC
LIMIT ? OFFSET ?;
"""


OBTER_POR_ID = """
SELECT 
    v.id,
    v.data_verificacao,
    v.status_verificacao,
    u.id_usuario AS id_veterinario,
    u.nome AS nome_veterinario,
    a.id_admin,
    a.nome AS nome_admin
FROM verificacao_crmv v
JOIN usuario u ON v.id_veterinario = u.id_usuario
JOIN administrador a ON v.id_admin = a.id_admin
WHERE v.id = ?;
"""
```

# data\veterinario_model.py

```py
from dataclasses import dataclass

from data.usuario_model import Usuario

@dataclass
class Veterinario(Usuario):
    crmv: str
    verificado: bool
    bio: str
```

# data\veterinario_repo.py

```py
from typing import Optional, List
from data import usuario_repo
from data import veterinario_sql
from data.usuario_model import Usuario
from data.veterinario_model import Veterinario
from data.veterinario_sql import *
from util import get_connection


def criar_tabela_veterinario() -> bool:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de categorias: {e}")
        return False

def inserir_veterinario(vet: Veterinario) -> Optional[int]:
    # Inserir dados do usuário (herdados)
    id_veterinario = usuario_repo.inserir_usuario(vet)
    with get_connection() as conn:
        cursor = conn.cursor()
        # Inserir apenas os atributos exclusivos do veterinário
        cursor.execute(
            veterinario_sql.INSERIR,
            (id_veterinario, vet.crmv, vet.verificado, vet.bio)
        )
        return id_veterinario


def atualizar_veterinario(vet: Veterinario) -> bool:
    usuario_repo.atualizar_usuario(vet)
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR, (
            vet.crmv,
            vet.verificado,
            vet.bio,
            vet.id_usuario
        ))
        return (cursor.rowcount > 0)

def excluir_veterinario(id_veterinario: int) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(EXCLUIR, (id_veterinario,))
        # usuario_repo.EXCLUIR(id_usuario, cursor)
        return (cursor.rowcount > 0)
    


def obter_todos(limit: int, offset: int) -> list[Veterinario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_VETERINARIO_PAGINADO, (limit, offset))
        rows = cursor.fetchall()
        veterinarios = [
            Veterinario(
                id_veterinario=row["id_veterinario"], 
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                telefone=row["telefone"],
                crmv=row["crmv"],
                verificado=row["verificado"],
                bio=row["bio"]
            ) for row in rows
        ]
        return veterinarios
    

def obter_por_id(id_veterinario: int) -> Optional[Veterinario]:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_POR_ID, (id_veterinario,))
        row = cursor.fetchone()
        if row is None:
            return None
        veterinario = Veterinario(
            id_usuario=row["id_veterinario"],
            nome=row["nome"],
            email=row["email"],
            senha=row["senha"],
            telefone=row["telefone"],
            crmv=row["crmv"],
            verificado=row["verificado"],
            bio=row["bio"]
        )
        return veterinario

```

# data\veterinario_sql.py

```py
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS veterinario (
    id_veterinario INTEGER PRIMARY KEY,
    crmv TEXT NOT NULL,
    verificado BOOLEAN DEFAULT 0,
    bio TEXT,
    FOREIGN KEY (id_veterinario) REFERENCES usuario(id_usuario)
);
"""

INSERIR = """
INSERT INTO veterinario (id_veterinario, crmv, verificado, bio)
VALUES (?, ?, ?, ?);
"""

ATUALIZAR = """
UPDATE veterinario SET crmv = ?, verificado = ?, bio = ?
WHERE id_veterinario = ?;
"""

EXCLUIR = """
DELETE FROM veterinario 
WHERE id_veterinario = ?;
"""

OBTER_VETERINARIO_PAGINADO = """
SELECT
    v.id_veterinario,
    u.nome,
    u.email,
    u.telefone,
    v.crmv,
    v.bio
FROM veterinario v
INNER JOIN usuario u ON v.id_veterinario = u.id_usuario
ORDER BY v.id_veterinario
LIMIT ? OFFSET ?;
"""

OBTER_POR_ID = """
SELECT 
    v.id_veterinario,
    u.nome,
    u.email,
    u.senha,
    u.telefone,
    v.crmv,
    v.verificado,
    v.bio
FROM veterinario v
JOIN usuario u ON v.id_veterinario = u.id_usuario
WHERE v.id_veterinario = ?
"""


```

# pytest.ini

```ini
[tool:pytest]
# Diretórios onde o pytest deve procurar por testes
testpaths = tests
# Padrões de arquivos de teste
python_files = test_*.py *_test.py
# Padrões de classes de teste
python_classes = Test*
# Padrões de funções de teste
python_functions = test_*
# Marcadores personalizados
markers =
    slow: marca testes que demoram para executar
    integration: marca testes de integração
    unit: marca testes unitários
# Opções padrão do pytest
addopts = 
    -v
    --strict-markers
    --disable-warnings
    --color=yes
# Filtros de warnings
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
```

# README.md

```md
VetConecta
```

# requirements.txt

```txt
fastapi[standard]
uvicorn[standard]
jinja2
Babel
python-multipart
itsdangerous

# Dependências de teste
pytest
pytest-asyncio
pytest-cov
```

# tests\__init__.py

```py

```

# tests\conftest.py

```py
import pytest
import os
import sys
import tempfile


# Adiciona o diretório raiz do projeto ao PYTHONPATH
# Isso permite importar módulos do projeto nos testes
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Fixture para criar um banco de dados temporário para testes
@pytest.fixture
def test_db():
    # Cria um arquivo temporário para o banco de dados
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    # Configura a variável de ambiente para usar o banco de teste
    os.environ['TEST_DATABASE_PATH'] = db_path
    # Retorna o caminho do banco de dados temporário
    yield db_path    
    # Remove o arquivo temporário ao concluir o teste
    os.close(db_fd)
    if os.path.exists(db_path):
        os.unlink(db_path)

```

# tests\test_administrador_repo.py

```py
import os
import sys
from data.administrador_repo import *
from data.administrador_model import Administrador

class TestAdministradorRepo:
    def test_criar_tabela_administrador(self, test_db):
        #Arrange
        # Act
        resultado = criar_tabela_administrador()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_administrador(self, test_db):
        # Arrange
        criar_tabela_administrador()
        admin_teste = Administrador(0, "Admin Teste", "admin@gmail.com", "12345678")
            # Act
        id_admin_inserido = inserir_administrador(admin_teste)
            # Assert
        admin_db = obter_administrador_por_id(id_admin_inserido)
        assert admin_db is not None, "O administrador inserido não deveria ser None"
        assert admin_db.id_admin == 1, "O administrador inserido deveria ter um ID igual a 1"
        assert admin_db.nome == "Admin Teste", "O nome do administrador inserido não confere"
        assert admin_db.email == "admin@gmail.com", "O email do administrador inserido não confere"
        assert admin_db.senha == "12345678", "A senha do administrador inserido não confere"

    def test_atualizar_administrador(self, test_db):
        # Arrange
        criar_tabela_administrador()
        admin_teste = Administrador(0, "Admin Teste", "admin@gmail.com", "12345678")
        id_admin_inserido = inserir_administrador(admin_teste)
        admin_inserido = obter_administrador_por_id(id_admin_inserido)
            # Act
        admin_inserido.nome = "Admin Atualizado"
        admin_inserido.email = "emailAtualizado@gmail.com"
        admin_inserido.senha = "12345678"
        resultado = atualizar_administrador(admin_inserido)
        # Assert
        assert resultado == True, "A atualização do administrador deveria retornar True"
        admin_db = obter_administrador_por_id(id_admin_inserido)
        assert admin_db.nome == "Admin Atualizado", "O nome do administrador atualizado não confere"
        assert admin_db.email == "emailAtualizado@gmail.com", "O email do administrador atualizado não confere"
        assert admin_db.senha == "12345678", "A senha do administrador atualizado não confere"

    def test_atualizar_senha(self, test_db):
        # Arrange
        criar_tabela_administrador()
        admin_teste = Administrador(0, "Admin Teste", "admin@gmail.com", "12345678")
        id_admin_inserido = inserir_administrador(admin_teste)
        # Act
        nova_senha = "87654321"
        resultado = atualizar_senha(id_admin_inserido, nova_senha)  
        # Assert
        assert resultado == True, "A atualização da senha deveria retornar True"
        admin_db = obter_administrador_por_id(id_admin_inserido)
        assert admin_db.senha == nova_senha, "A senha do administrador atualizado não confere"



    def test_excluir_administrador(self, test_db):
        # Arrange
        criar_tabela_administrador()
        admin_teste = Administrador(0, "Admin Teste", "admin@gmail.com", "12345678")
        id_admin_inserido = inserir_administrador(admin_teste)
        # Act
        resultado = excluir_administrador(id_admin_inserido)
        # Assert    
        assert resultado == True, "A exclusão do administrador deveria retornar True"
        admin_excluido = obter_administrador_por_id(id_admin_inserido)  
        assert admin_excluido == None, "O administrador excluído deveria ser None"


    def test_obter_todos_administradores(self, test_db):
        # Arrange
        criar_tabela_administrador()
        admin1 = Administrador(0, "Admin 1", "admin@gmail.com", "12345678")
        admin2 = Administrador(0, "Admin 2", "admin@@gmail.com", "87654321")
        inserir_administrador(admin1)
        inserir_administrador(admin2)   
        # Act
        administradores = obter_administradores_paginado(0, 10)

        # Assert
        assert len(administradores) == 2, "Deveria haver 2 administradores"
        assert administradores[0].nome == "Admin 1", "O nome do primeiro administrador não confere"
        assert administradores[1].nome == "Admin 2", "O nome do segundo administrador não confere"

    def test_obter_administrador_por_id(self, test_db):
        # Arrange
        criar_tabela_administrador()
        admin_teste = Administrador(0, "Admin Teste", "admin@gmail.com", "12345678")
        id_admin_inserido = inserir_administrador(admin_teste)
        # Act   
        admin_obtido = obter_administrador_por_id(id_admin_inserido)
        # Assert
        assert admin_obtido is not None, "O administrador obtido não deveria ser None"
        assert admin_obtido.id_admin == id_admin_inserido, "O ID do administrador obtido não confere"
        assert admin_obtido.nome == admin_teste.nome, "O nome do administrador obtido não confere"
        assert admin_obtido.email == admin_teste.email, "O email do administrador obtido não confere"
        assert admin_obtido.senha == admin_teste.senha, "A senha do administrador obtido não confere"


```

# tests\test_categoria_artigo_repo.py

```py
import os
import sys
from data.categoria_artigo_repo import *
from data.categoria_artigo_model import CategoriaArtigo

class TestCategoriaArtigoRepo:
    def test_criar_tabela(self, test_db):
        #Arrange
        # Act
        resultado = criar_tabela_categoria_artigo()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_categoria(self, test_db):
        # Arrange
        criar_tabela_categoria_artigo()
        categoria_teste = CategoriaArtigo(0,"Categoria Teste", "Descrição Teste")
        # Act
        id_categoria_inserida = inserir_categoria(categoria_teste)
        # Assert
        categoria_db = obter_categoria_por_id(id_categoria_inserida)
        assert categoria_db is not None, "A categoria inserida não deveria ser None"
        assert categoria_db.id == 1, "A categoria inserida deveria ter um ID igual a 1"
        assert categoria_db.nome == "Categoria Teste", "O nome da categoria inserida não confere"
        assert categoria_db.descricao == "Descrição Teste", "O campo de descrição não pode ser vazio"

    def test_atualizar_categoria(self, test_db):
        # Arrange
        criar_tabela_categoria_artigo()
        categoria_teste = CategoriaArtigo(0, "Categoria Teste", "Descrição Teste")
        id_categoria_inserida = inserir_categoria(categoria_teste)
        categoria_inserida = obter_categoria_por_id(id_categoria_inserida)
        # Act
        categoria_inserida.nome = "Categoria Atualizada"
        categoria_inserida.descricao = "Descrição Atualizada"
        resultado = atualizar_categoria(categoria_inserida)
        # Assert
        assert resultado == True, "A atualização da categoria deveria retornar True"
        categoria_db = obter_categoria_por_id(id_categoria_inserida)
        assert categoria_db.nome == "Categoria Atualizada", "O nome da categoria atualizada não confere"
        assert categoria_db.descricao == "Descrição Atualizada", "A descrição da categoria atualizada não confere"


    def test_excluir_categoria(self, test_db):
        # Arrange
        criar_tabela_categoria_artigo()
        categoria_teste = CategoriaArtigo(0, "Categoria Teste", "Descrição Teste")
        id_categoria_inserida = inserir_categoria(categoria_teste)
        # Act
        resultado = excluir_categoria(id_categoria_inserida)
        # Assert
        assert resultado == True, "A exclusão da categoria deveria retornar True"
        categoria_excluida = obter_categoria_por_id(id_categoria_inserida)
        assert categoria_excluida == None, "A categoria excluída deveria ser None"

    def test_obter_todas_categorias(self, test_db):
        # Arrange
        criar_tabela_categoria_artigo()
        categoria1 = CategoriaArtigo(0, "Categoria 1", "Descrição 1")
        categoria2 = CategoriaArtigo(1, "Categoria 2", "Descrição 2")
        inserir_categoria(categoria1)
        inserir_categoria(categoria2)
        # Act
        categorias = obter_categorias_paginado(0, 5)
        # Assert
        assert len(categorias) == 2, "Deveria retornar duas categorias"
        assert categorias[0].nome == "Categoria 1", "O nome da primeira categoria não confere"
        assert categorias[1].nome == "Categoria 2", "O nome da segunda categoria não confere"

    def test_obter_categoria_por_id(self, test_db):
        # Arrange
        criar_tabela_categoria_artigo()
        categoria_teste = CategoriaArtigo(0, "Categoria Teste", "Descrição Teste")
        id_categoria_inserida = inserir_categoria(categoria_teste)
        # Act
        categoria_db = obter_categoria_por_id(id_categoria_inserida)
        # Assert
        assert categoria_db is not None, "A categoria obtida não deveria ser diferente de None"
        assert categoria_db.id == id_categoria_inserida, "O ID da categoria obtida não confere"
        assert categoria_db.nome == categoria_teste.nome, "O nome da categoria obtida não confere"
        


```

# tests\test_chamado_repo.py

```py
import os
import sys

from data.administrador_model import *
from data.administrador_repo import *
from data.chamado_model import Chamado
from data.chamado_repo import *
from data.usuario_model import Usuario
from data.usuario_repo import *
from data.usuario_sql import *
from data.administrador_repo import criar_tabela_administrador, inserir_administrador
from data.administrador_model import Administrador

class TestChamadoRepo:
    def test_criar_tabelas(self, test_db):
        #Arrange
        # Act
        resultado = criar_tabela()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_chamado(self, test_db):
        # Arrange
        # Cria tabelas necessárias no banco temporário
        criar_tabela_usuario()
        criar_tabela_administrador()
        criar_tabela()  # cria tabela chamado

        # Insere usuário dummy e obtém ID
        usuario_teste = Usuario(0, "Usuário Teste", "teste@teste.com", "12345678", "11999999999")
        id_usuario = inserir_usuario(usuario_teste)

        # Insere administrador dummy e obtém ID

        admin_teste = Administrador(0, "Admin Teste", "admin@teste.com", "12345678")
        id_admin = inserir_administrador(admin_teste)

        # Cria chamado usando IDs válidos
        chamado_teste = Chamado(
            id=0,
            id_usuario=id_usuario,
            id_admin=id_admin,
            titulo="Título Chamado",
            descricao="Descrição",
            status="aberto",
            data="2025-06-30"
        )

        # Act
        id_chamado_inserido = inserir_chamado(chamado_teste)

        # Assert
        chamado_db = obter_chamado_por_id(id_chamado_inserido)
        assert chamado_db is not None, "O chamado inserido não deveria ser None"
        assert chamado_db.id_usuario == id_usuario, "O id do usuário inserido não confere"
        assert chamado_db.id_admin == id_admin, "O id do administrador inserido não confere"
        assert chamado_db.titulo == "Título Chamado", "O título do chamado inserido não confere"
        assert chamado_db.descricao == "Descrição", "A descrição do chamado inserido não confere"
        assert chamado_db.status == "aberto", "O status do chamado inserido não confere"
        assert chamado_db.data == "2025-06-30", "A data do chamado inserido não confere"


    def test_atualizar_status_chamado(self, test_db):
        # Arrange
        # Cria tabelas necessárias no banco temporário
        criar_tabela_usuario()
        criar_tabela_administrador()
        criar_tabela()  # cria tabela chamado

        # Insere usuário de teste e obtém ID
        from data.usuario_model import Usuario
        usuario_teste = Usuario(0, "Usuário Teste", "teste@teste.com", "12345678", "11999999999")
        id_usuario = inserir_usuario(usuario_teste)

        # Insere administrador de teste e obtém ID
        from data.administrador_model import Administrador
        admin_teste = Administrador(0, "Admin Teste", "admin@teste.com", "12345678")
        id_admin = inserir_administrador(admin_teste)

        # Cria chamado com IDs válidos
        chamado_teste = Chamado(
            id=0,
            id_usuario=id_usuario,
            id_admin=id_admin,
            titulo="Título Chamado",
            descricao="Descrição",
            status="aberto",
            data="2025-06-30"
        )
        id_chamado_inserido = inserir_chamado(chamado_teste)

        # Act
        resultado = atualizar_status_chamado(id_chamado_inserido, "resolvido")

        # Assert
        assert resultado == True, "A atualização do status deveria retornar True"
        chamado_db = obter_chamado_por_id(id_chamado_inserido)
        assert chamado_db.status == "resolvido", "O status do chamado atualizado não confere"

    def test_excluir_chamado(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_administrador()
        criar_tabela()

        from data.usuario_model import Usuario
        from data.administrador_model import Administrador

        # Insere usuário de teste e obtém ID
        usuario_teste = Usuario(0, "Usuário Teste", "teste@teste.com", "12345678", "11999999999")
        id_usuario = inserir_usuario(usuario_teste)

        # Insere administrador de teste e obtém ID
        admin_teste = Administrador(0, "Admin Teste", "admin@teste.com", "12345678")
        id_admin = inserir_administrador(admin_teste)

        # Insere chamado com IDs válidos
        chamado_teste = Chamado(
            id=0,
            id_usuario=id_usuario,
            id_admin=id_admin,
            titulo="Título Chamado",
            descricao="Descrição",
            status="aberto",
            data="2025-06-30"
        )
        id_chamado = inserir_chamado(chamado_teste)

        # Act
        resultado = excluir_chamado(id_chamado)

        # Assert
        assert resultado == True, "A exclusão do chamado deveria retornar True"
        chamado_db = obter_chamado_por_id(id_chamado)
        assert chamado_db is None, "O chamado deveria ter sido excluído"

    def test_obter_todos_chamados(self, test_db):
        # Arrange: cria tabelas necessárias
        criar_tabela_usuario()
        criar_tabela_administrador()
        criar_tabela()

        from data.usuario_model import Usuario
        from data.administrador_model import Administrador

        # Insere usuário e administrador de teste
        usuario_teste = Usuario(0, "Usuário Teste", "teste@teste.com", "12345678", "11999999999")
        id_usuario = inserir_usuario(usuario_teste)

        admin_teste = Administrador(0, "Admin Teste", "admin@teste.com", "12345678")
        id_admin = inserir_administrador(admin_teste)

        # Cria dois chamados válidos
        chamado1 = Chamado(
            id=0,
            id_usuario=id_usuario,
            id_admin=id_admin,
            titulo="Chamado 1",
            descricao="Descrição 1",
            status="aberto",
            data="2025-06-30"
        )
        chamado2 = Chamado(
            id=0,
            id_usuario=id_usuario,
            id_admin=id_admin,
            titulo="Chamado 2",
            descricao="Descrição 2",
            status="aberto",
            data="2025-06-30"
        )

        inserir_chamado(chamado1)
        inserir_chamado(chamado2)

        # Act
        chamados = obter_todos_chamados_paginado(0, 5)

        # Assert
        assert len(chamados) == 2, "Deveria retornar dois chamados"
        assert chamados[0].titulo == "Chamado 1", "O título do primeiro chamado não confere"
        assert chamados[1].titulo == "Chamado 2", "O título do segundo chamado não confere"



    def test_obter_chamado_por_id(self, test_db):
        # Arrange
        # Criar todas as tabelas necessárias
        criar_tabela_usuario()
        criar_tabela_administrador()
        criar_tabela()

        # Inserir o usuário (id_usuario=1)
        usuario = Usuario(
            id_usuario=0,
            nome="Usuario Teste",
            email="usuario@teste.com",
            senha="12345678",
            telefone="11999999999"
        )
        id_usuario = inserir_usuario(usuario)

        # Inserir o administrador (id_admin=1)
        admin = Administrador(
            id_admin=0,
            nome="Admin Teste",
            email="admin@teste.com",
            senha="12345678"
        )
        id_admin = inserir_administrador(admin)

        # Criar o chamado referenciando os IDs válidos
        chamado_teste = Chamado(
            id=0,
            id_usuario=id_usuario,
            id_admin=id_admin,
            titulo="Chamado Teste",
            descricao="Descrição Teste",
            status="aberto",
            data="2024-01-01"
        )

        id_chamado_inserido = inserir_chamado(chamado_teste)

        # Act
        chamado_db = obter_chamado_por_id(id_chamado_inserido)

        # Assert
        assert chamado_db is not None
        assert chamado_db.id == id_chamado_inserido
        assert chamado_db.titulo == chamado_teste.titulo
        assert chamado_db.descricao == chamado_teste.descricao
        assert chamado_db.status == chamado_teste.status
        assert chamado_db.data == chamado_teste.data
        assert chamado_db.id_usuario == id_usuario
        assert chamado_db.id_admin == id_admin






    
```

# tests\test_comentario_repo.py

```py
import os
import sys
from data.categoria_artigo_model import CategoriaArtigo
from data.comentario_model import Comentario
from data.comentario_repo import *
from data.usuario_repo import criar_tabela_usuario, inserir_usuario
from data.usuario_model import Usuario
from data.veterinario_model import Veterinario


class TestComentarioRepo:
    def test_criar_tabela(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela()
        # Assert
        assert resultado == True, "A criação da tabela de comentários deveria retornar True"

    
    def test_inserir_comentario(self, test_db):
        # 1. Criar tabelas necessárias
        criar_tabela_usuario()
        criar_tabela_veterinario()
        criar_tabela_categoria_artigo()
        criar_tabela_artigo()
        criar_tabela_comentario()

        # 2. Inserir usuário
        usuario = Usuario(
            id_usuario=0,
            nome="Usuario Teste",
            email="usuario@teste.com",
            senha="12345678",
            telefone="11999999999"
        )
        id_usuario = inserir_usuario(usuario)

        # 3. Inserir veterinário
        veterinario = Veterinario(
            id_veterinario=1,
            nome="Vet Teste",
            email="vet@teste.com",
            senha="12345678",
            telefone="11999999999",
            crmv="12345",
            verificado=True,
            bio="Bio do veterinario"
        )
        inserir_veterinario(veterinario)

        # 4. Inserir categoria
        categoria = CategoriaArtigo(
            id=0,
            nome="Categoria Teste",
            descricao="Descrição da categoria"
        )
        id_categoria = inserir_categoria(categoria)

        # 5. Inserir artigo
        artigo = PostagemArtigo(
            id=0,
            veterinario=veterinario,
            titulo="Artigo Teste",
            conteudo="Conteúdo do artigo",
            categoria_artigo=categoria,
            data_publicacao="2024-01-01",
            visualizacoes=0
        )
        id_artigo = inserir_artigo(artigo)

        # 6. Criar o comentário
        comentario = Comentario(
            id=0,
            id_usuario=id_usuario,
            id_artigo=id_artigo,
            texto="Este é um comentário de teste",
            data_comentario=None,
            data_moderacao=None
        )

        # 7. Inserir comentário
        id_comentario = inserir_comentario(comentario)

        # 8. Assert: Verificar se inseriu corretamente
        assert id_comentario is not None, "A inserção do comentário deveria retornar um ID válido"

        comentarios = obter_todos_paginado(10, 0)
        assert len(comentarios) > 0, "Deveria haver pelo menos 1 comentário"

        comentario_db = comentarios[0]
        assert comentario_db.texto == comentario.texto, "O texto do comentário não confere"
        assert comentario_db.usuario.nome == usuario.nome, "O nome do usuário não confere"
        assert comentario_db.artigo.titulo == artigo.titulo, "O título do artigo não confere"
        assert comentario_db.data_comentario is not None, "A data do comentário não deveria ser None"


    def test_atualizar(self, test_db):
        # Arrange
        criar_tabela()
        comentario_teste = Comentario(
            id=1,
            id_usuario=1,  
            id_artigo=1,   
            texto="Comentário original"
        )
        inserir(comentario_teste)
        comentario_teste.texto = "Comentário atualizado"
        # Act
        resultado = atualizar(comentario_teste)
        # Assert
        assert resultado == True, "A atualização do comentário deveria retornar True"
        comentario_db = obter_todos_paginado(10, 0)[0]
        assert comentario_db.texto == "Comentário atualizado", "O texto do comentário atualizado não confere"
```

# tests\test_denuncia_repo.py

```py
import os
import sys
from data.administrador_model import Administrador
from data.denuncia_repo import *
from data.usuario_repo import *
from data.administrador_repo import *
from data.denuncia_model import Denuncia
from data.usuario_model import Usuario

class TestDenunciaRepo:
    def test_criar_tabela_denuncia(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_denuncia()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_denuncia(self, test_db):
        # Arrange
        criar_tabela_usuario()       # Certifique que a tabela usuario existe
        criar_tabela_administrador() # Certifique que a tabela administrador existe
        criar_tabela_denuncia()      # Crie a tabela denuncia
        
        # Insere um usuário para a FK id_usuario
        usuario_id = inserir_usuario(Usuario(
            id_usuario=0, nome="Usuário Teste", email="teste@teste.com", senha="12345678", telefone="12345678900"
        ))
    
        # Insere um administrador para a FK id_admin
        admin_id = inserir_administrador(Administrador(
            id_admin=0, nome="Admin Teste", email="admin@teste.com", senha="admin123"
        ))
        
        # Cria uma denúncia com os IDs válidos
        denuncia_teste = Denuncia(
            id_denuncia=0,
            id_usuario=usuario_id,
            id_admin=admin_id,
            motivo="Motivo Teste",
            data_denuncia="2025-06-30",
            status="pendente"  
        )
        
        # Act
        id_denuncia_inserida = inserir_denuncia(denuncia_teste)
        
        # Assert
        denuncia_db = obter_denuncia_por_id(id_denuncia_inserida)
        assert denuncia_db is not None, "A denúncia inserida não deveria ser None"
        assert denuncia_db.id_usuario == usuario_id, "O ID do usuário da denúncia inserida não confere"
        assert denuncia_db.id_denuncia == 1, "A denúncia inserida deveria ter um ID igual a 1"
        assert denuncia_db.motivo == "Motivo Teste", "O motivo da denuncia da denúncia inserida não confere"
        assert denuncia_db.status == "pendente", "O status da denúncia inserida não confere"

    def test_atualizar_denuncia(self, test_db):
        # Arrange
        criar_tabela_usuario()       # Certifique que a tabela usuario existe
        criar_tabela_administrador() # Certifique que a tabela administrador existe
        criar_tabela_denuncia()      # Crie a tabela denuncia   
        # Insere um usuário para a FK id_usuario
        usuario_id = inserir_usuario(Usuario(id_usuario=0, nome="Usuário Teste", email="usuario@gmail.com", senha="12345678", telefone="12345678900"))
        # Insere um administrador para a FK id_admin
        admin_id = inserir_administrador(Administrador(id_admin=0, nome="Admin Teste", email="admin@gmail.com", senha="admin123"))
        # Insere uma denúncia
        denuncia_id = inserir_denuncia(Denuncia(
            id_denuncia=0,
            id_usuario=usuario_id,
            id_admin=admin_id,
            motivo="Motivo Teste",
            data_denuncia="2025-30-06",
            status="pendente"
        ))
        # Atualiza a denúncia
        denuncia_atualizada = Denuncia(
            id_denuncia=denuncia_id,
            id_usuario=usuario_id,
            id_admin=admin_id,
            motivo="Motivo Atualizado",
            data_denuncia="2025-01-07",
            status="aprovada"
        )
        # Act
        resultado = atualizar_denuncia(denuncia_atualizada)
        # Assert
        assert resultado == True, "A atualização da denúncia deveria retornar True"
        denuncia_db = obter_denuncia_por_id(denuncia_id)
        assert denuncia_db is not None, "A denúncia atualizada não deveria ser None"    
        assert denuncia_db.id_denuncia == denuncia_id, "O ID da denúncia atualizada não confere"
        assert denuncia_db.motivo == "Motivo Atualizado", "O motivo da denúncia atualizada não confere"
        assert denuncia_db.data_denuncia == "2025-01-07", "A data da denúncia atualizada não confere"
        assert denuncia_db.status == "aprovada", "O status da denúncia atualizada não confere"

    def test_excluir_denuncia(self, test_db):
        # Arrange
        criar_tabela_usuario()       # Certifique que a tabela usuario existe
        criar_tabela_administrador() # Certifique que a tabela administrador existe
        criar_tabela_denuncia()      # Crie a tabela denuncia
        # Insere um usuário para a FK id_usuario
        usuario_id = inserir_usuario(Usuario(id_usuario=0, nome="Usuário Teste", email="usuario@gmail.com", senha="12345678", telefone="12345678900"))
        # Insere um administrador para a FK id_admin
        admin_id = inserir_administrador(Administrador(id_admin=0, nome="Admin Teste", email="admin@gmail.com", senha="admin123"))
        # Insere uma denúncia
        denuncia_id = inserir_denuncia(Denuncia(
            id_denuncia=0,
            id_usuario=usuario_id,
            id_admin=admin_id,
            motivo="Motivo Teste",
            data_denuncia="2025-06-30",
            status="pendente"
        ))
        # Act
        resultado = excluir_denuncia(denuncia_id)
        # Assert
        assert resultado == True, "A exclusão da denúncia deveria retornar True"
        denuncia_db = obter_denuncia_por_id(denuncia_id)
        assert denuncia_db is None, "A denúncia excluída deveria ser None"

    def test_obter_todas_denuncias_paginadas(self, test_db):
        # Arrange
        criar_tabela_usuario()       # Certifique que a tabela usuario existe
        criar_tabela_administrador() # Certifique que a tabela administrador existe
        criar_tabela_denuncia()      # Crie a tabela denuncia   
        # Insere um usuário para a FK id_usuario
        usuario_id = inserir_usuario(Usuario(id_usuario=0, nome="Usuário Teste", email="usuario@gmail.com", senha="12345678", telefone="12345678900"))
        # Insere um administrador para a FK id_admin
        admin_id = inserir_administrador(Administrador(id_admin=0, nome="Admin Teste", email="admin@gmail.com", senha="admin123"))
        # Insere uma denúncia
        inserir_denuncia(Denuncia(
            id_denuncia=0,
            id_usuario=usuario_id,
            id_admin=admin_id,
            motivo="Motivo Teste 1",
            data_denuncia="2025-06-30",
            status="pendente"
        ))
        inserir_denuncia(Denuncia(
            id_denuncia=0,
            id_usuario=usuario_id,
            id_admin=admin_id,
            motivo="Motivo Teste 2",
            data_denuncia="2025-07-01",
            status="aprovada"
        ))
        inserir_denuncia(Denuncia(
            id_denuncia=0,
            id_usuario=usuario_id,
            id_admin=admin_id,
            motivo="Motivo Teste 3",
            data_denuncia="2025-07-02",
            status="rejeitada"
        ))
        # Act
        denuncias = obter_todas_denuncias_paginadas(limite=2, offset=0)
        # Assert    
        assert len(denuncias) == 2, "Deveria retornar 2 denúncias"
        motivos = [d.motivo for d in denuncias]
        assert "Motivo Teste 1" in motivos, "Motivo Teste 1 não encontrado"
        assert "Motivo Teste 2" in motivos, "Motivo Teste 2 não encontrado"


    

    def test_obter_denuncia_por_id(self, test_db):
        # Arrange
        criar_tabela_usuario()       # Certifique que a tabela usuario existe
        criar_tabela_administrador() # Certifique que a tabela administrador existe
        criar_tabela_denuncia()      # Crie a tabela denuncia
        # Insere um usuário para a FK id_usuario
        usuario_id = inserir_usuario(Usuario(id_usuario=0, nome="Usuário Teste", email="emailteste@gmail.com",senha="12345678", telefone="12345678900"))
        # Insere um administrador para a FK id_admin
        admin_id = inserir_administrador(Administrador(id_admin=0, nome="Admin Teste", email="adminTeste@gmail.com", senha="admin123"))
        # Insere uma denúncia
        denuncia_id = inserir_denuncia(Denuncia(
            id_denuncia=0,
            id_usuario=usuario_id,
            id_admin=admin_id,
            motivo="Motivo Teste",
            data_denuncia="2025-06-30",
            status="pendente"
        ))
        # Act
        denuncia_obtida = obter_denuncia_por_id(denuncia_id)
        # Assert
        assert denuncia_obtida is not None, "A denúncia obtida não deveria ser None"
        assert denuncia_obtida.id_denuncia == denuncia_id, "O ID da denúncia obtida não confere"
        assert denuncia_obtida.id_usuario == usuario_id, "O ID do usuário da denúncia obtida não confere"
        assert denuncia_obtida.id_admin == admin_id, "O ID do administrador da denúncia obtida não confere"
        assert denuncia_obtida.motivo == "Motivo Teste", "O motivo da denúncia obtida não confere"
        assert denuncia_obtida.data_denuncia == "2025-06-30", "A data da denúncia obtida não confere"
        assert denuncia_obtida.status == "pendente", "O status da denúncia obtida não confere"

 


    
      

```

# tests\test_postagem_artigo.py

```py
import os
import sys
from data.categoria_artigo_repo import *
from data.categoria_artigo_model import CategoriaArtigo
from data.postagem_artigo_repo import *
from data.postagem_artigo_model import PostagemArtigo
from data.veterinario_repo import *

class TestPostagemArtigoRepo:
    def test_criar_tabela(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_postagem_artigo(self, test_db):
        # Arrange
        criar_tabela_tutor()
        criar_tabela_categoria_artigo()
        criar_tabela()

        conn = get_connection()
        cursor = conn.cursor()

        # Inserir veterinário
        cursor.execute(
            "INSERT INTO veterinario (id_usuario, nome, email, senha, telefone, crmv, verificado, bio) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (1, "Dr. João", "joao@email.com", "123", "999999999", "CRMV123", True, "Especialista em felinos")
        )

        # Inserir categoria
        cursor.execute(
            "INSERT INTO categoria_artigo (id, nome, descricao) VALUES (?, ?, ?)",
            (1, "Saúde", "Descrição")
        )

        conn.commit()
        conn.close() 
        postagem_teste = postagem = PostagemArtigo(0,Veterinario(id_usuario=1,nome="Dr. João",email="joao@email.com",senha="123",telefone="999999999",crmv="CRMV123",verificado=True,bio="Especialista em felinos"),"Título","Conteúdo",CategoriaArtigo(1, "Saúde","Descrição"),"2025-06-30",0)
        # Act
        id_postagem_criada = inserir(postagem_teste) 
        # Assert
        postagem_db = obter_por_id(id_postagem_criada)
        assert postagem_db is not None, "A postagem retornada não deveria ser None"
        assert postagem_db.id == 1, "O ID da postagem criada deveria ser 1"
        assert postagem_db.titulo == "Título", "O título da postagem não confere"
        assert postagem_db.conteudo == "Conteúdo", "O conteúdo da postagem não confere"
        assert postagem_db.veterinario.nome == "Nome do Veterinário", "O nome do veterinário não confere"
        assert postagem_db.categoria_artigo.nome == "Categoria", "A categoria do artigo não confere"
        assert postagem_db.data_publicacao == "Data", "A data de publicação da postagem não confere"
        assert postagem_db.visualizacoes == 0, "O número de visualizações deveria ser 0"
                
```

# tests\test_tutor_repo.py

```py
from data.tutor_model import Tutor
from data.tutor_repo import *
from data.usuario_repo import *
from data.usuario_model import Usuario



class TestTutorRepo:
    def test_criar_tabela(self, test_db):
        # Act
        resultado = criar_tabela_tutor()
        # Assert
        assert resultado == True, "A criação da tabela deveria retornar True"

    def test_inserir_tutor(self, test_db):
        # Arrange
        criar_tabela_tutor()
        tutor_teste = Tutor(1, "Tutor Teste", "tutor@gmail.com", "12345678", "123456789")
        
            # Act
        id_tutor_inserido = inserir_tutor(tutor_teste)
            # Assert
        tutor_obtido = obter_tutor_por_id(id_tutor_inserido)
        assert tutor_obtido is not None, "O tutor inserido não deveria ser None"
        assert tutor_obtido.id_usuario == 1, "O tutor inserido deveria ter um ID igual a 1"
        assert tutor_obtido.nome == "Tutor Teste", "O nome do tutor inserido não confere"
        assert tutor_obtido.email == "tutor@gmail.com", "O email do tutor inserido não confere"
        assert tutor_obtido.senha == "12345678", "A senha do tutor inserido não confere"
        assert tutor_obtido.telefone == "123456789", "O telefone do tutor inserido não confere"


    def test_inserir_administrador(self, test_db):
        # Arrange
        criar_tabela_administrador()
        admin_teste = Administrador(0, "Admin Teste", "admin@gmail.com", "12345678")
            # Act
        id_admin_inserido = inserir_administrador(admin_teste)
            # Assert
        admin_db = obter_administrador_por_id(id_admin_inserido)
        assert admin_db is not None, "O administrador inserido não deveria ser None"
        assert admin_db.id_admin == 1, "O administrador inserido deveria ter um ID igual a 1"
        assert admin_db.nome == "Admin Teste", "O nome do administrador inserido não confere"
        assert admin_db.email == "admin@gmail.com", "O email do administrador inserido não confere"
        assert admin_db.senha == "12345678", "A senha do administrador inserido não confere"



    def test_atualizar_tutor(self, test_db):
        # Arrange
        criar_tabela_tutor()
        tutor_exemplo = Tutor(1, "Tutor Teste", "tutor@gmail.com", "12345678", "123456789")
        id_tutor_inserido = inserir_tutor(tutor_exemplo)
        tutor_inserido = obter_tutor_por_id(id_tutor_inserido)
        # Act
        tutor_inserido.nome = "Tutor Atualizado"
        tutor_inserido.email = "email Atualizada"
        tutor_inserido.senha = "12345678"
        tutor_inserido.telefone = "123456789"
        resultado = atualizar_tutor(tutor_obtido)
        # Assert
        assert resultado == True, "A atualização do tutor deveria retornar True"
        tutor_obtido = obter_tutor_por_id(tutor_inserido)
        assert tutor_obtido.nome == "Tutor Atualizado", "O nome do tutor atualizado não confere"
        assert tutor_obtido.email == "Email Atualizada", "O email do tutor atualizado não confere"
        assert tutor_obtido.senha == "Senha Atualizada", "A senha do tutor atualizado não confere"
        assert tutor_obtido.telefone == "Telefone Atualizado", "O telefone do tutor atualizado não confere"
    
    def test_atualizar_senha(self, test_db):
        criar_tabela_tutor
        tutor_exemplo = Tutor(1, "Tutor Teste", "tutor@gmail.com", "12345678", "123456789")
        id_tutor_inserido = inserir_tutor(tutor_exemplo)
        #Act
        nova_senha ="87654321"
        resultado = atualizar_senha_usuario(id_tutor_inserido, nova_senha)
        #Assert
        assert resultado == True, "A atualização da senha deveria retornar True"
        tutor_db = obter_tutor_por_id(id_tutor_inserido)
        assert tutor_db.senha == nova_senha, "A senha do tutor atualizado não confere"

    def test_excluir_tutor(self, test_db):
        # Arrange
        tutor_exemplo = Tutor(1, "Tutor Teste", "tutor@gmail.com", "12345678", "123456789")
        id_tutor_inserido = inserir_tutor(tutor_exemplo)
        # Act
        resultado = excluir_tutor(id_tutor_inserido)
        # Assert
        assert resultado == True, "A exclusão do tutor deveria retornar True"
        tutor_excluido = obter_tutor_por_id(id_tutor_inserido)
        assert tutor_excluido == None, "O tutor excluído deveria ser None"

    def test_obter_todos_tutores(self, test_db):
        # Arrange
        criar_tabela_tutor
        tutor1 = Tutor(1, "Tutor 1", "tutor1@gmail.com", "12345678", "123456789")
        tutor2 = Tutor(2, "Tutor 2", "tutor2@gmail.com", "12345678", "123456789")
        inserir_tutor(tutor1)
        inserir_tutor(tutor2)
        # Act
        tutores = obter_todos_tutores_paginado()
        # Assert
        assert len(tutores) == 2, "Deveria retornar duas categorias"
        assert tutores[0].nome == "Tutor 1", "O nome do primeiro tutor não confere"
        assert tutores[1].nome == "Tutor 2", "O nome do segundo tutor não confere"
    
    def test_obter_tutor_por_id(self, test_db):
        #Arrange
        criar_tabela_tutor()
        tutor_teste = (1, "Tutor Teste", "tutor@gmail.com", "12345678", "123456789")
        id_tutor_inserido = inserir_tutor(tutor_teste)
        # Act
        tutor_obtido = obter_tutor_por_id(id_tutor_inserido)
        # Assert
        assert tutor_obtido.nome == "Tutor Atualizado", "O nome do tutor atualizado não confere"
        assert tutor_obtido.email == "Email Atualizada", "O email do tutor atualizado não confere"
        assert tutor_obtido.senha == "Senha Atualizada", "A senha do tutor atualizado não confere"
        assert tutor_obtido.telefone == "Telefone Atualizado", "O telefone do tutor atualizado não confere"        
```

# tests\test_usuario_repo.py

```py
import os
import sys
from data.usuario_repo import *
from data.usuario_model import Usuario

class TestUsuarioRepo:
    def test_criar_tabela(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_usuario()
        # Assert
        assert resultado == True, "A criação da tabela de usuários deveria retornar True"


    def test_inserir_usuario(self, test_db):
        #Arrange 
        criar_tabela_usuario()

        usuario_teste = Usuario(
            id_usuario=1, 
            nome="Usuário Teste",
            email="teste@teste.com", 
            senha="12345678", 
            telefone="12345678900"  
        )
        #Act
        id_usuario_inserido = inserir_usuario(usuario_teste)
        #Assert
        usuario_db = obter_usuario_por_id(id_usuario_inserido)
        assert usuario_db is not None, "O usuario inserido não deveria ser None"
        assert usuario_db.id_usuario == 1, "O usuario inserido deveria ter um ID igual a 1"
        assert usuario_db.nome == "Usuário Teste", "O nome do usuario inserido não confere"
        assert usuario_db.email == "teste@teste.com", "O email do usuario não confere"
        assert usuario_db.senha == "12345678", "A senha do usuario não confere"
        assert usuario_db.telefone == "12345678900", "O telefone do usuario não confere"

    def test_atualizar_usuario(self, test_db):
        #Arrange
        criar_tabela_usuario()
        usuario_teste = Usuario(
            id_usuario=1, 
            nome="Usuário Teste",
            email="teste@teste.com", 
            senha="12345678", 
            telefone="12345678900"  
        )
        id_usuario_inserido = inserir_usuario(usuario_teste)
        usuario_inserido = obter_usuario_por_id(id_usuario_inserido)
        #Act
        usuario_inserido.nome = "Usuário Teste"
        usuario_inserido.email = "teste@teste.com"
        usuario_inserido.senha = "12345678"
        usuario_inserido.telefone = "12345678900"
        resultado = atualizar_usuario(usuario_inserido)
        #Assert
        assert resultado == True, "A atualização da categoria deveria retornar True"
        usuario_db = obter_usuario_por_id(id_usuario_inserido)
        assert usuario_db.nome == "Usuário Teste", "O nome do usuario inserido não confere"
        assert usuario_db.email == "teste@teste.com", "O email do usuario não confere"
        assert usuario_db.senha == "12345678", "A senha do usuario não confere"
        assert usuario_db.telefone == "12345678900", "O telefone do usuario não confere"


    def test_atualizar_senha_usuario(self, test_db):
        # Arrange
        criar_tabela_usuario()
        usuario_teste = Usuario(0, "Teste", "teste@email.com", "senha_antiga", "11999999999")
        id_usuario = inserir_usuario(usuario_teste)
        
        # Act
        nova_senha = "senha_nova123"
        resultado = atualizar_senha_usuario(id_usuario, nova_senha)
        
        # Assert
        assert resultado is True, "A atualização da senha deveria retornar True"
        usuario_atualizado = obter_usuario_por_id(id_usuario)
        assert usuario_atualizado.senha == nova_senha, "A senha do usuário não foi atualizada corretamente"

    def test_excluir_usuario(self, test_db):
        # Arrange
        criar_tabela_usuario()
        usuario_teste = Usuario(
            id_usuario=1, 
            nome="Usuário Teste",
            email="teste@teste.com", 
            senha="12345678", 
            telefone="12345678900"  
        )
        id_usuario_inserido = inserir_usuario(usuario_teste)
        # Act
        resultado = excluir_usuario(id_usuario_inserido)
        # Assert
        assert resultado == True, "A exclusão do usuário deveria retornar True"
        usuario_excluido = obter_usuario_por_id(id_usuario_inserido)
        assert usuario_excluido == None, "O usuário excluído deveria ser None"
    
    def test_obter_todos_usuarios_paginado(self, test_db):
        # Arrange
        criar_tabela_usuario()
        usuario1 = Usuario(0, "Usuário 1", "u1@email.com", "senha1", "1111111111")
        usuario2 = Usuario(0, "Usuário 2", "u2@email.com", "senha2", "2222222222")
        inserir_usuario(usuario1)
        inserir_usuario(usuario2)

        # Act
        usuarios = obter_todos_usuarios_paginado(limite=10, offset=0)

        # Assert
        assert len(usuarios) == 2, "Deveria retornar dois usuários"
        assert usuarios[0].nome == "Usuário 1", "O nome do primeiro usuário não confere"
        assert usuarios[1].nome == "Usuário 2", "O nome do segundo usuário não confere"


    def test_obter_usuario_por_id(self, test_db):
        # Arrange
        criar_tabela_usuario()
        usuario_teste = Usuario(0, "Teste", "teste@email.com", "senha123", "11999999999")
        id_usuario_inserido = inserir_usuario(usuario_teste)

        # Act
        usuario_db = obter_usuario_por_id(id_usuario_inserido)

        # Assert
        assert usuario_db is not None, "O usuário obtido não deveria ser None"
        assert usuario_db.id_usuario == id_usuario_inserido, "O ID do usuário obtido não confere"
        assert usuario_db.nome == usuario_teste.nome, "O nome do usuário obtido não confere"
        assert usuario_db.email == usuario_teste.email, "O email do usuário obtido não confere"
        assert usuario_db.senha == usuario_teste.senha, "A senha do usuário obtido não confere"
        assert usuario_db.telefone == usuario_teste.telefone, "O telefone do usuário obtido não confere"


        
```

# tests\test_veterinario_repo.py

```py
import os
import sys
from data.veterinario_repo import *
from data.veterinario_model import Veterinario
from data.usuario_model import Usuario
from data.usuario_repo import *

class TestVeterinarioRepo:
    def test_criar_tabela(self, test_db):
        # Arrange
        # Act
        resultado = criar_tabela_veterinario()
        # Assert
        assert resultado == True, "A criação da tabela de veterinários deveria retornar True"

    def test_inserir_veterinario(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_veterinario()
        novo_veterinario = Veterinario(
            id_usuario=0,
            nome="Veterinario Teste",
            email="vet@gmail.com",
            senha="senha123",
            telefone="11999999999",
            crmv="SP-123456",
            verificado=False,
            bio="Veterinário para teste"
        )
        # Insere um usuário para a FK id_usuario        
        id_novo_veterinario = inserir_veterinario(novo_veterinario)
        # Act
        # Assert
        assert id_novo_veterinario is not None, "A inserção do veterinário deveria retornar um ID válido"
        veterinario_db = obter_por_id(id_novo_veterinario)
        assert veterinario_db is not None, "O veterinário inserido não deveria ser None"
        assert veterinario_db.id_usuario == id_novo_veterinario, "O ID do veterinário inserido não confere"
        assert veterinario_db.nome == "Veterinario Teste", "O nome do veterinário inserido não confere"
        assert veterinario_db.email == "vet@gmail.com", "O email do veterinário inserido não confere"
        assert veterinario_db.senha == "senha123", "A senha do veterinário inserido não confere"
        assert veterinario_db.telefone == "11999999999", "O telefone do veterinário inserido não confere"
        assert veterinario_db.crmv == "SP-123456", "O CRMV do veterinário inserido não confere"
        assert veterinario_db.verificado == False, "O status de verificado do veterinário inserido não confere"
        assert veterinario_db.bio == "Veterinário para teste", "A bio do veterinário inserido não confere"    

    def test_atualizar_veterinario(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_veterinario()
        novo_veterinario = Veterinario(
            id_usuario=0,
            nome="Veterinario Teste",
            email="vet@gmail.com",
            senha="senha123",
            telefone="11999999999",
            crmv="SP-123456",
            verificado=False,
            bio="Veterinário para teste"
        )        
        id_novo_veterinario = inserir_veterinario(novo_veterinario)
        veterinario_inserido = obter_por_id(id_novo_veterinario)
        
        # Act
        # Atualizando atributos herdados do usuário
        veterinario_inserido.nome = "Dr. Atualizado"
        veterinario_inserido.email = "atualizado@example.com"        
        veterinario_inserido.telefone = "11988888888"
        # Atualizando atributos exclusivos do veterinário
        veterinario_inserido.crmv = "SP-654321"
        veterinario_inserido.verificado = True
        veterinario_inserido.bio = "Bio atualizada"
        # Chama a função de atualização        
        resultado = atualizar_veterinario(veterinario_inserido)
        
        # Assert
        assert resultado == True, "A atualização do veterinário deveria retornar True"
        veterinario_db = obter_por_id(id_novo_veterinario)
        assert veterinario_db.nome == "Dr. Atualizado", "O nome do veterinário não foi atualizado corretamente"
        assert veterinario_db.email == "atualizado@example.com", "O email do veterinário não foi atualizado corretamente"
        assert veterinario_db.telefone == "11988888888", "O telefone do veterinário não foi atualizado corretamente"
        assert veterinario_db.crmv == "SP-654321", "O CRMV do veterinário não foi atualizado corretamente"
        assert veterinario_db.verificado == True, "O status de verificado não foi atualizado corretamente"
        assert veterinario_db.bio == "Bio atualizada", "A bio do veterinário não foi atualizada corretamente"

    def test_excluir_veterinario(self, test_db):
        # Arrange
        criar_tabela_veterinario()
        veterinario_teste = Veterinario(
            id_usuario=1,
            id_veterinario=1,
            nome="Dr. Remover",
            email="remover@example.com",
            senha="senha123",
            telefone="11999999999",
            crmv="SP-54321",
            verificado=False,
            bio="Será removido"
        )
        inserir_veterinario(veterinario_teste)
        
        # Act
        resultado = excluir_veterinario(veterinario_teste.id_veterinario)
        
        # Assert
        assert resultado == True, "A exclusão do veterinário deveria retornar True"
        veterinario_excluido = obter_por_id(veterinario_teste.id_veterinario)
        assert veterinario_excluido is None, "O veterinário excluído deveria ser None"

    def test_obter_todos_veterinarios(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_veterinario()

        vet1 = Veterinario(
            id_usuario=1,
            id_veterinario=1,
            nome="Dr. A",
            email="a@example.com",
            senha="senhaA",
            telefone="11111111111",
            crmv="CRMV-A",
            verificado=False,
            bio="Veterinário A"
        )
        vet2 = Veterinario(
            id_usuario=2,
            id_veterinario=2,
            nome="Dr. B",
            email="b@example.com",
            senha="senhaB",
            telefone="22222222222",
            crmv="CRMV-B",
            verificado=True,
            bio="Veterinário B"
        )
        inserir_veterinario(vet1)
        inserir_veterinario(vet2)
        
        # Act
        veterinarios = obter_todos()
        
        # Assert
        assert len(veterinarios) >= 2, "Deveria retornar pelo menos dois veterinários"
        nomes = [v.nome for v in veterinarios]
        assert "Dr. A" in nomes, "O nome 'Dr. A' deveria estar na lista de veterinários"
        assert "Dr. B" in nomes, "O nome 'Dr. B' deveria estar na lista de veterinários"
        
    def test_obter_veterinario_por_id(self, test_db):
        # Arrange
        criar_tabela_veterinario()
        veterinario_teste = Veterinario(
            id_usuario=1,
            id_veterinario=1,
            nome="Dr. Teste",
            email="vet@gmail.com",
            senha="senha123",
            telefone="11999999999",
            crmv="SP-123456",
            verificado=False,
            bio="Veterinário para teste"
        )
        inserir_veterinario(veterinario_teste)
        # Act
        veterinario_db = obter_por_id(veterinario_teste.id_veterinario)
        # Assert
        assert veterinario_db is not None, "O veterinário obtido não deveria ser None"
        assert veterinario_db.id_veterinario == veterinario_teste.id_veterinario, "O ID do veterinário obtido não confere"
        assert veterinario_db.nome == "Dr. Teste", "O nome do veterinário obtido não confere"
        assert veterinario_db.crmv == "SP-123456", "O CRMV do veterinário obtido não confere"
        assert veterinario_db.bio == "Veterinário para teste", "A bio do veterinário obtido não confere"
        
```

# util.py

```py
import sqlite3
import os

def get_connection():
    conn = None
    try:
        database_path = os.environ.get('TEST_DATABASE_PATH', 'dados.db')
        conn = sqlite3.connect(database_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")  # Ativa as chaves estrangeiras
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    return conn
```

