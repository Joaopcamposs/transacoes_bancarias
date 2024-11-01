from decimal import Decimal

from pydantic import BaseModel, UUID4, field_validator


class CadastrarContaBancaria(BaseModel):
    numero_da_conta: str
    saldo: Decimal
    cpf_cliente: str

    @field_validator("saldo", mode="before")
    def formatar_saldo(cls, v):
        # Define o saldo com duas casas decimais
        return Decimal(v).quantize(Decimal("0.00"))


class AtualizarContaBancaria(BaseModel):
    numero_da_conta: str
    cpf_cliente: str


class LerContaBancaria(BaseModel):
    id: UUID4
    numero_da_conta: str
    saldo: Decimal
    cpf_cliente: str

    @field_validator("saldo", mode="before")
    def formatar_saldo(cls, v):
        # Define o saldo com duas casas decimais
        return Decimal(v).quantize(Decimal("0.00"))
