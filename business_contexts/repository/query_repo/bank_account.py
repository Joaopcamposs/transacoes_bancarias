from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from business_contexts.domain.aggregates.bank_account import Account
from business_contexts.domain.aggregates.bank_transaction import Transaction
from business_contexts.domain.entities.bank_account import AccountEntity
from libs.ddd.adapters.repository import QueryRepository
from libs.ddd.adapters.viewers import Filters


class BankAccountQueryRepo(QueryRepository):
    """Repositório de consulta para contas bancárias."""

    async def query_by_filters(self, filters: Filters) -> Sequence[AccountEntity]:
        """Consulta contas bancárias aplicando os filtros fornecidos."""
        list_transactions: bool = True
        if "list_transactions" in filters:
            list_transactions = filters.get("list_transactions")
            filters.pop("list_transactions")

        async with self:
            operation = select(Account).filter_by(**filters)
            if list_transactions:
                operation = operation.options(joinedload(Account.transactions))
            accounts = (await self.session.execute(operation)).unique().scalars().all()

            account_entities: list[AccountEntity] = []
            for account in accounts:
                transactions_list: list[Transaction] = []
                if list_transactions:
                    received_transactions = (
                        (
                            await self.session.execute(
                                select(Transaction).where(
                                    Transaction.destination_account_number
                                    == account.account_number
                                )
                            )
                        )
                        .scalars()
                        .all()
                    )

                    all_transactions = list(account.transactions) + list(
                        received_transactions
                    )
                    all_transactions.sort(key=lambda t: t.date, reverse=True)

                    transactions_list = [
                        Transaction(
                            id=transaction.id,
                            type=transaction.type,
                            amount=transaction.amount,
                            date=transaction.date,
                            account_number=transaction.account_number,
                            destination_account_number=transaction.destination_account_number,
                        )
                        for transaction in all_transactions
                    ]

                account_entities.append(
                    AccountEntity(
                        id=account.id,
                        account_number=account.account_number,
                        balance=account.balance,
                        client_cpf=account.client_cpf,
                        transactions=transactions_list,
                    )
                )

        return account_entities

    async def query_one_by_filters(self, filters: Filters) -> AccountEntity | None:
        """Consulta uma única conta bancária aplicando os filtros fornecidos."""
        list_transactions: bool = True
        if "list_transactions" in filters:
            list_transactions = filters.get("list_transactions")
            filters.pop("list_transactions")

        async with self:
            operation = select(Account).filter_by(**filters)
            if list_transactions:
                operation = operation.options(joinedload(Account.transactions))
            account = (
                (await self.session.execute(operation)).unique().scalar_one_or_none()
            )
            if not account:
                return None

            transactions_list: list[Transaction] = []
            if list_transactions:
                received_transactions = (
                    (
                        await self.session.execute(
                            select(Transaction).where(
                                Transaction.destination_account_number
                                == account.account_number
                            )
                        )
                    )
                    .scalars()
                    .all()
                )

                all_transactions = list(account.transactions) + list(
                    received_transactions
                )
                all_transactions.sort(key=lambda t: t.date, reverse=True)

                transactions_list = [
                    Transaction(
                        id=transaction.id,
                        type=transaction.type,
                        amount=transaction.amount,
                        date=transaction.date,
                        account_number=transaction.account_number,
                        destination_account_number=transaction.destination_account_number,
                    )
                    for transaction in all_transactions
                ]

            account_entity = AccountEntity(
                id=account.id,
                account_number=account.account_number,
                balance=account.balance,
                client_cpf=account.client_cpf,
                transactions=transactions_list,
            )

        return account_entity
