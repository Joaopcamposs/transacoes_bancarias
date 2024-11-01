from decimal import Decimal

from pydantic import BaseModel, UUID4


class CadastrarContaBancaria(BaseModel):
    numero_da_conta: str
    saldo: Decimal
    cpf_cliente: str


class AtualizarContaBancaria(BaseModel):
    numero_da_conta: str
    cpf_cliente: str


class LerContaBancaria(BaseModel):
    id: UUID4
    numero_da_conta: str
    saldo: Decimal
    cpf_cliente: str
