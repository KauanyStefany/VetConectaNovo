"""
Classe base para todos os DTOs do sistema.
Fornece configurações padrão e métodos de validação comuns.
"""

from pydantic import BaseModel, ConfigDict

class BaseDTO(BaseModel):
    """
    Classe base para todos os DTOs do sistema.
    Fornece configurações padrão e métodos de validação comuns.

    Esta classe implementa:
    - Configurações padrão do Pydantic
    - Wrapper para tratamento de erros de validação
    - Métodos auxiliares para conversão de dados
    """

    model_config = ConfigDict(
        # Remover espaços em branco automaticamente
        str_strip_whitespace=True,
        # Validar na atribuição também (não só na criação)
        validate_assignment=True,
        # Usar valores dos enums ao invés dos objetos
        use_enum_values=True,
        # Permitir population by name (útil para formulários HTML)
        populate_by_name=True,
        # Validar valores padrão também
        validate_default=True
    )

    def to_dict(self) -> dict:
        """
        Converte DTO para dicionário simples.
        Remove campos None para limpar o retorno.

        Returns:
            Dicionário com os dados do DTO
        """
        return self.model_dump(exclude_none=True)

    def to_json(self) -> str:
        """
        Converte DTO para JSON.
        Remove campos None para limpar o retorno.

        Returns:
            String JSON com os dados do DTO
        """
        return self.model_dump_json(exclude_none=True)

    @classmethod
    def from_dict(cls, data: dict):
        """
        Cria DTO a partir de dicionário.

        Args:
            data: Dicionário com os dados

        Returns:
            Instância do DTO
        """
        return cls(**data)

    def __str__(self) -> str:
        """Representação string melhorada do DTO"""
        campos = ', '.join([f"{k}={v}" for k, v in self.to_dict().items()])
        return f"{self.__class__.__name__}({campos})"

    def __repr__(self) -> str:
        """Representação técnica do DTO"""
        return self.__str__()
