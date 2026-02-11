from sqlalchemy import Uuid

from business_contexts.domain.exceptions import (
    ClientNotFound,
    BankAccountNotFound,
    BankAccountAlreadyRegistered,
)
from business_contexts.repository.query_repo.client import ClientQueryRepo
from business_contexts.domain.aggregates.bank_account import Account
from business_contexts.repository.query_repo.bank_account import (
    BankAccountQueryRepo,
)
from business_contexts.repository.domain_repo.bank_account import (
    BankAccountDomainRepo,
)
from business_contexts.domain.entities.bank_account import (
    CreateBankAccount,
    UpdateBankAccount,
)
from business_contexts.utils.base_types import OperationType
from libs.ddd.adapters.viewers import Filters


async def create_account(
    bank_account: CreateBankAccount,
) -> Account:
    """Cadastra uma nova conta bancária, validando número único e existência do cliente."""
    account_with_same_number = await BankAccountQueryRepo().query_one_by_filters(
        Filters({"account_number": bank_account.account_number})
    )
    if account_with_same_number:
        raise BankAccountAlreadyRegistered

    client = await ClientQueryRepo().query_one_by_filters(
        Filters({"cpf": bank_account.client_cpf})
    )
    if not client:
        raise ClientNotFound

    new_bank_account = Account.return_aggregate_for_creation(
        account_number=bank_account.account_number,
        balance=bank_account.balance,
        client_cpf=bank_account.client_cpf,
    )

    result_id = await BankAccountDomainRepo().add(
        account=new_bank_account,
        operation_type=OperationType.INSERT,
    )
    new_bank_account.id = result_id

    return new_bank_account


async def update_account(
    updated_bank_account: UpdateBankAccount,
) -> Account:
    """Atualiza os dados de uma conta bancária existente."""
    account = await BankAccountDomainRepo().query_by_account_number(
        account_number=updated_bank_account._old_account_number
    )

    if not account:
        raise BankAccountNotFound

    account.update(
        account_number=updated_bank_account.account_number,
        client_cpf=updated_bank_account.client_cpf,
    )

    await BankAccountDomainRepo().add(
        account=account,
        operation_type=OperationType.UPDATE,
    )

    return account


async def delete_account(id: Uuid) -> str:
    """Remove uma conta bancária pelo ID."""
    account = await BankAccountDomainRepo().query_by_id(id=id)

    if not account:
        raise BankAccountNotFound

    await BankAccountDomainRepo().remove(account=account)

    return "Conta bancária deletada!"
