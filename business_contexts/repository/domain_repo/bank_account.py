from uuid import UUID

from sqlalchemy import select, insert, delete, update, Uuid
from sqlalchemy.orm import joinedload

from business_contexts.domain.aggregates.bank_account import Account
from business_contexts.domain.aggregates.bank_transaction import Transaction
from business_contexts.utils.base_types import OperationType
from libs.ddd.adapters.repository import DomainRepository


class BankAccountDomainRepo(DomainRepository):
    """Repositório de domínio para operações de escrita de contas bancárias."""

    async def query_by_id(self, id: Uuid) -> Account | None:
        """Consulta uma conta bancária pelo ID, incluindo transações."""
        async with self:
            bank_account = (
                (
                    await self.session.execute(
                        select(Account)
                        .options(joinedload(Account.transactions))
                        .filter_by(id=id)
                    )
                )
                .unique()
                .scalar_one_or_none()
            )

            if not bank_account:
                return None

            aggregate = Account(
                id=bank_account.id,
                account_number=bank_account.account_number,
                balance=bank_account.balance,
                client_cpf=bank_account.client_cpf,
                transactions=[
                    Transaction(
                        id=transaction.id,
                        type=transaction.type,
                        amount=transaction.amount,
                        date=transaction.date,
                        account_number=transaction.account_number,
                        destination_account_number=transaction.destination_account_number,
                    )
                    for transaction in bank_account.transactions
                ],
            )
        return aggregate

    async def query_by_account_number(self, account_number: str) -> Account | None:
        """Consulta uma conta bancária pelo número da conta, incluindo transações."""
        async with self:
            bank_account = (
                (
                    await self.session.execute(
                        select(Account)
                        .options(joinedload(Account.transactions))
                        .filter_by(account_number=account_number)
                    )
                )
                .unique()
                .scalar_one_or_none()
            )

            if not bank_account:
                return None

            aggregate = Account(
                id=bank_account.id,
                account_number=bank_account.account_number,
                balance=bank_account.balance,
                client_cpf=bank_account.client_cpf,
                transactions=[
                    Transaction(
                        id=transaction.id,
                        type=transaction.type,
                        amount=transaction.amount,
                        date=transaction.date,
                        account_number=transaction.account_number,
                        destination_account_number=transaction.destination_account_number,
                    )
                    for transaction in bank_account.transactions
                ],
            )
        return aggregate

    async def add(
        self,
        account: Account,
        operation_type: OperationType,
    ) -> UUID:
        """Adiciona ou atualiza uma conta bancária no banco de dados."""
        async with self:
            try:
                data: dict = {
                    "account_number": account.account_number,
                    "balance": account.balance,
                    "client_cpf": account.client_cpf,
                }

                match operation_type:
                    case OperationType.INSERT:
                        operation = insert(Account).values(data).returning(Account.id)
                        result = await self.session.execute(operation)

                    case OperationType.UPDATE:
                        operation = (
                            update(Account).where(Account.id == account.id).values(data)
                        )
                        await self.session.execute(operation)

                await self.commit()
            except Exception as error:
                await self.rollback()
                raise error

            result_id: UUID | None = account.id
            if not result_id:
                result_id = result.scalar_one_or_none()

        return result_id

    async def remove(self, account: Account) -> None:
        """Remove uma conta bancária do banco de dados."""
        async with self:
            try:
                operation = delete(Account).where(Account.id == account.id)

                await self.session.execute(operation)
                await self.commit()
            except Exception as error:
                await self.rollback()
                raise error
