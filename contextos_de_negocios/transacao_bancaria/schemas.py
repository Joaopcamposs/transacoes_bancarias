from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, UUID4, field_validator

from contextos_de_negocios.transacao_bancaria.models import TransacaoBancaria
from contextos_de_negocios.transacao_bancaria.objetos_de_valor import TipoTransacao


class CadastrarTransacaoBancaria(BaseModel):
    tipo: TipoTransacao
    valor: Decimal
    numero_da_conta: str
    numero_da_conta_destino: str | None = None

    @field_validator("valor", mode="before")
    def formatar_saldo(cls, v):
        return Decimal(v).quantize(Decimal("0.00"))


class LerTransacaoBancaria(BaseModel):
    id: UUID4
    tipo: TipoTransacao
    valor: Decimal
    data: datetime
    numero_da_conta: str
    numero_da_conta_destino: str | None = None

    @field_validator("valor", mode="before")
    def formatar_saldo(cls, v):
        return Decimal(v).quantize(Decimal("0.00"))

    @staticmethod
    def from_transacao(transacao: TransacaoBancaria):
        return LerTransacaoBancaria(
            id=transacao.id,
            tipo=transacao.tipo,
            valor=transacao.valor,
            data=transacao.data,
            numero_da_conta=transacao.numero_da_conta,
            numero_da_conta_destino=transacao.numero_da_conta_destino,
        )
