from enum import Enum

class StatusProjeto(str, Enum):
    ATIVO = "Ativo"
    PAUSADO = "Pausado"
    FINALIZADO = "Finalizado"
    