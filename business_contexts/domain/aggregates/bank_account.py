from dataclasses import dataclass, field
from uuid import UUID

from _decimal import Decimal

from business_contexts.domain.aggregates.bank_transaction import Transaction
from business_contexts.domain.exceptions import (
    InsufficientBalanceForTransaction,
)
from business_contexts.domain.value_objects.bank_transaction import (
    TransactionType,
)
from business_contexts.domain.entities.bank_transaction import (
    CreateBankTransaction,
)
from business_contexts.domain.business_rules.bank_transaction import (
    get_local_time,
)
from business_contexts.utils.base_types import AccountNumber, CPF
from libs.ddd.domain.aggregate import Aggregate


@dataclass
class Account(Aggregate):
    """Agregado raiz que representa uma conta bancária no sistema."""

    account_number: AccountNumber | str
    balance: Decimal
    client_cpf: CPF | str
    id: UUID | None = None
    transactions: list[Transaction] = field(default_factory=list)

    @classmethod
    def return_aggregate_for_creation(
        cls, account_number: AccountNumber, balance: Decimal, client_cpf: CPF
    ) -> "Account":
        """Retorna uma instância do agregado Account preparada para cadastro."""
        return Account(
            account_number=account_number, balance=balance, client_cpf=client_cpf
        )

    @staticmethod
    def _validate_operation_amount(amount: Decimal) -> None:
        """Valida se o valor da operação não é negativo."""
        if amount < 0:
            raise ValueError("Valor da operação não pode ser negativo")

    def _validate_balance(self, amount: Decimal) -> None:
        """Valida se o saldo é suficiente para a operação."""
        if self.balance < amount:
            raise InsufficientBalanceForTransaction

    def new_transaction(self, bank_transaction: CreateBankTransaction) -> Transaction:
        """Processa uma nova transação bancária de acordo com seu tipo."""
        self._validate_operation_amount(bank_transaction.amount)

        match bank_transaction.type:
            case TransactionType.WITHDRAWAL:
                return self.perform_withdrawal(bank_transaction.amount)
            case TransactionType.DEPOSIT:
                return self.perform_deposit(bank_transaction.amount)
            case TransactionType.TRANSFER:
                return self.perform_transfer(
                    bank_transaction.amount, bank_transaction.destination_account_number
                )
            case _:
                raise ValueError("Tipo de transação inválido")

    def perform_withdrawal(self, amount: Decimal) -> Transaction:
        """Realiza um saque na conta, validando saldo e retornando a transação."""
        self._validate_balance(amount)

        self.balance -= amount
        return Transaction.return_aggregate_for_creation(
            type=TransactionType.WITHDRAWAL,
            amount=amount,
            account_number=self.account_number,
            date=get_local_time(),
        )

    def perform_deposit(self, amount: Decimal) -> Transaction:
        """Realiza um depósito na conta e retorna a transação."""
        self.balance += amount
        return Transaction.return_aggregate_for_creation(
            type=TransactionType.DEPOSIT,
            amount=amount,
            account_number=self.account_number,
            date=get_local_time(),
        )

    def perform_transfer(
        self, amount: Decimal, destination_account_number: str
    ) -> Transaction:
        """Realiza uma transferência, validando saldo e retornando a transação."""
        self._validate_balance(amount)

        self.balance -= amount
        return Transaction.return_aggregate_for_creation(
            type=TransactionType.TRANSFER,
            amount=amount,
            account_number=self.account_number,
            destination_account_number=destination_account_number,
            date=get_local_time(),
        )

    def create(self) -> None:
        """Executa a lógica de criação da conta."""
        ...

    def update(self, account_number: AccountNumber, client_cpf: CPF) -> None:
        """Atualiza os dados da conta bancária."""
        self.account_number = account_number
        self.client_cpf = client_cpf

    def remove(self) -> None:
        """Executa a lógica de remoção da conta."""
        ...
