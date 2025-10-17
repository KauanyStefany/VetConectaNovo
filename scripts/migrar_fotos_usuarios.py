"""
Script de Migração de Fotos de Usuários

Migra fotos de /static/uploads/usuarios/ para /static/img/usuarios/
com novo formato de nome baseado no ID do usuário (000123.jpg).

Este script:
- Cria o diretório destino se não existir
- Copia (não move) as fotos para o novo local
- Renomeia arquivos para o formato 000123.jpg
- Atualiza registros no banco de dados
- Gera log detalhado da migração
- Preserva arquivos originais (não deleta)

Uso:
    python scripts/migrar_fotos_usuarios.py
"""
import os
import sys
import shutil
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple, List

# Adicionar o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.upload_config import UploadConfig
from util.db_util import get_connection
from util.file_manager import FileManager

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'migracao_fotos_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class MigracaoFotos:
    """Gerenciador de migração de fotos de usuários"""

    ORIGEM = Path("static/uploads/usuarios")
    DESTINO = Path("static/img/usuarios")

    def __init__(self):
        self.sucesso: List[Tuple[int, str, str]] = []
        self.erros: List[Tuple[str, str]] = []
        self.ignorados: List[str] = []

    def criar_diretorio_destino(self) -> bool:
        """Cria diretório destino se não existir"""
        try:
            self.DESTINO.mkdir(parents=True, exist_ok=True)
            self.DESTINO.chmod(UploadConfig.DIR_PERMISSIONS)
            logger.info(f"Diretório destino criado/verificado: {self.DESTINO}")
            return True
        except Exception as e:
            logger.error(f"Erro ao criar diretório destino: {e}")
            return False

    def extrair_id_usuario(self, nome_arquivo: str) -> Optional[int]:
        """
        Extrai ID do usuário do nome do arquivo

        Formatos suportados:
        - {id}_{hash}.{ext} (ex: 2_14f35b65a937a7a6.png)
        - {id}.{ext} (ex: 2.png)
        """
        try:
            # Remove extensão
            nome_sem_ext = Path(nome_arquivo).stem

            # Tenta extrair ID antes do underscore
            if '_' in nome_sem_ext:
                id_str = nome_sem_ext.split('_')[0]
            else:
                id_str = nome_sem_ext

            # Converte para int
            return int(id_str)
        except (ValueError, IndexError) as e:
            logger.warning(f"Não foi possível extrair ID de '{nome_arquivo}': {e}")
            return None

    def obter_extensao(self, nome_arquivo: str) -> str:
        """Obtém extensão do arquivo sem o ponto"""
        return Path(nome_arquivo).suffix.lstrip('.')

    def verificar_usuario_existe(self, id_usuario: int) -> bool:
        """Verifica se o usuário existe no banco de dados"""
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT id_usuario FROM usuario WHERE id_usuario = ?",
                    (id_usuario,)
                )
                return cursor.fetchone() is not None
        except Exception as e:
            logger.error(f"Erro ao verificar usuário {id_usuario}: {e}")
            return False

    def atualizar_foto_bd(self, id_usuario: int, novo_caminho: str) -> bool:
        """Atualiza caminho da foto no banco de dados"""
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE usuario SET foto = ? WHERE id_usuario = ?",
                    (novo_caminho, id_usuario)
                )
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            logger.error(f"Erro ao atualizar BD para usuário {id_usuario}: {e}")
            return False

    def migrar_foto(self, arquivo_origem: Path) -> bool:
        """
        Migra uma foto individual

        Returns:
            bool: True se sucesso, False caso contrário
        """
        nome_arquivo = arquivo_origem.name
        logger.info(f"Processando: {nome_arquivo}")

        # 1. Extrair ID do usuário
        id_usuario = self.extrair_id_usuario(nome_arquivo)
        if id_usuario is None:
            logger.warning(f"Ignorando arquivo: {nome_arquivo} (ID não identificado)")
            self.ignorados.append(nome_arquivo)
            return False

        # 2. Verificar se usuário existe no BD
        if not self.verificar_usuario_existe(id_usuario):
            logger.warning(
                f"Ignorando arquivo: {nome_arquivo} "
                f"(usuário {id_usuario} não existe no BD)"
            )
            self.ignorados.append(nome_arquivo)
            return False

        # 3. Obter extensão
        extensao = self.obter_extensao(nome_arquivo)
        if not extensao:
            logger.warning(f"Ignorando arquivo: {nome_arquivo} (sem extensão)")
            self.ignorados.append(nome_arquivo)
            return False

        # 4. Gerar novo nome
        novo_nome = FileManager.gerar_nome_foto_usuario(id_usuario, extensao)
        arquivo_destino = self.DESTINO / novo_nome

        # 5. Copiar arquivo
        try:
            shutil.copy2(arquivo_origem, arquivo_destino)
            arquivo_destino.chmod(UploadConfig.FILE_PERMISSIONS)
            logger.info(f"Copiado: {nome_arquivo} -> {novo_nome}")
        except Exception as e:
            logger.error(f"Erro ao copiar {nome_arquivo}: {e}")
            self.erros.append((nome_arquivo, str(e)))
            return False

        # 6. Atualizar banco de dados
        novo_caminho = f"/static/img/usuarios/{novo_nome}"
        if not self.atualizar_foto_bd(id_usuario, novo_caminho):
            logger.error(
                f"Erro ao atualizar BD para {nome_arquivo}. "
                f"Arquivo copiado mas BD não atualizado."
            )
            self.erros.append((nome_arquivo, "Erro ao atualizar banco de dados"))
            return False

        # Registrar sucesso
        self.sucesso.append((id_usuario, nome_arquivo, novo_nome))
        logger.info(
            f"✓ Migração concluída: {nome_arquivo} -> {novo_nome} "
            f"(usuário: {id_usuario})"
        )
        return True

    def executar(self) -> bool:
        """
        Executa a migração completa

        Returns:
            bool: True se todas as migrações foram bem-sucedidas
        """
        logger.info("=" * 70)
        logger.info("INICIANDO MIGRAÇÃO DE FOTOS DE USUÁRIOS")
        logger.info("=" * 70)

        # 1. Verificar diretório origem
        if not self.ORIGEM.exists():
            logger.error(f"Diretório origem não existe: {self.ORIGEM}")
            return False

        # 2. Criar diretório destino
        if not self.criar_diretorio_destino():
            return False

        # 3. Listar arquivos
        arquivos = list(self.ORIGEM.glob("*"))
        arquivos = [f for f in arquivos if f.is_file()]

        if not arquivos:
            logger.warning("Nenhum arquivo encontrado para migrar")
            return True

        logger.info(f"Encontrados {len(arquivos)} arquivos para processar")
        logger.info("-" * 70)

        # 4. Migrar cada arquivo
        for arquivo in arquivos:
            self.migrar_foto(arquivo)
            logger.info("-" * 70)

        # 5. Gerar relatório
        self.gerar_relatorio()

        return len(self.erros) == 0

    def gerar_relatorio(self):
        """Gera relatório final da migração"""
        logger.info("=" * 70)
        logger.info("RELATÓRIO DE MIGRAÇÃO")
        logger.info("=" * 70)

        logger.info(f"Total de arquivos processados: {len(self.sucesso) + len(self.erros) + len(self.ignorados)}")
        logger.info(f"✓ Sucesso: {len(self.sucesso)}")
        logger.info(f"✗ Erros: {len(self.erros)}")
        logger.info(f"⊘ Ignorados: {len(self.ignorados)}")

        if self.sucesso:
            logger.info("\nArquivos migrados com sucesso:")
            for id_usuario, origem, destino in self.sucesso:
                logger.info(f"  - Usuário {id_usuario:06d}: {origem} -> {destino}")

        if self.erros:
            logger.error("\nErros encontrados:")
            for arquivo, erro in self.erros:
                logger.error(f"  - {arquivo}: {erro}")

        if self.ignorados:
            logger.warning("\nArquivos ignorados:")
            for arquivo in self.ignorados:
                logger.warning(f"  - {arquivo}")

        logger.info("=" * 70)

        if len(self.erros) == 0:
            logger.info("✓ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
            logger.info("\nPróximos passos:")
            logger.info("1. Verificar se as fotos estão sendo exibidas corretamente")
            logger.info("2. Testar upload de novas fotos")
            logger.info("3. Após confirmação, deletar manualmente: static/uploads/usuarios/")
        else:
            logger.error("✗ MIGRAÇÃO CONCLUÍDA COM ERROS!")
            logger.error("Revise os erros acima antes de prosseguir")

        logger.info("=" * 70)


def main():
    """Função principal"""
    try:
        migracao = MigracaoFotos()
        sucesso = migracao.executar()

        if sucesso:
            sys.exit(0)
        else:
            sys.exit(1)

    except KeyboardInterrupt:
        logger.warning("\nMigração interrompida pelo usuário")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Erro inesperado: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
