# Análise: Alteração de Foto do Perfil do Usuário

**Data da Análise:** 2025-10-15
**Versão:** 1.0
**Analista:** Sistema de Análise de Código

---

## 1. Visão Geral da Implementação

A funcionalidade de alteração de foto de perfil está implementada em:

- **Rota Backend:** `/perfil/alterar-foto` (POST) em `routes/publico/perfil_routes.py:212-258`
- **Repositório:** `repo/usuario_repo.py:169-174` (função `atualizar_foto`)
- **SQL:** `sql/usuario_sql.py:84-96` (query `ATUALIZAR_FOTO`)
- **Frontend:** `templates/perfil/dados.html` + `static/js/preview_perfil.js`
- **Modelo:** `model/usuario_model.py` (campo `foto: Optional[str]`)

### Fluxo Atual

1. Usuário seleciona arquivo no formulário HTML
2. JavaScript valida tipo e mostra preview
3. Upload via POST multipart/form-data
4. Backend valida content_type
5. Arquivo salvo em `static/uploads/usuarios/`
6. Caminho relativo armazenado no banco
7. Sessão atualizada com nova foto

---

## 2. Problemas Identificados

### 2.1 Problemas de Configuração

#### 🔴 **CRÍTICO: Sem Limite de Tamanho de Arquivo**

**Localização:** `routes/publico/perfil_routes.py:212-258`

**Problema:**
Nenhum limite de tamanho configurado. Usuários podem fazer upload de arquivos gigantescos, causando:
- Esgotamento de espaço em disco
- Consumo excessivo de memória
- Timeout de requisições
- Negação de serviço (DoS)

**Código Atual:**
```python
async def alterar_foto(
    request: Request,
    foto: UploadFile = File(...),  # ← Sem max_size
    usuario_logado: Optional[dict] = None
):
```

---

#### 🟡 **MÉDIO: Falta Configuração Centralizada**

**Problema:**
Valores hardcoded espalhados pelo código:

```python
# perfil_routes.py:223
tipos_permitidos = ["image/jpeg", "image/png", "image/jpg"]

# perfil_routes.py:228
upload_dir = "static/uploads/usuarios"
```

**Impacto:**
- Difícil manutenção
- Inconsistências entre diferentes partes do código
- Necessidade de alterar código para mudar configurações

---

#### 🟡 **MÉDIO: Diretório de Uploads Não Está no .gitignore**

**Problema:**
O diretório `static/uploads/usuarios/` contém arquivos de usuários e não está ignorado pelo Git.

**Impacto:**
- Arquivos pessoais podem ser commitados no repositório
- Violação de privacidade (LGPD)
- Histórico Git poluído com binários
- Repositório cresce desnecessariamente

---

#### 🟢 **BAIXO: Sem Configuração de Dimensões Máximas**

**Problema:**
Não há validação de largura/altura da imagem.

**Impacto:**
- Imagens muito grandes consumem recursos
- Problemas de performance no carregamento
- Desperdício de armazenamento

---

### 2.2 Problemas de Validação de Arquivos

#### 🔴 **CRÍTICO: Validação de Tipo Apenas por Content-Type**

**Localização:** `routes/publico/perfil_routes.py:222-225`

**Problema:**
```python
tipos_permitidos = ["image/jpeg", "image/png", "image/jpg"]
if foto.content_type not in tipos_permitidos:
    return RedirectResponse("/perfil?erro=tipo_invalido", status.HTTP_303_SEE_OTHER)
```

O `content_type` é enviado pelo cliente e **facilmente falsificável**:

```bash
# Atacante pode fazer:
curl -F "foto=@malware.exe" \
     -H "Content-Type: image/jpeg" \
     https://site.com/perfil/alterar-foto
```

**Impacto:**
- Upload de arquivos maliciosos (executáveis, scripts)
- Vulnerabilidade de segurança grave
- Possível execução de código arbitrário

---

#### 🔴 **CRÍTICO: Sem Validação de Tamanho de Arquivo**

**Localização:** `routes/publico/perfil_routes.py:212-258`

**Problema:**
Nenhuma verificação do tamanho do arquivo:

```python
conteudo = await foto.read()  # ← Lê arquivo inteiro sem limite
with open(caminho_arquivo, "wb") as f:
    f.write(conteudo)
```

**Ataques Possíveis:**
```python
# Cenário 1: Upload de 10GB
# → Servidor trava
# → Disco cheio
# → Aplicação indisponível

# Cenário 2: Múltiplos uploads grandes
# → DoS distribuído
```

---

#### 🔴 **CRÍTICO: Sem Validação de Conteúdo Real (Magic Bytes)**

**Problema:**
Não verifica os bytes iniciais (file signature) do arquivo.

**Exemplo de Ataque:**
```bash
# Renomear executável como imagem
cp virus.exe fake_image.jpg

# Upload bem-sucedido apesar de não ser imagem
```

**Magic Bytes de Imagens Válidas:**
- **JPEG:** `FF D8 FF`
- **PNG:** `89 50 4E 47 0D 0A 1A 0A`
- **GIF:** `47 49 46 38`

---

#### 🟡 **MÉDIO: Validação Duplicada no Frontend**

**Localização:** `static/js/preview_perfil.js:14`

**Problema:**
```javascript
if (file.type.startsWith('image/')) {
    // Validação apenas no frontend
}
```

**Impacto:**
- Facilmente bypassável (desabilitar JavaScript)
- Falsa sensação de segurança
- Validação deve ser **sempre** no backend

---

#### 🟡 **MÉDIO: Sem Normalização de Extensão**

**Localização:** `routes/publico/perfil_routes.py:236`

**Problema:**
```python
extensao = foto.filename.split(".")[-1]  # ← Sem validação
nome_arquivo = f"{usuario_logado['id']}_{secrets.token_hex(8)}.{extensao}"
```

**Ataques Possíveis:**
```python
# Arquivo: "malware.php.jpg.exe"
# → extensao = "exe" ❌

# Arquivo: "foto...........jpg"
# → Aceito sem sanitização

# Arquivo: "foto.JPG" vs "foto.jpg"
# → Case sensitivity pode causar problemas
```

---

### 2.3 Problemas de Permissões

#### 🟡 **MÉDIO: Sem Verificação de Permissões do Diretório**

**Localização:** `routes/publico/perfil_routes.py:228-229`

**Problema:**
```python
upload_dir = "static/uploads/usuarios"
os.makedirs(upload_dir, exist_ok=True)  # ← Falha silenciosa possível
```

**Cenários Problemáticos:**
```python
# 1. Diretório sem permissão de escrita
# → os.makedirs() pode falhar silenciosamente

# 2. Diretório criado mas sem permissão
# → Falha ao escrever arquivo

# 3. Diretório em sistema de arquivos cheio
# → Sem tratamento adequado
```

---

#### 🟡 **MÉDIO: Arquivos Salvos com Permissões Padrão**

**Problema:**
Arquivos criados sem definir permissões explícitas:

```python
with open(caminho_arquivo, "wb") as f:
    f.write(conteudo)  # ← Permissões padrão (umask)
```

**Riscos:**
```bash
# Permissões típicas: 644 ou 666
# → Outros usuários podem ler
# → Possível vazamento em servidor compartilhado

# Ideal: 600 ou 640
os.chmod(caminho_arquivo, 0o644)  # Melhor controle
```

---

#### 🔴 **CRÍTICO: Fotos Antigas Não São Deletadas**

**Localização:** `routes/publico/perfil_routes.py:246-248`

**Problema:**
```python
# Atualizar caminho no banco
caminho_relativo = f"/static/uploads/usuarios/{nome_arquivo}"
usuario_repo.atualizar_foto(usuario_logado['id'], caminho_relativo)
# ← Foto antiga permanece no disco!
```

**Impactos:**
```python
# Cenário:
# 1. Usuário faz upload de foto1.jpg
# 2. Usuário faz upload de foto2.jpg
# 3. Usuário faz upload de foto3.jpg
# → Resultado: 3 arquivos no disco, apenas 1 usado
# → Desperdício de espaço
# → Violação LGPD (dados antigos não deletados)
# → URLs antigas podem vazar informação
```

---

### 2.4 Problemas de Segurança

#### 🔴 **CRÍTICO: Vulnerabilidade Path Traversal**

**Localização:** `routes/publico/perfil_routes.py:233-238`

**Problema:**
```python
if not foto.filename:
    return RedirectResponse("/perfil?erro=arquivo_invalido", status.HTTP_303_SEE_OTHER)

extensao = foto.filename.split(".")[-1]
nome_arquivo = f"{usuario_logado['id']}_{secrets.token_hex(8)}.{extensao}"
```

**Ataque Possível:**
```python
# Arquivo malicioso: "../../etc/passwd"
# ou: "foto.jpg\x00.php"
# ou: "foto.jpg%00.php"

# Sem sanitização adequada:
nome_arquivo = "2_abc123def456.../../etc/passwd"
# → Pode escapar do diretório de upload
```

---

#### 🟡 **MÉDIO: Nome de Arquivo Parcialmente Previsível**

**Problema:**
```python
nome_arquivo = f"{usuario_logado['id']}_{secrets.token_hex(8)}.{extensao}"
#                  ^^^ previsível    ^^^ 16 caracteres hex (2^64)
```

**Impacto:**
- ID do usuário é previsível
- Token de 64 bits pode ser suficiente, mas...
- Informação vazada: ID do usuário no nome do arquivo

**Melhor Abordagem:**
```python
# UUID4 completamente aleatório
nome_arquivo = f"{uuid.uuid4()}.{extensao_validada}"
```

---

#### 🔴 **CRÍTICO: Tratamento de Exceção Genérico**

**Localização:** `routes/publico/perfil_routes.py:255-256`

**Problema:**
```python
except Exception as e:
    return RedirectResponse("/perfil?erro=upload_falhou", status.HTTP_303_SEE_OTHER)
    # ← Erro ignorado! Sem logging!
```

**Problemas:**
```python
# 1. Nenhum registro do erro
# 2. Debug impossível
# 3. Atacante pode tentar múltiplas vezes sem detecção
# 4. Falhas silenciosas
# 5. Usuário sem informação útil
```

---

#### 🟡 **MÉDIO: Sem Sanitização do Nome Original**

**Problema:**
Nome original do arquivo não é validado adequadamente antes de processar.

**Ataques Possíveis:**
```python
# Nomes maliciosos:
"<script>alert('xss')</script>.jpg"
"; rm -rf /; .jpg"
"../../../../../../etc/passwd%00.jpg"
"con.jpg"  # Nome reservado no Windows
"\\\\?\\C:\\Windows\\System32\\config\\SAM.jpg"
```

---

### 2.5 Problemas de Usabilidade

#### 🟢 **BAIXO: Sem Indicação de Progresso**

**Problema:**
Upload de arquivos grandes não mostra progresso.

**Impacto:**
- Usuário não sabe se upload está funcionando
- Pode clicar múltiplas vezes
- Má experiência do usuário

---

#### 🟢 **BAIXO: Mensagens de Erro Genéricas**

**Localização:** `routes/publico/perfil_routes.py`

**Problema:**
```python
return RedirectResponse("/perfil?erro=tipo_invalido", status.HTTP_303_SEE_OTHER)
return RedirectResponse("/perfil?erro=arquivo_invalido", status.HTTP_303_SEE_OTHER)
return RedirectResponse("/perfil?erro=upload_falhou", status.HTTP_303_SEE_OTHER)
```

Usuário vê apenas:
- "Tipo inválido" ← Quais tipos são válidos?
- "Arquivo inválido" ← Por quê?
- "Upload falhou" ← O que fazer?

---

#### 🟢 **BAIXO: Sem Funcionalidade de Recorte/Redimensionamento**

**Problema:**
- Usuário não pode recortar imagem
- Imagem pode ficar distorcida
- Sem ajuste de enquadramento

---

### 2.6 Problemas de Manutenção

#### 🟡 **MÉDIO: Duplicação de Código SQL**

**Localização:** `sql/usuario_sql.py`

**Problema:**
```python
# Linha 84-86
ATUALIZAR_FOTO = """
UPDATE usuario
SET foto=?
WHERE id_usuario=?
"""

# Linha 94-96 - DUPLICADO!
ATUALIZAR_FOTO = """
UPDATE usuario SET foto = ? WHERE id_usuario = ?
"""
```

**Impacto:**
- Confusão: qual é usada?
- Risco de inconsistência
- Manutenção duplicada

---

#### 🟡 **MÉDIO: Falta de Logging**

**Problema:**
Nenhum log de operações críticas:

```python
# Deveria ter:
logger.info(f"Upload iniciado: usuário {usuario_id}")
logger.info(f"Arquivo salvo: {caminho_arquivo}")
logger.warning(f"Tentativa de upload com tipo inválido: {content_type}")
logger.error(f"Falha no upload: {e}", exc_info=True)
```

---

#### 🟢 **BAIXO: Falta Tratamento Específico de Exceções**

**Problema:**
```python
except Exception as e:  # ← Muito genérico
```

**Deveria Tratar:**
```python
except IOError as e:
    # Problema de I/O (disco cheio, sem permissão)
except OSError as e:
    # Problema do sistema operacional
except ValueError as e:
    # Dados inválidos
```

---

## 3. Soluções Propostas

### 3.1 Solução para Problemas de Configuração

#### Criar arquivo `config/upload_config.py`:

```python
"""
Configurações de Upload de Arquivos
"""
from pathlib import Path
from typing import Set

class UploadConfig:
    """Configurações centralizadas para upload de arquivos"""

    # Diretórios
    BASE_DIR = Path("static/uploads")
    USUARIOS_DIR = BASE_DIR / "usuarios"
    TEMP_DIR = BASE_DIR / "temp"

    # Limites de tamanho
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    MAX_FILE_SIZE_MB = 5

    # Dimensões de imagem
    MAX_WIDTH = 2048
    MAX_HEIGHT = 2048
    MIN_WIDTH = 100
    MIN_HEIGHT = 100

    # Tipos permitidos
    ALLOWED_EXTENSIONS: Set[str] = {'.jpg', '.jpeg', '.png', '.webp'}
    ALLOWED_MIME_TYPES: Set[str] = {
        'image/jpeg',
        'image/png',
        'image/webp'
    }

    # Magic bytes para validação
    MAGIC_BYTES = {
        b'\xFF\xD8\xFF': 'jpeg',
        b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A': 'png',
        b'RIFF': 'webp'  # Seguido por 'WEBP' nos bytes 8-11
    }

    # Permissões
    DIR_PERMISSIONS = 0o755
    FILE_PERMISSIONS = 0o644

    # Timeouts
    UPLOAD_TIMEOUT = 30  # segundos

    @classmethod
    def init_directories(cls):
        """Cria diretórios necessários com permissões corretas"""
        for directory in [cls.USUARIOS_DIR, cls.TEMP_DIR]:
            directory.mkdir(parents=True, exist_ok=True)
            directory.chmod(cls.DIR_PERMISSIONS)

# Inicializar na inicialização da aplicação
UploadConfig.init_directories()
```

#### Adicionar ao `.gitignore`:

```gitignore
# Uploads de usuários (não versionar)
static/uploads/usuarios/*
!static/uploads/usuarios/.gitkeep

# Uploads temporários
static/uploads/temp/*
!static/uploads/temp/.gitkeep
```

#### Criar arquivos `.gitkeep`:

```bash
touch static/uploads/usuarios/.gitkeep
touch static/uploads/temp/.gitkeep
```

---

### 3.2 Solução para Problemas de Validação

#### Criar arquivo `util/file_validator.py`:

```python
"""
Validador Robusto de Arquivos de Upload
"""
import os
import uuid
import imghdr
from pathlib import Path
from typing import Tuple, Optional
from PIL import Image
import magic  # python-magic
from fastapi import UploadFile

from config.upload_config import UploadConfig


class FileValidationError(Exception):
    """Erro de validação de arquivo"""
    pass


class FileValidator:
    """Validador completo de arquivos de upload"""

    @staticmethod
    async def validar_imagem_completo(
        arquivo: UploadFile,
        max_size: int = UploadConfig.MAX_FILE_SIZE
    ) -> Tuple[bytes, str]:
        """
        Validação completa de arquivo de imagem

        Returns:
            Tuple[bytes, str]: (conteúdo do arquivo, extensão validada)

        Raises:
            FileValidationError: Se arquivo inválido
        """

        # 1. Validar nome do arquivo
        if not arquivo.filename:
            raise FileValidationError("Nome do arquivo não fornecido")

        FileValidator._validar_nome_arquivo(arquivo.filename)

        # 2. Validar extensão
        extensao = FileValidator._obter_extensao_segura(arquivo.filename)
        if extensao not in UploadConfig.ALLOWED_EXTENSIONS:
            extensoes_str = ', '.join(UploadConfig.ALLOWED_EXTENSIONS)
            raise FileValidationError(
                f"Extensão não permitida. Use: {extensoes_str}"
            )

        # 3. Ler conteúdo com limite de tamanho
        try:
            conteudo = await FileValidator._ler_com_limite(arquivo, max_size)
        except FileValidationError:
            raise

        # 4. Validar magic bytes
        tipo_real = FileValidator._validar_magic_bytes(conteudo)
        if not tipo_real:
            raise FileValidationError(
                "Arquivo não é uma imagem válida (validação de assinatura falhou)"
            )

        # 5. Validar com biblioteca de imagem
        try:
            FileValidator._validar_com_pillow(conteudo)
        except Exception as e:
            raise FileValidationError(f"Arquivo de imagem corrompido: {str(e)}")

        # 6. Validar MIME type
        if arquivo.content_type not in UploadConfig.ALLOWED_MIME_TYPES:
            raise FileValidationError(
                f"Tipo MIME não permitido: {arquivo.content_type}"
            )

        return conteudo, extensao

    @staticmethod
    async def _ler_com_limite(
        arquivo: UploadFile,
        max_size: int
    ) -> bytes:
        """Lê arquivo com limite de tamanho"""
        conteudo = b""
        chunk_size = 1024 * 1024  # 1MB por vez

        while True:
            chunk = await arquivo.read(chunk_size)
            if not chunk:
                break

            conteudo += chunk

            if len(conteudo) > max_size:
                raise FileValidationError(
                    f"Arquivo muito grande. Máximo: {max_size // (1024*1024)}MB"
                )

        if len(conteudo) == 0:
            raise FileValidationError("Arquivo vazio")

        return conteudo

    @staticmethod
    def _validar_nome_arquivo(filename: str):
        """Valida nome do arquivo contra path traversal e caracteres perigosos"""
        # Caracteres proibidos
        caracteres_proibidos = ['..', '/', '\\', '\x00', '<', '>', ':', '"', '|', '?', '*']

        for char in caracteres_proibidos:
            if char in filename:
                raise FileValidationError(
                    f"Nome de arquivo contém caracteres proibidos: {char}"
                )

        # Verificar nomes reservados (Windows)
        nomes_reservados = {
            'CON', 'PRN', 'AUX', 'NUL',
            'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
            'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
        }

        nome_base = filename.split('.')[0].upper()
        if nome_base in nomes_reservados:
            raise FileValidationError("Nome de arquivo reservado pelo sistema")

    @staticmethod
    def _obter_extensao_segura(filename: str) -> str:
        """Obtém extensão de forma segura"""
        # Remover null bytes
        filename = filename.replace('\x00', '')

        # Obter última extensão
        partes = filename.lower().split('.')
        if len(partes) < 2:
            raise FileValidationError("Arquivo sem extensão")

        extensao = '.' + partes[-1]
        return extensao

    @staticmethod
    def _validar_magic_bytes(conteudo: bytes) -> Optional[str]:
        """Valida arquivo através dos magic bytes (assinatura)"""
        for magic_byte, tipo in UploadConfig.MAGIC_BYTES.items():
            if conteudo.startswith(magic_byte):
                # Validação especial para WebP
                if tipo == 'webp':
                    if len(conteudo) > 12 and conteudo[8:12] == b'WEBP':
                        return tipo
                    return None
                return tipo
        return None

    @staticmethod
    def _validar_com_pillow(conteudo: bytes):
        """Valida imagem usando Pillow e retorna dimensões"""
        from io import BytesIO

        try:
            img = Image.open(BytesIO(conteudo))
            img.verify()  # Verifica integridade

            # Reabrir para obter dimensões (verify() invalida objeto)
            img = Image.open(BytesIO(conteudo))
            width, height = img.size

            # Validar dimensões
            if width < UploadConfig.MIN_WIDTH or height < UploadConfig.MIN_HEIGHT:
                raise FileValidationError(
                    f"Imagem muito pequena. Mínimo: {UploadConfig.MIN_WIDTH}x{UploadConfig.MIN_HEIGHT}px"
                )

            if width > UploadConfig.MAX_WIDTH or height > UploadConfig.MAX_HEIGHT:
                raise FileValidationError(
                    f"Imagem muito grande. Máximo: {UploadConfig.MAX_WIDTH}x{UploadConfig.MAX_HEIGHT}px"
                )

        except FileValidationError:
            raise
        except Exception as e:
            raise FileValidationError(f"Erro ao validar imagem: {str(e)}")

    @staticmethod
    def gerar_nome_arquivo_seguro(extensao: str) -> str:
        """Gera nome de arquivo único e seguro"""
        # Normalizar extensão
        extensao = extensao.lower().lstrip('.')

        # Gerar UUID completamente aleatório
        nome_unico = str(uuid.uuid4())

        return f"{nome_unico}.{extensao}"

    @staticmethod
    def sanitizar_path(caminho: str) -> Path:
        """Sanitiza path para evitar path traversal"""
        path = Path(caminho).resolve()

        # Verificar se está dentro do diretório permitido
        base_permitido = UploadConfig.USUARIOS_DIR.resolve()

        if not str(path).startswith(str(base_permitido)):
            raise FileValidationError("Path inválido detectado")

        return path
```

#### Instalar dependências necessárias:

```bash
pip install Pillow python-magic-bin
```

---

### 3.3 Solução para Problemas de Permissões e Limpeza

#### Criar arquivo `util/file_manager.py`:

```python
"""
Gerenciador de Arquivos de Upload
"""
import os
import logging
from pathlib import Path
from typing import Optional

from config.upload_config import UploadConfig


logger = logging.getLogger(__name__)


class FileManager:
    """Gerenciador de arquivos de upload com limpeza"""

    @staticmethod
    def salvar_arquivo(
        conteudo: bytes,
        nome_arquivo: str,
        usuario_id: int
    ) -> str:
        """
        Salva arquivo com permissões corretas

        Returns:
            str: Caminho relativo do arquivo salvo
        """
        # Caminho completo
        caminho_completo = UploadConfig.USUARIOS_DIR / nome_arquivo

        try:
            # Verificar permissões do diretório
            if not os.access(UploadConfig.USUARIOS_DIR, os.W_OK):
                raise PermissionError(
                    f"Sem permissão de escrita em {UploadConfig.USUARIOS_DIR}"
                )

            # Salvar arquivo
            with open(caminho_completo, 'wb') as f:
                f.write(conteudo)

            # Definir permissões
            os.chmod(caminho_completo, UploadConfig.FILE_PERMISSIONS)

            # Caminho relativo para URL
            caminho_relativo = f"/static/uploads/usuarios/{nome_arquivo}"

            logger.info(
                f"Arquivo salvo com sucesso: {nome_arquivo} "
                f"(usuário: {usuario_id}, tamanho: {len(conteudo)} bytes)"
            )

            return caminho_relativo

        except PermissionError as e:
            logger.error(f"Erro de permissão ao salvar arquivo: {e}")
            raise
        except OSError as e:
            logger.error(f"Erro de sistema ao salvar arquivo: {e}")
            raise
        except Exception as e:
            logger.error(f"Erro inesperado ao salvar arquivo: {e}", exc_info=True)
            raise

    @staticmethod
    def deletar_foto_antiga(caminho_foto: Optional[str]):
        """
        Deleta foto antiga do usuário (LGPD compliance)
        """
        if not caminho_foto:
            return

        try:
            # Converter caminho relativo para absoluto
            # caminho_foto = "/static/uploads/usuarios/abc.jpg"
            nome_arquivo = Path(caminho_foto).name
            caminho_completo = UploadConfig.USUARIOS_DIR / nome_arquivo

            if caminho_completo.exists():
                caminho_completo.unlink()
                logger.info(f"Foto antiga deletada: {nome_arquivo}")
            else:
                logger.warning(f"Foto antiga não encontrada: {caminho_completo}")

        except PermissionError as e:
            logger.error(f"Sem permissão para deletar foto: {e}")
        except Exception as e:
            logger.error(f"Erro ao deletar foto antiga: {e}", exc_info=True)

    @staticmethod
    def verificar_espaco_disco(tamanho_necessario: int) -> bool:
        """Verifica se há espaço suficiente no disco"""
        import shutil

        try:
            stats = shutil.disk_usage(UploadConfig.USUARIOS_DIR)
            espaco_livre = stats.free

            # Deixar pelo menos 100MB de margem
            margem_seguranca = 100 * 1024 * 1024

            return espaco_livre > (tamanho_necessario + margem_seguranca)
        except Exception as e:
            logger.error(f"Erro ao verificar espaço em disco: {e}")
            return False
```

---

### 3.4 Solução Completa: Rota Refatorada

#### Arquivo `routes/publico/perfil_routes.py` (refatorado):

```python
import logging
from fastapi import APIRouter, Form, Request, status, UploadFile, File
from fastapi.responses import RedirectResponse
from typing import Optional

from model.usuario_model import Usuario
from repo import usuario_repo
from util.auth_decorator import requer_autenticacao, criar_sessao
from util.template_util import criar_templates
from util.file_validator import FileValidator, FileValidationError
from util.file_manager import FileManager
from config.upload_config import UploadConfig


logger = logging.getLogger(__name__)
router = APIRouter()
templates = criar_templates("templates/publico")


@router.post("/alterar-foto")
@requer_autenticacao()
async def alterar_foto(
    request: Request,
    foto: UploadFile = File(...),
    usuario_logado: Optional[dict] = None
):
    """
    Endpoint para alteração de foto de perfil

    Validações realizadas:
    - Tipo de arquivo (magic bytes)
    - Tamanho do arquivo
    - Dimensões da imagem
    - Nome do arquivo (path traversal)
    - Permissões do sistema
    """
    if not usuario_logado:
        logger.warning("Tentativa de upload sem autenticação")
        return RedirectResponse("/", status.HTTP_303_SEE_OTHER)

    usuario_id = usuario_logado['id']
    logger.info(f"Iniciando upload de foto para usuário {usuario_id}")

    try:
        # 1. Validação completa do arquivo
        try:
            conteudo, extensao = await FileValidator.validar_imagem_completo(
                foto,
                max_size=UploadConfig.MAX_FILE_SIZE
            )
        except FileValidationError as e:
            logger.warning(f"Validação falhou para usuário {usuario_id}: {e}")
            return RedirectResponse(
                f"/perfil?erro={str(e)}",
                status.HTTP_303_SEE_OTHER
            )

        # 2. Verificar espaço em disco
        if not FileManager.verificar_espaco_disco(len(conteudo)):
            logger.error("Espaço em disco insuficiente")
            return RedirectResponse(
                "/perfil?erro=Espaço em disco insuficiente",
                status.HTTP_303_SEE_OTHER
            )

        # 3. Obter foto atual do usuário
        usuario = usuario_repo.obter_usuario_por_id(usuario_id)
        if not usuario:
            logger.error(f"Usuário {usuario_id} não encontrado")
            return RedirectResponse("/", status.HTTP_303_SEE_OTHER)

        foto_antiga = usuario.foto

        # 4. Gerar nome seguro para novo arquivo
        nome_arquivo = FileValidator.gerar_nome_arquivo_seguro(extensao)

        # 5. Salvar novo arquivo
        try:
            caminho_relativo = FileManager.salvar_arquivo(
                conteudo,
                nome_arquivo,
                usuario_id
            )
        except (PermissionError, OSError) as e:
            logger.error(f"Erro ao salvar arquivo: {e}", exc_info=True)
            return RedirectResponse(
                "/perfil?erro=Erro ao salvar arquivo. Contate o administrador.",
                status.HTTP_303_SEE_OTHER
            )

        # 6. Atualizar banco de dados
        try:
            usuario_repo.atualizar_foto(usuario_id, caminho_relativo)
        except Exception as e:
            logger.error(f"Erro ao atualizar banco: {e}", exc_info=True)
            # Rollback: deletar arquivo recém-criado
            FileManager.deletar_foto_antiga(caminho_relativo)
            return RedirectResponse(
                "/perfil?erro=Erro ao atualizar perfil",
                status.HTTP_303_SEE_OTHER
            )

        # 7. Deletar foto antiga (LGPD compliance)
        if foto_antiga:
            FileManager.deletar_foto_antiga(foto_antiga)

        # 8. Atualizar sessão
        usuario_logado['foto'] = caminho_relativo
        criar_sessao(request, usuario_logado)

        logger.info(f"Upload concluído com sucesso para usuário {usuario_id}")
        return RedirectResponse("/perfil?foto_sucesso=1", status.HTTP_303_SEE_OTHER)

    except Exception as e:
        # Catch-all para erros inesperados
        logger.error(
            f"Erro inesperado no upload do usuário {usuario_id}: {e}",
            exc_info=True
        )
        return RedirectResponse(
            "/perfil?erro=Erro inesperado. Tente novamente.",
            status.HTTP_303_SEE_OTHER
        )
```

---

### 3.5 Melhorias de Frontend

#### Template `templates/perfil/dados.html` (melhorado):

```html
{% extends "base_publica.html" %}
{% block conteudo %}
<!-- Container centralizado para foto atual -->
<div class="d-flex justify-content-center">
    <img id="foto-atual"
         src="{{ usuario.foto or '/static/img/user-default.png' }}"
         class="rounded-circle mb-3"
         style="width: 150px; height: 150px; object-fit: cover; border: 3px solid #dee2e6;"
         alt="Foto do perfil">
</div>

<!-- Preview da nova foto -->
<div id="preview-foto-container" style="display: none;">
    <div class="d-flex justify-content-center">
        <img id="preview-foto"
             src=""
             class="rounded-circle mb-2"
             style="width: 150px; height: 150px; object-fit: cover; border: 3px solid #28a745;"
             alt="Preview da nova foto">
    </div>
    <div class="small text-success mb-2">
        <i class="bi-check-circle"></i> Nova foto selecionada
    </div>
</div>

<!-- Barra de progresso -->
<div id="upload-progress" class="mb-3" style="display: none;">
    <div class="progress">
        <div id="progress-bar" class="progress-bar progress-bar-striped progress-bar-animated"
             role="progressbar" style="width: 0%"></div>
    </div>
    <small id="upload-status" class="text-muted">Enviando...</small>
</div>

<!-- Mensagens de erro/sucesso -->
{% if request.query_params.get('erro') %}
<div class="alert alert-danger alert-dismissible fade show" role="alert">
    <i class="bi-exclamation-triangle"></i>
    {{ request.query_params.get('erro') }}
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
</div>
{% endif %}

{% if request.query_params.get('foto_sucesso') %}
<div class="alert alert-success alert-dismissible fade show" role="alert">
    <i class="bi-check-circle"></i>
    Foto atualizada com sucesso!
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
</div>
{% endif %}

<!-- Formulário de upload -->
<form id="upload-form" action="/perfil/alterar-foto" method="post" enctype="multipart/form-data">
    <div class="mb-2">
        <label for="foto" class="form-label small">Selecionar Nova Foto</label>
        <input type="file"
               class="form-control form-control-sm"
               id="foto"
               name="foto"
               accept="image/jpeg,image/jpg,image/png,image/webp">
        <div class="form-text small">
            JPG, PNG ou WebP | Máximo: 5MB | Mínimo: 100x100px
        </div>
    </div>
    <button type="submit" class="btn btn-sm btn-outline-primary" id="btn-alterar" disabled>
        <i class="bi-camera"></i> Alterar Foto
    </button>
    <button type="button" class="btn btn-sm btn-outline-secondary" id="btn-cancelar"
            onclick="cancelarSelecao()" style="display: none;">
        <i class="bi-x"></i> Cancelar
    </button>
</form>
{% endblock %}
```

#### JavaScript `static/js/preview_perfil.js` (melhorado):

```javascript
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('upload-form');
    const fotoInput = document.getElementById('foto');
    const fotoAtual = document.getElementById('foto-atual');
    const previewContainer = document.getElementById('preview-foto-container');
    const previewFoto = document.getElementById('preview-foto');
    const btnAlterar = document.getElementById('btn-alterar');
    const btnCancelar = document.getElementById('btn-cancelar');
    const progressContainer = document.getElementById('upload-progress');
    const progressBar = document.getElementById('progress-bar');
    const uploadStatus = document.getElementById('upload-status');

    // Configurações
    const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
    const ALLOWED_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];

    fotoInput.addEventListener('change', async function(e) {
        const file = e.target.files[0];

        if (!file) {
            cancelarSelecao();
            return;
        }

        // Validação 1: Tipo de arquivo
        if (!ALLOWED_TYPES.includes(file.type)) {
            alert('Tipo de arquivo não permitido. Use JPG, PNG ou WebP.');
            cancelarSelecao();
            return;
        }

        // Validação 2: Tamanho do arquivo
        if (file.size > MAX_FILE_SIZE) {
            alert(`Arquivo muito grande. Máximo: ${MAX_FILE_SIZE / (1024*1024)}MB`);
            cancelarSelecao();
            return;
        }

        // Validação 3: Dimensões da imagem
        try {
            const img = await carregarImagem(file);

            if (img.width < 100 || img.height < 100) {
                alert('Imagem muito pequena. Mínimo: 100x100 pixels');
                cancelarSelecao();
                return;
            }

            // Mostrar preview
            fotoAtual.style.display = 'none';
            previewFoto.src = img.src;
            previewContainer.style.display = 'block';

            // Habilitar botão e mostrar opções
            btnAlterar.disabled = false;
            btnAlterar.innerHTML = '<i class="bi-check"></i> Confirmar Alteração';
            btnCancelar.style.display = 'inline-block';

        } catch (error) {
            alert('Erro ao carregar imagem: ' + error.message);
            cancelarSelecao();
        }
    });

    // Upload com progress
    form.addEventListener('submit', function(e) {
        e.preventDefault();

        const formData = new FormData(form);
        const xhr = new XMLHttpRequest();

        // Mostrar barra de progresso
        progressContainer.style.display = 'block';
        btnAlterar.disabled = true;
        btnCancelar.disabled = true;

        // Progress handler
        xhr.upload.addEventListener('progress', function(e) {
            if (e.lengthComputable) {
                const percentComplete = (e.loaded / e.total) * 100;
                progressBar.style.width = percentComplete + '%';
                uploadStatus.textContent = `Enviando... ${Math.round(percentComplete)}%`;
            }
        });

        // Load handler
        xhr.addEventListener('load', function() {
            if (xhr.status === 303 || xhr.status === 200) {
                uploadStatus.textContent = 'Upload concluído!';
                progressBar.classList.remove('progress-bar-animated');
                progressBar.classList.add('bg-success');

                // Redirecionar
                const redirectUrl = xhr.getResponseHeader('Location') || '/perfil?foto_sucesso=1';
                setTimeout(() => {
                    window.location.href = redirectUrl;
                }, 500);
            } else {
                uploadStatus.textContent = 'Erro no upload';
                progressBar.classList.add('bg-danger');
                btnAlterar.disabled = false;
                btnCancelar.disabled = false;
            }
        });

        // Error handler
        xhr.addEventListener('error', function() {
            uploadStatus.textContent = 'Erro de conexão';
            progressBar.classList.add('bg-danger');
            btnAlterar.disabled = false;
            btnCancelar.disabled = false;
        });

        // Enviar
        xhr.open('POST', form.action);
        xhr.send(formData);
    });

    function carregarImagem(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();

            reader.onload = function(e) {
                const img = new Image();

                img.onload = function() {
                    resolve(img);
                };

                img.onerror = function() {
                    reject(new Error('Não foi possível carregar a imagem'));
                };

                img.src = e.target.result;
            };

            reader.onerror = function() {
                reject(new Error('Não foi possível ler o arquivo'));
            };

            reader.readAsDataURL(file);
        });
    }

    window.cancelarSelecao = function() {
        fotoInput.value = '';
        fotoAtual.style.display = 'block';
        previewContainer.style.display = 'none';
        progressContainer.style.display = 'none';
        btnAlterar.disabled = true;
        btnAlterar.innerHTML = '<i class="bi-camera"></i> Alterar Foto';
        btnCancelar.style.display = 'none';
        progressBar.style.width = '0%';
        progressBar.classList.remove('bg-success', 'bg-danger');
    };
});
```

---

### 3.6 Correção do SQL Duplicado

#### Arquivo `sql/usuario_sql.py` (corrigido):

```python
CRIAR_TABELA = """
CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    telefone TEXT NOT NULL,
    perfil TEXT NOT NULL DEFAULT 'tutor',
    foto TEXT,
    token_redefinicao TEXT,
    data_token TIMESTAMP,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

INSERIR = """
INSERT INTO usuario (nome, email, senha, telefone, perfil)
VALUES (?, ?, ?, ?, ?);
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

# ← REMOVIDO: Duplicação eliminada
ATUALIZAR_FOTO = """
UPDATE usuario
SET foto = ?
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
    telefone,
    perfil,
    foto,
    token_redefinicao,
    data_token,
    data_cadastro
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
    telefone,
    perfil,
    foto,
    token_redefinicao,
    data_token,
    data_cadastro
FROM usuario
WHERE id_usuario = ?;
"""

OBTER_POR_EMAIL = """
SELECT
    id_usuario, nome, email, senha, telefone, perfil, foto,
    token_redefinicao, data_token, data_cadastro
FROM usuario
WHERE email = ?;
"""

ATUALIZAR_TOKEN = """
UPDATE usuario
SET token_redefinicao = ?, data_token = ?
WHERE email = ?;
"""

OBTER_POR_TOKEN = """
SELECT
    id_usuario, nome, email, senha, telefone, perfil, foto,
    token_redefinicao, data_token, data_cadastro
FROM usuario
WHERE token_redefinicao = ? AND data_token > datetime('now');
"""
```

---

### 3.7 Configuração de Logging

#### Adicionar ao `main.py`:

```python
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Configurar logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Handler para arquivo
file_handler = RotatingFileHandler(
    'logs/app.log',
    maxBytes=10 * 1024 * 1024,  # 10MB
    backupCount=5
)
file_handler.setLevel(logging.INFO)

# Handler para console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)

# Formato
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Configurar logger raiz
logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler, console_handler]
)

# Logger específico para uploads
upload_logger = logging.getLogger('upload')
upload_logger.setLevel(logging.INFO)
```

#### Adicionar ao `.gitignore`:

```gitignore
# Logs
logs/
*.log
```

---

## 4. Plano de Implementação

### Fase 1: Segurança Crítica (PRIORITÁRIO)

- [ ] Criar `config/upload_config.py`
- [ ] Criar `util/file_validator.py` com validação de magic bytes
- [ ] Implementar limite de tamanho de arquivo
- [ ] Adicionar validação de dimensões
- [ ] Implementar limpeza de fotos antigas
- [ ] Corrigir SQL duplicado

**Tempo estimado:** 4-6 horas
**Risco se não implementado:** ALTO - vulnerabilidades de segurança

---

### Fase 2: Permissões e Gestão

- [ ] Criar `util/file_manager.py`
- [ ] Implementar verificação de permissões
- [ ] Adicionar logging estruturado
- [ ] Configurar .gitignore
- [ ] Criar arquivos .gitkeep

**Tempo estimado:** 2-3 horas
**Risco se não implementado:** MÉDIO - problemas operacionais

---

### Fase 3: Melhorias de UX

- [ ] Adicionar barra de progresso
- [ ] Melhorar mensagens de erro
- [ ] Implementar validações no frontend aprimoradas
- [ ] Adicionar indicadores visuais

**Tempo estimado:** 3-4 horas
**Risco se não implementado:** BAIXO - apenas UX

---

### Fase 4: Otimizações (Opcional)

- [ ] Implementar redimensionamento automático
- [ ] Adicionar funcionalidade de crop
- [ ] Implementar compressão de imagens
- [ ] Adicionar suporte a WebP
- [ ] Cache de imagens

**Tempo estimado:** 6-8 horas
**Risco se não implementado:** NENHUM - são melhorias

---

## 5. Checklist de Segurança

### Antes do Deploy

- [ ] Todos os arquivos validados por magic bytes
- [ ] Limite de tamanho configurado
- [ ] Permissões de arquivo corretas (644)
- [ ] Permissões de diretório corretas (755)
- [ ] Fotos antigas são deletadas
- [ ] Logging funcionando
- [ ] Tratamento de erros específico
- [ ] Mensagens de erro não revelam informações sensíveis
- [ ] .gitignore configurado
- [ ] Testes de segurança executados
- [ ] Validação de path traversal
- [ ] Sanitização de nomes de arquivo

---

## 6. Testes Recomendados

### Testes Funcionais

```python
# test_upload_foto.py
import pytest
from fastapi.testclient import TestClient
from io import BytesIO
from PIL import Image

def test_upload_foto_valida(client: TestClient, auth_headers):
    """Teste: upload de foto válida"""
    # Criar imagem fake
    img = Image.new('RGB', (200, 200), color='red')
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)

    response = client.post(
        '/perfil/alterar-foto',
        files={'foto': ('test.jpg', img_bytes, 'image/jpeg')},
        headers=auth_headers
    )

    assert response.status_code == 303
    assert 'foto_sucesso=1' in response.headers['location']

def test_upload_arquivo_muito_grande(client: TestClient, auth_headers):
    """Teste: arquivo excede limite de tamanho"""
    # Criar arquivo grande (10MB)
    arquivo_grande = BytesIO(b'x' * (10 * 1024 * 1024))

    response = client.post(
        '/perfil/alterar-foto',
        files={'foto': ('grande.jpg', arquivo_grande, 'image/jpeg')},
        headers=auth_headers
    )

    assert 'erro' in response.headers['location']

def test_upload_tipo_invalido(client: TestClient, auth_headers):
    """Teste: tipo de arquivo não permitido"""
    arquivo_txt = BytesIO(b'nao sou uma imagem')

    response = client.post(
        '/perfil/alterar-foto',
        files={'foto': ('fake.jpg', arquivo_txt, 'text/plain')},
        headers=auth_headers
    )

    assert 'erro' in response.headers['location']

def test_path_traversal(client: TestClient, auth_headers):
    """Teste: tentativa de path traversal"""
    img = Image.new('RGB', (200, 200), color='red')
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)

    response = client.post(
        '/perfil/alterar-foto',
        files={'foto': ('../../etc/passwd.jpg', img_bytes, 'image/jpeg')},
        headers=auth_headers
    )

    # Deve falhar ou sanitizar o nome
    # Verificar que arquivo não foi salvo fora do diretório
    assert not Path('/etc/passwd.jpg').exists()
```

### Testes de Segurança

```bash
# Teste manual: Tentar upload de executável disfarçado
cp /bin/ls fake_image.jpg
# Fazer upload via interface → Deve falhar

# Teste manual: Arquivo com nome malicioso
touch "../../../etc/passwd.jpg"
# Fazer upload → Deve falhar ou sanitizar

# Teste: Arquivo muito grande
dd if=/dev/zero of=huge.jpg bs=1M count=100
# Fazer upload → Deve falhar com erro de tamanho
```

---

## 7. Conformidade LGPD

### Pontos Atendidos com as Melhorias

- ✅ **Minimização de Dados:** Fotos antigas são deletadas
- ✅ **Direito ao Esquecimento:** Sistema permite deletar dados
- ✅ **Segurança:** Validações robustas protegem dados
- ✅ **Logs Auditáveis:** Registro de operações
- ✅ **Controle de Acesso:** Apenas dono pode alterar foto

---

## 8. Documentação para Desenvolvedores

### Como Usar o Novo Sistema

```python
# Em qualquer rota que precise de upload:

from util.file_validator import FileValidator, FileValidationError
from util.file_manager import FileManager

async def minha_rota_upload(arquivo: UploadFile):
    try:
        # 1. Validar
        conteudo, extensao = await FileValidator.validar_imagem_completo(arquivo)

        # 2. Gerar nome seguro
        nome = FileValidator.gerar_nome_arquivo_seguro(extensao)

        # 3. Salvar
        caminho = FileManager.salvar_arquivo(conteudo, nome, user_id)

        # 4. Usar caminho no banco
        repo.atualizar(user_id, foto=caminho)

    except FileValidationError as e:
        # Tratar erro de validação
        return {"erro": str(e)}
```

---

## 9. Referências

- [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)
- [FastAPI Security Best Practices](https://fastapi.tiangolo.com/tutorial/security/)
- [Python Pillow Documentation](https://pillow.readthedocs.io/)
- [LGPD - Lei Geral de Proteção de Dados](http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)

---

## 10. Conclusão

A implementação atual da funcionalidade de alteração de foto de perfil possui **múltiplas vulnerabilidades críticas de segurança** que expõem a aplicação a:

1. Upload de arquivos maliciosos
2. Ataques de negação de serviço (DoS)
3. Path traversal
4. Violação de privacidade (LGPD)
5. Esgotamento de recursos

As soluções propostas neste documento resolvem **todos os problemas identificados** e adicionam:

- ✅ Validação robusta em múltiplas camadas
- ✅ Proteção contra ataques comuns
- ✅ Conformidade com LGPD
- ✅ Melhor experiência do usuário
- ✅ Código mais manutenível
- ✅ Logging para auditoria

**Recomendação:** Implementar **Fase 1 imediatamente** antes de colocar em produção.
