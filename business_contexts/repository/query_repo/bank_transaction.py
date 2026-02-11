from typing import Sequence

from sqlalchemy import select

from business_contexts.domain.aggregates.bank_transaction import Transaction
from business_contexts.domain.entities.bank_transaction import TransactionEntity
from libs.ddd.adapters.repository import QueryRepository
from libs.ddd.adapters.viewers import Filters


class BankTransactionQueryRepo(QueryRepository):
    """Repositório de consulta para transações bancárias."""

    async def query_by_filters(self, filters: Filters) -> Sequence[TransactionEntity]:
        """Consulta transações bancárias aplicando os filtros fornecidos."""
        async with self:
            transactions = (
                (await self.session.execute(select(Transaction).filter_by(**filters)))
                .scalars()
                .all()
            )

            transaction_entities: list[TransactionEntity] = [
                TransactionEntity(
                    id=transaction.id,
                    type=transaction.type,
                    amount=transaction.amount,
                    date=transaction.date,
                    account_number=transaction.account_number,
                    destination_account_number=transaction.destination_account_number,
                )
                for transaction in transactions
            ]

        return transaction_entities

    async def query_one_by_filters(self, filters: Filters) -> TransactionEntity | None:
        """Consulta uma única transação bancária aplicando os filtros fornecidos."""
        transaction = (
            await self.session.execute(select(Transaction).filter_by(**filters))
        ).scalar_one_or_none()
        if not transaction:
            return None

        transaction_entity = TransactionEntity(
            id=transaction.id,
            type=transaction.type,
            amount=transaction.amount,
            date=transaction.date,
            account_number=transaction.account_number,
            destination_account_number=transaction.destination_account_number,
        )

        return transaction_entity
