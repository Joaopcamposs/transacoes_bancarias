from uuid import UUID

from sqlalchemy import update, insert, select

from business_contexts.domain.aggregates.bank_account import Account
from business_contexts.domain.aggregates.bank_transaction import Transaction
from business_contexts.domain.value_objects.bank_transaction import (
    TransactionType,
)
from libs.ddd.adapters.repository import DomainRepository


class BankTransactionDomainRepo(DomainRepository):
    """Repositório de domínio para operações de escrita de transações bancárias."""

    async def add(
        self,
        transaction: Transaction,
    ) -> UUID:
        """Adiciona uma transação bancária e atualiza os saldos das contas envolvidas."""
        async with self:
            try:
                await self.__lock_accounts_for_concurrency(
                    transaction.account_number, transaction.destination_account_number
                )

                data: dict = {
                    "type": transaction.type.value,
                    "amount": transaction.amount,
                    "date": transaction.date,
                    "account_number": transaction.account_number,
                    "destination_account_number": transaction.destination_account_number,
                }
                operation = insert(Transaction).values(data).returning(Transaction.id)
                result = await self.session.execute(operation)

                moved_amount = transaction.amount
                if transaction.type in [
                    TransactionType.WITHDRAWAL,
                    TransactionType.TRANSFER,
                ]:
                    moved_amount *= -1

                update_origin_account_balance = (
                    update(Account)
                    .where(Account.account_number == transaction.account_number)
                    .values(balance=Account.balance + moved_amount)
                )
                await self.session.execute(update_origin_account_balance)

                if transaction.destination_account_number:
                    update_destination_account_balance = (
                        update(Account)
                        .where(
                            Account.account_number
                            == transaction.destination_account_number
                        )
                        .values(balance=Account.balance + transaction.amount)
                    )
                    await self.session.execute(update_destination_account_balance)

                await self.commit()
            except Exception as error:
                await self.rollback()
                raise error

            result_id: UUID | None = transaction.id
            if not result_id:
                result_id = result.scalar_one_or_none()

        return result_id

    async def __lock_accounts_for_concurrency(
        self, origin_account_number: str, destination_account_number: str | None = None
    ) -> None:
        """Bloqueia as contas envolvidas para evitar problemas de concorrência."""
        lock_origin_account = (
            select(Account)
            .where(Account.account_number == origin_account_number)
            .with_for_update()
        )
        await self.session.execute(lock_origin_account)

        if destination_account_number:
            lock_destination_account = (
                select(Account)
                .where(Account.account_number == destination_account_number)
                .with_for_update()
            )
            await self.session.execute(lock_destination_account)
