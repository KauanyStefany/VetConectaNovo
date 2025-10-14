from pydantic import BaseModel, field_validator
from typing import Optional
import re


class CategoriaCadastroDTO(BaseModel):
	nome: str
	cor: str
	imagem: str

	@field_validator('nome')
	@classmethod
	def validate_nome(cls, nome: str) -> str:
		if not nome or not nome.strip():
			raise ValueError('Nome é obrigatório')
		nome_stripped = nome.strip()
		if len(nome_stripped) < 5:
			raise ValueError('Nome deve ter pelo menos 5 caracteres')
		return nome_stripped

	@field_validator('cor')
	@classmethod
	def validate_cor(cls, cor: str) -> str:
		if not cor or not cor.strip():
			raise ValueError('Cor é obrigatória')
		cor = cor.strip()
		# aceitar formatos como #fff ou #ffffff
		if not re.match(r'^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$', cor):
			raise ValueError('Formato de cor inválido. Use hexadecimal (#RRGGBB ou #RGB)')
		return cor

	@field_validator('imagem')
	@classmethod
	def validate_imagem(cls, imagem: str) -> str:
		if not imagem or not imagem.strip():
			raise ValueError('Imagem é obrigatória')
		imagem = imagem.strip()
		# validação simples: aceitar caminhos/nomes com extensão comum
		if not re.search(r'\.(jpg|jpeg|png|gif)$', imagem, re.IGNORECASE):
			raise ValueError('Imagem deve ser um arquivo com extensão JPG, JPEG, PNG ou GIF')
		return imagem
