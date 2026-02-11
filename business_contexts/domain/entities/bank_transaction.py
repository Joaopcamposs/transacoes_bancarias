from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, UUID4, field_validator

from business_contexts.domain.aggregates.bank_transaction import Transaction
from business_contexts.domain.value_objects.bank_transaction import (
    TransactionType,
)
from business_contexts.utils.base_types import AccountNumber


class CreateBankTransaction(BaseModel):
    """Modelo de entrada para cadastro de transação bancária."""

    type: TransactionType
    amount: Decimal
    account_number: str
    destination_account_number: str = ""

    @field_validator("amount", mode="before")
    def format_amount(cls, v: Decimal | str | float) -> Decimal:
        """Formata o valor da transação com duas casas decimais."""
        return Decimal(v).quantize(Decimal("0.00"))


class ReadBankTransaction(BaseModel):
    """Modelo de saída para leitura de transação bancária."""

    id: UUID4
    type: TransactionType
    amount: Decimal
    date: datetime
    account_number: str
    destination_account_number: str | None = None

    @field_validator("amount", mode="before")
    def format_amount(cls, v: Decimal | str | float) -> Decimal:
        """Formata o valor da transação com duas casas decimais."""
        return Decimal(v).quantize(Decimal("0.00"))

    @staticmethod
    def from_transaction(transaction: Transaction) -> "ReadBankTransaction":
        """Cria uma instância de ReadBankTransaction a partir de um agregado Transaction."""
        return ReadBankTransaction(
            id=transaction.id,
            type=transaction.type,
            amount=transaction.amount,
            date=transaction.date,
            account_number=transaction.account_number,
            destination_account_number=transaction.destination_account_number,
        )


@dataclass(frozen=True)
class TransactionEntity:
    """Entidade imutável que representa uma transação consultada do banco de dados."""

    type: TransactionType
    amount: Decimal
    date: datetime
    account_number: AccountNumber
    id: UUID | None = None
    destination_account_number: AccountNumber | None = None
