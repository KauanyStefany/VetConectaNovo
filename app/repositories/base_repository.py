"""
Repositório base com operações CRUD comuns.
Elimina duplicação de código entre repositórios.
"""

from typing import TypeVar, Generic, Optional, List, Any, Tuple
from app.db.connection import get_connection

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """
    Classe base para repositórios com operações CRUD genéricas.

    Subclasses devem implementar:
    - _row_to_model(row) -> T: Converter row do banco para model
    """

    def _executar_query(self, sql: str, parametros: Tuple[Any, ...] = (), commit: bool = True) -> Any:
        """
        Executa uma query SQL e retorna o cursor.

        Args:
            sql: Query SQL a executar
            parametros: Tupla de parâmetros para a query
            commit: Se True, faz commit após execução

        Returns:
            Cursor do banco de dados
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, parametros)
            if commit:
                conn.commit()
            return cursor

    def _obter_um(self, sql: str, parametros: Tuple[Any, ...] = ()) -> Optional[T]:
        """
        Executa query e retorna um único registro convertido para model.

        Args:
            sql: Query SQL a executar
            parametros: Tupla de parâmetros para a query

        Returns:
            Model do tipo T ou None se não encontrado
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, parametros)
            row = cursor.fetchone()
            return self._row_to_model(row) if row else None

    def _obter_todos(self, sql: str, parametros: Tuple[Any, ...] = ()) -> List[T]:
        """
        Executa query e retorna lista de registros convertidos para models.

        Args:
            sql: Query SQL a executar
            parametros: Tupla de parâmetros para a query

        Returns:
            Lista de models do tipo T
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, parametros)
            rows = cursor.fetchall()
            return [self._row_to_model(row) for row in rows]

    def _contar(self, sql: str, parametros: Tuple[Any, ...] = ()) -> int:
        """
        Executa query de contagem e retorna o número.

        Args:
            sql: Query SQL de contagem (SELECT COUNT...)
            parametros: Tupla de parâmetros para a query

        Returns:
            Número de registros
        """
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, parametros)
            row = cursor.fetchone()
            return row[0] if row else 0

    def _row_to_model(self, row: Any) -> T:
        """
        Converte uma row do banco de dados para o model correspondente.

        DEVE ser implementado pelas subclasses.

        Args:
            row: Row do banco (sqlite3.Row)

        Returns:
            Instância do model do tipo T
        """
        raise NotImplementedError(f"{self.__class__.__name__} deve implementar _row_to_model()")
