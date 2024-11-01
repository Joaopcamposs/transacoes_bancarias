import enum


class TipoTransacao(enum.Enum):
    SAQUE = "saque"
    DEPOSITO = "deposito"
    TRANSFERENCIA = "transferencia"
