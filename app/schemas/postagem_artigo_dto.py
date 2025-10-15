from pydantic import BaseModel, field_validator

class PostagemArtigoDTO(BaseModel):

    titulo: str
    conteudo: str
    id_categoria_artigo: int

    @field_validator('titulo')
    @classmethod
    def validate_titulo(cls, v):
        if not v or not v.strip():
            raise ValueError('Título é obrigatório')
        if len(v.split()) < 2:
            raise ValueError('O título deve ter pelo menos 2 palavras')
        if len(v.split()) > 20:
            raise ValueError('O título deve ter no máximo 20 palavras')
        return v

    @field_validator('conteudo')
    @classmethod
    def validate_conteudo(cls, v):
        if not v or not v.strip():
            raise ValueError('Conteúdo é obrigatório')
        if len(v.split()) < 10:
            raise ValueError('Conteúdo deve ter pelo menos 10 palavras')
        return v

    @field_validator('id_categoria_artigo')
    @classmethod
    def validate_id_categoria_artigo(cls, v):
        if not isinstance(v, int) or v <= 0:
            raise ValueError('ID da categoria é obrigatório e deve ser positivo')
        return v