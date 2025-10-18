from enum import Enum

class ChamadoStatus(Enum):
    ABERTO = "aberto"
    EM_ANDAMENTO = "em_andamento"
    RESOLVIDO = "resolvido"

class DenunciaStatus(Enum):
    PENDENTE = "pendente"
    EM_ANALISE = "em_analise"
    RESOLVIDA = "resolvida"
    REJEITADA = "rejeitada"

class VerificacaoStatus(Enum):
    PENDENTE = "pendente"
    APROVADO = "aprovado"
    REJEITADO = "rejeitado"
    EM_ANALISE = "em_analise"

class PerfilUsuario(str, Enum):
    ADMIN = "admin"
    TUTOR = "tutor"
    VETERINARIO = "veterinario"