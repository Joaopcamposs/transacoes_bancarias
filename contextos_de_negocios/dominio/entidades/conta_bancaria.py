from dataclasses import dataclass
from decimal import Decimal

from pydantic import BaseModel, UUID4, field_validator

from contextos_de_negocios.dominio.entidades.transacao_bancaria import (
    LerTransacaoBancaria,
)
from contextos_de_negocios.repositorio.orm.transacao_bancaria import TransacaoBancaria


class CadastrarContaBancaria(BaseModel):
    numero_da_conta: str
    saldo: Decimal
    cpf_cliente: str

    @field_validator("saldo", mode="before")
    def formatar_saldo(cls, v):
        return Decimal(v).quantize(Decimal("0.00"))


class AtualizarContaBancaria(BaseModel):
    numero_da_conta: str
    cpf_cliente: str

    _numero_da_conta_antigo: UUID4 | None = None


class LerContaBancaria(BaseModel):
    id: UUID4
    numero_da_conta: str
    saldo: Decimal
    cpf_cliente: str

    @field_validator("saldo", mode="before")
    def formatar_saldo(cls, v):
        return Decimal(v).quantize(Decimal("0.00"))

    @staticmethod
    def from_conta(conta: "ContaEntidade"):
        return LerContaBancaria(
            id=conta.id,
            numero_da_conta=conta.numero_da_conta,
            saldo=conta.saldo,
            cpf_cliente=conta.cpf_cliente,
        )


class LerContaBancariaETransacoes(BaseModel):
    contas: list[LerContaBancaria]
    transacoes: list[LerTransacaoBancaria]


@dataclass(frozen=True)
class ContaEntidade:
    id: UUID4
    numero_da_conta: str
    saldo: Decimal
    cpf_cliente: str
    transacoes: list[TransacaoBancaria] | None = None
