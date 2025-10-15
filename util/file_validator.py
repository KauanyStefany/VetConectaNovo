"""
Validador Robusto de Arquivos de Upload
"""
import uuid
from pathlib import Path
from typing import Tuple, Optional
from PIL import Image
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
