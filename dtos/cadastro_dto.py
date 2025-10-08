from pydantic import BaseModel, field_validator


class CadastroTutorDTO(BaseModel):
    nome: str
    email: str
    telefone: str
    senha: str


    @field_validator('nome')
    @classmethod
    def validate_nome(cls, nome):
        if not nome:
            raise ValueError('Nome é obrigatório')
        if len(nome.split()) < 2:
            raise ValueError('Nome deve ter pelo menos 2 palavras')
        return nome

    @field_validator('email')
    @classmethod
    def validate_email(cls, email):
        if not email:
            raise ValueError('E-mail é obrigatório')
        if '@' not in email or '.' not in email:
            raise ValueError('E-mail inválido')
        return email
    
    @field_validator('telefone')
    @classmethod
    def validate_telefone(cls, telefone):
        if not telefone:
            raise ValueError('Telefone é obrigatório')
        if len(telefone) < 10:
            raise ValueError('Telefone deve ter pelo menos 10 caracteres')
        return telefone
    
    
    @field_validator('senha')
    @classmethod
    def validate_senha(cls, senha):
        if not senha:
            raise ValueError('Senha é obrigatória')
        if len(senha) < 6:
            raise ValueError('Senha deve ter pelo menos 6 caracteres')
        return senha
    

class CadastroVeterinarioDTO(CadastroTutorDTO):
    crmv: str


    @field_validator('crmv')
    @classmethod
    def validate_crmv(cls, crmv):
        if crmv and len(crmv) < 6:
            raise ValueError('CRMV deve ter pelo menos 6 caracteres')
        return crmv