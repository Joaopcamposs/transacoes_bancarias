from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from business_contexts.domain.value_objects.bank_transaction import (
    TransactionType,
)
from business_contexts.utils.base_types import AccountNumber
from libs.ddd.domain.aggregate import Aggregate


@dataclass
class Transaction(Aggregate):
    """Agregado que representa uma transação bancária."""

    type: TransactionType
    amount: Decimal
    date: datetime
    account_number: AccountNumber
    destination_account_number: AccountNumber | None = None
    id: UUID | None = None

    @classmethod
    def return_aggregate_for_creation(
        cls,
        type: TransactionType,
        amount: Decimal,
        date: datetime,
        account_number: AccountNumber,
        destination_account_number: AccountNumber | None = None,
    ) -> "Transaction":
        """Retorna uma instância do agregado Transaction preparada para cadastro."""
        return Transaction(
            type=type,
            amount=amount,
            date=date,
            account_number=account_number,
            destination_account_number=destination_account_number,
        )

    def create(self) -> None:
        """Executa a lógica de criação da transação."""
        ...

    def update(self) -> None:
        """Executa a lógica de atualização da transação."""
        ...

    def remove(self) -> None:
        """Executa a lógica de remoção da transação."""
        ...
