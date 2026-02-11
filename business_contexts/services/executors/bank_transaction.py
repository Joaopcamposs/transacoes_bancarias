from business_contexts.domain.aggregates.bank_transaction import Transaction
from business_contexts.domain.exceptions import BankAccountNotFound
from business_contexts.repository.query_repo.bank_account import (
    BankAccountQueryRepo,
)
from business_contexts.repository.domain_repo.bank_account import (
    BankAccountDomainRepo,
)
from business_contexts.repository.domain_repo.bank_transaction import (
    BankTransactionDomainRepo,
)
from business_contexts.domain.entities.bank_transaction import (
    CreateBankTransaction,
)
from libs.ddd.adapters.viewers import Filters


async def create_bank_transaction(
    bank_transaction: CreateBankTransaction,
) -> Transaction:
    """Cadastra uma nova transação bancária, validando as contas envolvidas."""
    origin_account = await BankAccountDomainRepo().query_by_account_number(
        account_number=bank_transaction.account_number
    )
    if not origin_account:
        raise BankAccountNotFound

    if bank_transaction.destination_account_number:
        destination_account = await BankAccountQueryRepo().query_one_by_filters(
            Filters({"account_number": bank_transaction.destination_account_number})
        )
        if not destination_account:
            raise BankAccountNotFound

    new_bank_transaction: Transaction = origin_account.new_transaction(bank_transaction)
    result_id = await BankTransactionDomainRepo().add(
        transaction=new_bank_transaction,
    )
    new_bank_transaction.id = result_id

    return new_bank_transaction
