from pydantic import BaseModel, field_validator


class ChamadoDTO(BaseModel):
    titulo: str
    descricao: str

    @field_validator('titulo')
    @classmethod
    def validate_titulo(cls, titulo):
        if not titulo or not titulo.strip():
            raise ValueError('Título é obrigatório')
        if len(titulo.split()) < 2:
            raise ValueError('Título deve ter pelo menos 2 palavras')
        return titulo.strip()

    @field_validator('descricao')
    @classmethod
    def validate_descricao(cls, descricao):
        if not descricao or not descricao.strip():
            raise ValueError('Descrição é obrigatória')
        if len(descricao.split()) < 5:
            raise ValueError('Descrição deve ter pelo menos 5 palavras')
        return descricao.strip()