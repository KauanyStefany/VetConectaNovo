"""
Configurações de Upload de Arquivos
"""
from pathlib import Path
from typing import Set


class UploadConfig:
    """Configurações centralizadas para upload de arquivos"""

    # Diretórios    
    USUARIOS_DIR = Path("static/img/usuarios")      

    # Formato de nome de arquivo para fotos de usuários
    FOTO_USUARIO_PATTERN = "{:08d}"  # Formato: 00000123 (8 dígitos)

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
        for directory in [cls.USUARIOS_DIR]:
            directory.mkdir(parents=True, exist_ok=True)
            directory.chmod(cls.DIR_PERMISSIONS)


# Inicializar na inicialização da aplicação
UploadConfig.init_directories()
