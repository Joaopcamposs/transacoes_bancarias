from dataclasses import dataclass
from decimal import Decimal

from pydantic import BaseModel, UUID4, field_validator

from business_contexts.domain.aggregates.bank_transaction import Transaction
from business_contexts.domain.entities.bank_transaction import (
    ReadBankTransaction,
)


class CreateBankAccount(BaseModel):
    """Modelo de entrada para cadastro de conta bancária."""

    account_number: str
    balance: Decimal
    client_cpf: str

    @field_validator("balance", mode="before")
    def format_balance(cls, v: Decimal | str | float) -> Decimal:
        """Formata o saldo com duas casas decimais."""
        return Decimal(v).quantize(Decimal("0.00"))


class UpdateBankAccount(BaseModel):
    """Modelo de entrada para atualização de conta bancária."""

    account_number: str
    client_cpf: str

    _old_account_number: UUID4 | None = None


class ReadBankAccount(BaseModel):
    """Modelo de saída para leitura de conta bancária."""

    id: UUID4
    account_number: str
    balance: Decimal
    client_cpf: str
    transactions: list[ReadBankTransaction]

    @field_validator("balance", mode="before")
    def format_balance(cls, v: Decimal | str | float) -> Decimal:
        """Formata o saldo com duas casas decimais."""
        return Decimal(v).quantize(Decimal("0.00"))

    @staticmethod
    def from_account(account: "AccountEntity") -> "ReadBankAccount":
        """Cria uma instância de ReadBankAccount a partir de uma AccountEntity."""
        return ReadBankAccount(
            id=account.id,
            account_number=account.account_number,
            balance=account.balance,
            client_cpf=account.client_cpf,
        )


@dataclass(frozen=True)
class AccountEntity:
    """Entidade imutável que representa uma conta bancária consultada do banco de dados."""

    id: UUID4
    account_number: str
    balance: Decimal
    client_cpf: str
    transactions: list[Transaction] | None = None
