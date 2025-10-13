from pydantic import BaseModel, field_validator

class PostagemFeedDTO(BaseModel):
    imagem: str | None = None
    descricao: str | None = None

    @field_validator('descricao')
    @classmethod
    def validate_descricao(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Descrição não pode ser vazia se fornecida')
        return v

    @field_validator('imagem')
    @classmethod
    def validate_imagem(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError('Imagem não pode ser vazia se fornecida')
            ext = v.lower().split('.')[-1]
            if ext not in ['jpg', 'jpeg', 'png']:
                raise ValueError('A imagem deve ser dos tipos: jpg, jpeg ou png')
        return v