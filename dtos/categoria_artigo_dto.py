from pydantic import BaseModel, field_validator
from typing import Optional


class CategoriaCadastroDTO(BaseModel):
	nome: str
	descricao: Optional[str] = None

	@field_validator('nome')
	@classmethod
	def validate_nome(cls, nome: str) -> str:
		if not nome or not nome.strip():
			raise ValueError('Nome é obrigatório')
		nome_stripped = nome.strip()
		if len(nome_stripped) < 5:
			raise ValueError('Nome deve ter pelo menos 5 caracteres')
		return nome_stripped

	@field_validator('descricao')
	@classmethod
	def validate_descricao(cls, descricao: Optional[str]) -> Optional[str]:
		if descricao is None:
			return None
		desc = descricao.strip()
		if desc == "":
			return None
		if len(desc) > 1000:
			raise ValueError('Descrição muito longa (máx. 1000 caracteres)')
		return desc

#add campos cor e imagem