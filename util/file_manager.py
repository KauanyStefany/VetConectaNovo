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
