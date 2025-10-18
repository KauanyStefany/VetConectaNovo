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
            caminho_relativo = f"/static/img/usuarios/{nome_arquivo}"

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

    @staticmethod
    def gerar_nome_foto_usuario(id_usuario: int, extensao: str) -> str:
        """
        Gera nome de arquivo para foto de usuário no formato 000123.jpg

        Args:
            id_usuario: ID do usuário
            extensao: Extensão do arquivo (sem ponto, ex: 'jpg', 'png')

        Returns:
            str: Nome do arquivo (ex: '000123.jpg')
        """
        # Remove ponto da extensão se presente
        extensao_limpa = extensao.lstrip('.')

        # Gera nome usando o pattern configurado
        nome_base = UploadConfig.FOTO_USUARIO_PATTERN.format(id_usuario)
        return f"{nome_base}.{extensao_limpa}"

    @staticmethod
    def obter_foto_usuario_existente(id_usuario: int) -> Optional[Path]:
        """
        Busca foto existente do usuário em qualquer extensão permitida

        Args:
            id_usuario: ID do usuário

        Returns:
            Path do arquivo encontrado ou None
        """
        nome_base = UploadConfig.FOTO_USUARIO_PATTERN.format(id_usuario)

        for extensao in UploadConfig.ALLOWED_EXTENSIONS:
            # Remove ponto da extensão
            ext_limpa = extensao.lstrip('.')
            nome_arquivo = f"{nome_base}.{ext_limpa}"
            caminho_completo = UploadConfig.USUARIOS_DIR / nome_arquivo

            if caminho_completo.exists():
                return caminho_completo

        return None

    @staticmethod
    def deletar_todas_fotos_usuario(id_usuario: int):
        """
        Deleta todas as extensões possíveis de foto de um usuário

        Args:
            id_usuario: ID do usuário
        """
        nome_base = UploadConfig.FOTO_USUARIO_PATTERN.format(id_usuario)

        for extensao in UploadConfig.ALLOWED_EXTENSIONS:
            nome_arquivo = ""  # Inicializar para evitar UnboundLocalError
            try:
                # Remove ponto da extensão
                ext_limpa = extensao.lstrip('.')
                nome_arquivo = f"{nome_base}.{ext_limpa}"
                caminho_completo = UploadConfig.USUARIOS_DIR / nome_arquivo

                if caminho_completo.exists():
                    caminho_completo.unlink()
                    logger.info(
                        f"Foto deletada: {nome_arquivo} (usuário: {id_usuario})"
                    )
            except PermissionError as e:
                logger.error(
                    f"Sem permissão para deletar {nome_arquivo or extensao}: {e}"
                )
            except Exception as e:
                logger.error(
                    f"Erro ao deletar {nome_arquivo or extensao}: {e}",
                    exc_info=True
                )
